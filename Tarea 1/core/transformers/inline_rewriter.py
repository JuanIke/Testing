from ast import *
import ast
from typing import Any
from core.rewriter import RewriterCommand

class InLineTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()
        self.variables = {} # {variable: [Node, uses]}
        self.expr = {} # {variable: Expr}
        self.used = set() # [variable]
        self.returns = [] # [Node]

    def visit_FunctionDef(self, node):
        print("\n")
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
                        # Recuperamos el nodo
                        newNode = cuerpo
                        # Recorremos las variables creadas para buscar la que está dentro de BinOp
                        for keyVariables in self.variables.keys():
                            # Si la encontramos
                            if keyVariables == variableExpr:
                                # Subimos en 1 los usos de la variable
                                self.variables[variableExpr][1] += 1
                        # Guardamos variable creada y nodo asignación
                        self.variables[variableName] = [newNode, 0]
                        # Guardamos la variable usada
                        self.used.add(variableExpr)
                    
                    # Asignación de BinOp - Variable usada en right
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=BinOp(
                                left=Constant(value=_)),
                                op=_,
                                right=Name(id=variableExpr, ctx=Load())):
                        # Recuperamos el nodo
                        newNode = cuerpo
                        # Recorremos las variables creadas para buscar la que está dentro de BinOp
                        for keyVariables in self.variables.keys():
                            # Si la encontramos
                            if keyVariables == variableExpr:
                                # Subimos en 1 los usos de la variable
                                self.variables[variableExpr][1] += 1
                        # Guardamos variable creada y nodo asignación
                        self.variables[variableName] = [newNode, 0]
                        # Guardamos la variable usada
                        self.used.add(variableExpr)

                    # Asignación de BinOp - Variables en right y left
                    case Assign(
                            targets=[
                                Name(id=variableName, ctx=Store())],
                            value=BinOp(
                                left=Name(id=variableExpr1, ctx=Load()),
                                op=_,
                                right=Name(id=variableExpr2, ctx=Load()))):
                        # Si la encontramos
                        newNode = cuerpo
                        # Recorremos las variables creadas para buscar la que está dentro de BinOp
                        for keyVariables in self.variables.keys():
                            if keyVariables == variableExpr1:
                                # Subimos en 1 los usos de la variable
                                self.variables[variableExpr1][1] += 1
                            elif keyVariables == variableExpr2:
                                # Subimos en 1 los usos de la variable
                                self.variables[variableExpr2][1] += 1
                        # Guardamos variable creada y nodo asignación
                        self.variables[variableName] = [newNode, 0]
                        # Guardamos las variables usadas
                        self.used.add(variableExpr1)
                        self.used.add(variableExpr2)

            # Revisamos las expresiones
            elif isinstance(cuerpo, Expr):
                # Para cada argumento de la expresión
                for arg in cuerpo.value.args:
                    match arg:
                        # Un argumento es una variable
                        case Name(id=variableExpr, ctx=Load()):
                            # Guardamos la variable usada
                            self.used.add(variableExpr)
                            # Aumentamos en 1 los usos de la variable
                            self.variables[variableExpr][1] += 1
                            # Guardamos el nodo
                            self.expr[variableExpr] = cuerpo


        # Ordenamos las variables usadas (No extensible)
        sortedUsedVars = sorted(list(self.used))
        # Recorremos las variables usadas
        for variableUsed in sortedUsedVars:
            for variableKey, variableValues in self.variables.items():

                # Buscamos que la variable tenga justo 1 uso
                if variableUsed == variableKey and variableValues[1] == 1:
                    if isinstance(variableValues[0], Assign):
                        match variableValues[0]:

                            # BinOp con var en left
                            case Assign(
                                    targets=[
                                        Name(id=varName, ctx=Store())],
                                    value=BinOp(
                                        left=Name(id=varExpr, ctx=Load()),
                                        op=_,
                                        right=Constant(value=_))):
                                for varKey, varVal in self.variables.items():
                                    if varKey == varExpr and varVal[1] == 1:
                                        variableValues[0].value.left = varVal[0].value
                                        break
                            
                            # BinOp con var en right
                            case Assign(
                                    targets=[
                                        Name(id=varName, ctx=Store())],
                                    value=BinOp(
                                        left=Constant(value=_),
                                        op=_,
                                        right=Name(id=varExpr, ctx=Load()))):
                                for varKey, varVal in self.variables.items():
                                    if varKey == varExpr and varVal[1] == 1:
                                        variableValues[0].value.right = varVal[0].value
                                        break
                            
                            #BinOp con dos var
                            case Assign(
                                    targets=[
                                        Name(id=varName, ctx=Store())],
                                    value=BinOp(
                                        left=Name(id=varLeft, ctx=Load()),
                                        op=_,
                                        right=Name(id=varRight, ctx=Load()))):
                                for varKey, varVal in self.variables.items():
                                    if varKey == varLeft and varVal[1] == 1:
                                        variableValues[0].value.left = varVal[0].value
                                        break
                                for varKey, varVal in self.variables.items():
                                    if varKey == varRight and varVal[1] == 1:
                                        variableValues[0].value.right = varVal[0].value
                                        break
                                

                # Buscamos que la variable tenga más de un uso
                if variableUsed == variableKey and variableValues[1] > 1:
                    if isinstance(variableValues[0], Assign):
                        # Agregamos el nodo a los devueltos
                        self.returns.append(variableValues[0])

        for variableUsed, exprNode in self.expr.items():
            for variableKey, variableValues in self.variables.items():
                if exprNode.value.args[0].id == variableKey and variableValues[1] == 1:
                    retNode = exprNode
                    retNode.value.args[0] = variableValues[0].value
                    print(ast.dump(parse(retNode)))
                    self.returns.append(retNode)


        node.body = [self.returns]
        return node
                

class InlineCommand(RewriterCommand):   
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, tree):
        new_tree = fix_missing_locations(InLineTransformer().visit(tree))
        return new_tree 