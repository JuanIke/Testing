from _ast import AST, Assert, Assign
from typing import Any
from ..rule import *

class AssertionTrueVisitor(WarningNodeVisitor): 

    def __init__(self):
        super().__init__()
        self.values = {}

    def visit(self, node):
        match node:
            case Assign(
               targets=[
                  Name(id=id_constant, ctx=Store())],
               value=Constant(value=value)):
                self.values[id_constant] = value
            case Expr(
               value=Call(
                  func=Attribute(
                     value=Name(id='self', ctx=Load()),
                     attr='assertTrue',
                     ctx=Load()),
                  args=[
                     Constant(value=True)],
                  keywords=[])):
                self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
            case Expr(
               value=Call(
                  func=Attribute(
                     value=Name(id='self', ctx=Load()),
                     attr='assertTrue',
                     ctx=Load()),
                  args=[
                     Name(id=variable, ctx=Load())],
                  keywords=[])):
                if self.values[variable] == True:
                    self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
        NodeVisitor.generic_visit(self, node)


class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionTrueVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-true'

