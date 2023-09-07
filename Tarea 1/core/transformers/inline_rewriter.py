from _ast import FunctionDef
from ast import *
from typing import Any
from core.rewriter import RewriterCommand

class InLineTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()
        self.variables = {}
        self.used = {}
        self.returns = []

    def visit_FunctionDef(self, node):
        NodeTransformer.generic_visit(self, node)
        for cuerpo in node.body:

             # Revisamos las Asignaciones
            if isinstance(cuerpo, Assign):
                match cuerpo:
                    # Asignación de constante
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=Constant(value=variableValue)):
                        # Guardamos variable nueva y su nodo
                        self.variables[variableName] = [cuerpo, 0]

                    # Asignación de función
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=Call(
                                func=Name(id=functionName, ctx=Load()),
                                args=[],
                                keywords=[])):
                        # Guardamos variable nueva y su nodo
                        self.variables[variableName] = [cuerpo, 0]

                    # Asignación de BinOp - Variable usada en left
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=BinOp(
                                left=Name(id=variableExpr, ctx=Load()),
                                op=_,
                                right=Constant(value=_))):
                        # Recorremos las variables creadas para buscar la que está dentro de BinOp
                        for keyVariables, valuesVariable in self.variables.items():
                            # Si la encontramos
                            if keyVariables == variableExpr:
                                # Lado izquierdo del BinOp será el value de la variable ya creada
                                newNode = cuerpo
                                newNode.value.left = valuesVariable[0].value
                        # Guardamos variable creada y nodo asignación
                        self.variables[variableName] = [newNode, 0]
                        # Si la variable no ha sido usada
                        # Subimos en 1 los usos de la variable
                        self.variables[variableExpr][1] += 1
                        # Guardamos el nodo Assign modificado en used
                        self.used[variableExpr] = newNode
                    
                    # Asignación de BinOp - Variable usada en right
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=BinOp(
                                left=Constant(value=_)),
                                op=_,
                                right=Name(id=variableExpr, ctx=Load())):
                        # Recorremos las variables creadas para buscar la que está dentro de BinOp
                        for keyVariables, valuesVariable in self.variables.items():
                            # Si la encontramos
                            if keyVariables == variableExpr:
                                # Lado derecho del BinOp será el value de la variable ya creada
                                newNode = cuerpo
                                newNode.value.right = valuesVariable[0].value
                        # Guardamos variable creada y nodo asignación
                        self.variables[variableName] = [newNode, 0]
                        # Si la variable no ha sido usada
                        # Subimos en 1 los usos de la variable
                        self.variables[variableExpr][1] += 1
                        # Guardamos el nodo Assign modificado en used
                        self.used[variableExpr] = newNode
                    
                    # Asignación de BinOp - Variables en right y left
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=BinOp(
                                left=Name(id=variableExpr1, ctx=Load())),
                                op=_,
                                right=Name(id=variableExpr2, ctx=Load())):
                        # Recorremos las variables creadas para buscar la que está dentro de BinOp
                        for keyVariables, valuesVariable in self.variables.items():
                            # Si la encontramos
                            newNode1 = cuerpo
                            if keyVariables == variableExpr1:
                                newNode1.value.left = valuesVariable[0].value
                            elif keyVariables == variableExpr2:
                                newNode1.value.right = valuesVariable[0].value
                        # Guardamos variable creada y nodo asignación
                        self.variables[variableName] = [newNode1, 0]
                        # Si la variable no ha sido usada
                        # Subimos en 1 los usos de la variable 1
                        self.variables[variableExpr1][1] += 1
                        # Subimos en 1 los usos de la variable 2
                        self.variables[variableExpr2][1] += 1
                        # Guardamos el nodo Assign modificado en used
                        self.used[variableExpr1] = newNode1

            # Revisamos las expresiones
            elif isinstance(cuerpo, Expr):
                # Para cada argumento de la expresión
                for arg in cuerpo.value.args:
                    match arg:
                        # Un argumento es una variable
                        case Name(id=variableExpr, ctx=Load()):
                            # Guardamos la variable usada y su nodo
                            self.used[variableExpr] = cuerpo
                            # Aumentamos en 1 los usos de a variable
                            self.variables[variableExpr][1] += 1

        # Recorremos el diccionario
        for keyVariables, valuesVariable in self.variables.items():
            for keyUsed, valuesUsed in self.used.items():
                # Si la variable está siendo usada
                if keyVariables == keyUsed:
                    if isinstance(valuesUsed, Expr):
                        # Si el primer argumento es una variable o función
                        if isinstance(valuesUsed.value.args[0], Name):
                            # Guardamos el nodo usado
                            newNode = valuesUsed
                            # Cambiamos el argumento
                            newNode.value.args[0] = valuesVariable[0].value
                            # Agregamos el nodo nuevo a returns
                            self.returns.append(newNode)
                    if isinstance(valuesUsed, Assign):
                        pass
                        if valuesUsed.targets[0].id in self.used.keys():
                            pass
                        # Si se asignó a algo que no está siendo usado, entonces
                        else:
                            pass
                        
        print("Variables:", self.variables)
        print("Used:", self.used)
        node.body = [self.returns]
        return node
                

class InlineCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, tree):
        new_tree = fix_missing_locations(InLineTransformer().visit(tree))
        return new_tree
