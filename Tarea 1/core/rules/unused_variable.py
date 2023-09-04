from _ast import FunctionDef, Name
from typing import Any
from ..rule import *
from collections import defaultdict


class UnusedVariableVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        # Dicionario tipo {variable: [Número de linea, Booleano]}
        # Casos Bool; False: Variable instanciada, True: Variable ocupada
        self.dict =  {}

    def visit_FunctionDef(self, node):
        self.dict={}
        NodeVisitor.generic_visit(self, node)
        for cuerpo in node.body:
            # Si es una instancia Assign
            if isinstance(cuerpo, Assign):
                # Recorremos los targets
                for id in cuerpo.targets:
                    match id:
                        # Si un target el del tipo Name - Store()
                        case Name(id=nombre, ctx=Store()):
                            # Excluimos todos los name del tipo self
                            if nombre != "self":
                                self.dict[nombre] = [id.lineno, False]
                # Visitamos ahora los value. Si es del tipo BinOp
                if isinstance(cuerpo.value, BinOp):
                    match cuerpo.value:
                        # Caso en que la variable está en la izquierda y derecha
                        case BinOp(
                        left=Name(id=nombre, ctx=Load()),
                        op=Add(),
                        right=Name(id=nombre2, ctx=Load())):
                            self.dict[nombre][1] = True
                            self.dict[nombre2][1] = True
                        # Caso en que la variable está a la izquierda
                        case BinOp(
                        left=Name(id=nombre, ctx=Load()),
                        op=Add(),
                        right=_):
                            self.dict[nombre][1] = True
                        # Caso en que la variable está a la derecha
                        case BinOp(
                        left=_,
                        op=Add(),
                        right=Name(id=nombre, ctx=Load())):
                            self.dict[nombre][1] = True
            # Si es una instancia tipo Expr
            elif isinstance(cuerpo, Expr):
                # Visitamos los value y buscamos una instancia Call
                if isinstance(cuerpo.value, Call):
                    # Recorremos los argumentos
                    for arg in cuerpo.value.args:
                        match arg:
                            # Si el argumento es del tipo Name - Load()
                            case Name(id=nombre, ctx=Load()):
                                self.dict[nombre][1] = True
        
        # Recorremos nuestro diccionario
        for key, values in self.dict.items():
            if not values[1]:
                self.addWarning('UnusedVariable', values[0], 'variable ' + key + ' has not been used')


class UnusedVariableTestRule(Rule):
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
