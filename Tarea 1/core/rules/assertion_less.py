from _ast import FunctionDef
from typing import Any
from ..rule import *


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()
        self.count = 0
        pass

    def visit_FunctionDef(self, node):
        NodeVisitor.generic_visit(self, node)
        self.count = 0
        for expression in node.body:
            match expression:
                case Expr(value=Call(
                    func=Attribute(
                        value=Name(id='self', ctx=Load()),
                        attr= nombre,
                        ctx=Load()),
                    args=args,
                    keywords= key)):
                    print("Entramos al caso")
                    if not nombre.startswith("assert"):
                        print("Wena  MAry")
                        self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')
                case Assign(
               targets=[
                  Name(id=_, ctx=Store())],
               value=Constant(value=_)):
                    self.count +=1
                case _:
                    print("Entré a case-")
                    self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')

        if self.count == len(node.body):
            print('AssertionLessWarning', node.lineno, 'it is an assertion less test')
            self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')    


class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = AssertionLessVisitor()
        visitor.visit(node)
        return visitor.warningsList()

        
    @classmethod
    def name(cls):
        return 'assertion-less'
