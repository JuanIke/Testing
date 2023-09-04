from _ast import FunctionDef
import ast
from typing import Any
from ..rule import *


class DuplicatedSetupVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.functions = []
        self.counter = 0
        self.min_len_fun = 10000
        self.equal = True

    def visit_FunctionDef(self, node: FunctionDef):
        NodeVisitor.generic_visit(self, node)
        
        self.una_function = []

        for cuerpo in node.body:
            match cuerpo:
                case Expr(value=Call(
                    func=Attribute(
                        value=Name(id=id, ctx=Load()),
                        attr= nombre,
                        ctx=Load()),
                    args=args,
                    keywords= key)):

                    string = "Exp, " + str(id) + ", " + str(nombre) + ", " + str(value) + ", args: "

                    for a in args:
                        if isinstance(a, Name):
                            string += "[Var: " + str(a.id) + "] "

                        elif isinstance(a, Constant):
                            string += "[Con: " + str(a.value) + "] "

                        elif isinstance(a, BinOp):
                            # primero left
                            if isinstance(a.left, Name):
                                string += "[BO: var " + str(a.left.id)
                            elif isinstance(a.left, Constant):
                                string += "[BO: con " + str(a.left.value)
                            #string += "[BO: " + str(a.left.) + "] "
                            # segundo op
                            string += "(" + str(a.op) + ")"
                            #tercero right
                            if isinstance(a.right, Name):
                                string += "var " + str(a.right.id) + "] "
                            elif isinstance(a.right, Constant):
                                string += "con " + str(a.right.value) + "] "

                    self.una_function.append(string)

                case Assign(
               targets=[
                  Name(id=id, ctx=Store())],
               value=Constant(value=value)):
                    string = "Ass, " + str(id) + ", " + str(value)
                    self.una_function.append(string)
      

        self.functions.append(self.una_function)

        if len(self.una_function) < self.min_len_fun:
            self.min_len_fun = len(self.una_function)

    
    def compare_functions(self):
        for pos in range(0, self.min_len_fun):
            first_fun = self.functions[0][pos]
            for fun in self.functions:
                if fun[pos] != first_fun:
                    self.equal = False # dejaron de ser iguales 
                    break
            
            if self.equal:
                self.counter += 1
            else:
                break

        if self.counter != 0:
            self.addWarning('DuplicatedSetup', self.counter, 'there are ' + str(self.counter) + ' duplicated setup statements')





class DuplicatedSetupRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(node)
        visitor.compare_functions()
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'duplicate-setup'
