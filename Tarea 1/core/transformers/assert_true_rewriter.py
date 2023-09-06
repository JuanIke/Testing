from ast import *
import ast
from core.rewriter import RewriterCommand


class AssertTrueTransformer(NodeTransformer):
    def visit_Call(self, node):
        NodeTransformer.generic_visit(self, node)
        if node.func.attr == 'assertEquals':
            return Call(
            func=Attribute(
               value=Name(id='self', ctx=Load()),
               attr='assertTrue',
               ctx=Load()),
            args=[node.args[0]],
            keywords=[])
        else:
            return node
        

class AssertTrueCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.

    def apply(self, tree):
        new_tree = fix_missing_locations(AssertTrueTransformer().visit(tree))
        return new_tree
