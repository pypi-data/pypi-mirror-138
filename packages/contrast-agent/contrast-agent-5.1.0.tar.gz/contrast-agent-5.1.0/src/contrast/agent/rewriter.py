# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib.abc
import importlib.machinery
import importlib.util
import types
import sys
import ast


import contrast
from contrast.agent import scope
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.utils import clear_properties
from contrast.agent.request_context import RequestContext
from contrast.patches.rewriter import contrast__add
from contrast.utils.decorators import fail_safely
from contrast.utils.environ import test_environ
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class ContrastMetaPathFinder(importlib.abc.MetaPathFinder):
    @fail_safely("Unexpected error in find_spec - will not rewrite this module")
    def find_spec(self, fullname, path, target=None):
        """
        The finder is in charge of finding a module's "spec". The spec includes import
        machinery metadata about the module - including its name, source file path, and
        the loader, among others.

        Here, we first use importlib's default machinery to get the spec for the module
        about to be imported. The problem with this spec is that it also uses the
        default loader, which isn't what we want. To get around this, we reuse some
        metadata and generate a new spec that points at our loader.

        It's possible that this is needlessly complicated. It's a first-pass
        implementation, so we can (and should) refactor this as we learn more.
        """
        default_spec = importlib.machinery.PathFinder.find_spec(fullname, path)

        if not default_spec:
            logger.debug(
                "WARNING: no spec found for module - fullname=<%s>, path=<%s>",
                fullname,
                path,
            )
            return None

        if not default_spec.origin.endswith(".py"):
            logger.debug(
                "Will not rewrite non *.py file - fullname=<%s>, path=<%s>",
                fullname,
                default_spec.origin,
            )
            return None

        return importlib.util.spec_from_file_location(
            fullname,
            default_spec.origin,
            loader=ContrastRewriteLoader(),
            submodule_search_locations=default_spec.submodule_search_locations,
        )


class ContrastRewriteLoader(importlib.abc.Loader):
    def create_module(self, _):
        """returning None uses the default behavior, which is fine"""
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        """
        This method is responsible for actually doing the module `exec`-ing. We take
        control of this system and do the following:
        - read the original source file. We require pyc caching to be disabled for this
        - parse the source file into an AST
        - rewrite the AST
        - compile the AST into a code object
        - exec the code object

        Note that we add our custom add function to the module's globals. This prevents
        the need for import rewriting entirely
        """
        filename = module.__spec__.origin
        with open(filename) as f:
            source = f.read()

        tree = ast.parse(source)
        if "contrast__add" not in module.__dict__:
            try:
                module.__dict__["contrast__add"] = contrast__add
                ConcatRewriter().visit(tree)
                ast.fix_missing_locations(tree)
            except Exception:
                logger.debug("WARNING: failed to rewrite %s", filename)
        else:
            logger.warning(
                "contrast__add is already defined in %s; will not rewrite", filename
            )

        co = compile(tree, filename, "exec", dont_inherit=True)
        exec(co, module.__dict__)


class ConcatRewriter(ast.NodeTransformer):
    def visit_BinOp(self, binop: ast.BinOp):
        """
        If we see an "Add" binary operation, replace it with a call to our custom add
        function, which includes all necessary instrumentation.
        """
        self.visit(binop.left)
        self.visit(binop.right)

        if not isinstance(binop.op, ast.Add):
            return binop

        binop_replacement = ast.Call(
            func=ast.Name(id="contrast__add", ctx=ast.Load()),
            args=[binop.left, binop.right],
            keywords=[],
        )
        ast.copy_location(binop_replacement, binop)
        return binop_replacement


@fail_safely("Unexpected error concat_works", log_level="debug", return_value=False)
def concat_works():
    """
    Tests to see if concat via hooks patches works in this environment
    by running a str concat test as if we were in a request.

    Return: True if propagation happened, False otherwise.
    """
    logger.debug("Testing if concat works.")

    with scope.pop_contrast_scope():
        one = "one"
        two = "two"
        properties = contrast.STRING_TRACKER.track(one)
        properties.add_tag("UNTRUSTED", AdjustedSpan(0, len(one)))

        context = RequestContext(test_environ)
        with contrast.CS__CONTEXT_TRACKER.lifespan(context):
            res = one + two

    properties = contrast.STRING_TRACKER.get(res)
    result = properties is not None

    clear_properties()
    return result


def register():
    """
    Register our rewriter with the import system. After this call, any newly imported
    modules (from source code) will use our custom rewriter.

    Note that because this function is defined in the same module that defines our add
    replacement function, we never have to worry about rewriting the addition in the
    replacement function itself. If that were to occur, we would get an infinite
    recursion.

    Rewriter should only run in py3.10 and only in environments in which our default
    patching mechanism does not work.
    """
    if not sys.version_info[:2] == (3, 10):
        # Don't register rewriter in a non py3.10 environment
        return

    if concat_works():
        # Don't register rewriter if concat already works.
        return

    sys.meta_path.insert(0, ContrastMetaPathFinder())
    logger.debug("enabled AST rewriter")


def deregister():
    """
    Remove our rewriter from the import system. Modules that were loaded by our rewriter
    will remain rewritten.

    Return True if we find and deregister our machinery, False otherwise.
    """
    for i, finder in enumerate(sys.meta_path.copy()):
        if isinstance(finder, ContrastMetaPathFinder):
            sys.meta_path.pop(i)
            return True
    return False
