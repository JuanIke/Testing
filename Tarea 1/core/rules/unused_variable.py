from _ast import FunctionDef, Name
from typing import Any
from ..rule import *
from collections import defaultdict


class UnusedVariableVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.dict =  {}

    def visit_FunctionDef(self, node):
        self.dict={}
        NodeVisitor.generic_visit(self, node)
        for cuerpo in node.body:
            if isinstance(cuerpo, Assign):
                for id in cuerpo.targets:
                    match id:
                        case Name(id=nombre, ctx=Store()):
                            if nombre != "self":
                                self.dict[nombre] = [id.lineno, False]
                if isinstance(cuerpo.value, BinOp):
                    match cuerpo.value:
                        case BinOp(
                        left=Name(id=nombre, ctx=Load()),
                        op=Add(),
                        right=Name(id=nombre2, ctx=Load())):
                            self.dict[nombre][1] = True
                            self.dict[nombre2][1] = True
                        case BinOp(
                        left=Name(id=nombre, ctx=Load()),
                        op=Add(),
                        right=_):
                            self.dict[nombre][1] = True
                        case BinOp(
                        left=_,
                        op=Add(),
                        right=Name(id=nombre, ctx=Load())):
                            self.dict[nombre][1] = True
            elif isinstance(cuerpo, Expr):
                if isinstance(cuerpo.value, Call):
                    for arg in cuerpo.value.args:
                        match arg:
                            case Name(id=nombre, ctx=Load()):
                                self.dict[nombre][1] = True
                                print(self.dict)
        for key, values in self.dict.items():
            if not values[1]:
                self.addWarning('UnusedVariable', values[0], 'variable ' + key + ' has not been used')
                            


    # def visit_Name(self, node: Name):
    #     NodeVisitor.generic_visit(self, node)
    #     match node:
    #         case Name(id=nombre, ctx=Store()):
    #             if nombre != "self":
    #                 self.dict[nombre] = [node.lineno, False]
    #         case Name(id=nombre, ctx=Load()):
    #             if nombre != "self":
    #                 self.dict[nombre][1] = True
    
    def impresor(self):
        pass
        # for key, values in self.dict.items():
        #     if not values[1]:
        #         self.addWarning('UnusedVariable', values[0], 'variable ' + key + ' has not been used')


class UnusedVariableTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        visitor.impresor()
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
