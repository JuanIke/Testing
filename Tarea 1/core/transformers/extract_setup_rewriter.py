from _ast import ClassDef
from ast import *
import ast
from typing import Any
from core.rewriter import RewriterCommand


class ExtractSetupTransformer(NodeTransformer):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.ass = {}
        self.new_body = []


    def visit_ClassDef(self, node: ClassDef):
        NodeTransformer.generic_visit(self, node)

        # primero recolectar variables
        for def_de_funcion in node.body:
            if isinstance(def_de_funcion, FunctionDef):
                self.recolectar_variables(def_de_funcion.body)

        #realizar transformaciones
        for def_de_funcion in node.body:
            if isinstance(def_de_funcion, FunctionDef):
                self.transformaciones(def_de_funcion)

        self.crear_setup(node.body)
        return node
        
    # Recolectar variables
    def recolectar_variables(self, body):
        for cuerpo in body:
            match cuerpo:
                case Assign(
                targets=[
                    Name(id=id, ctx=Store())],
                value=Constant(value=value)):
                    if (str(id) in self.ass) and (self.ass[str(id)][0] == False):
                        self.ass[str(id)][0] = True
                    elif not(str(id) in self.ass):
                        self.ass[str(id)] = [False, value, id, False] # el 4to indica si es un call o no

                case Assign(
                    targets=[
                        Name(id=id, ctx=Store())],
                        value=Call(
                            func=Name(id=id2, ctx=Load()),
                            args=args,
                            keywords=[])):
                    if (str(id) in self.ass) and (self.ass[str(id)][0] == False):
                        self.ass[str(id)][0] = True
                    elif not(str(id) in self.ass):
                        self.ass[str(id)] = [False, False, id, True, id2, args] 
                    

        
    # hacer las transformaciones
    def transformaciones(self, node):
        if isinstance(node, FunctionDef):        
            new_body = []

            for cuerpo in range(len(node.body)):
                match node.body[cuerpo]:
                    case Expr(value=Call(
                        func=Attribute(
                            value=Name(id=id, ctx=Load()),
                            attr= nombre,
                            ctx=Load()),
                        args=args,
                        keywords= key)):
                        
                        new_args = []

                        for a in args:
                            if isinstance(a, Name):
                                if self.ass[str(a.id)][0]:
                                    new_args.append(ast.Attribute(value=Name(id='self', ctx=Load()),attr=a.id,ctx=Load()))
                                else:
                                    new_args.append(ast.Name(id=a.id, ctx=Load()))
                            elif isinstance(a, Constant):
                                new_args.append(ast.Constant(value=a.value))

                            elif isinstance(a, BinOp):
                                # primero left
                                if isinstance(a.left, Name):
                                    if self.ass[str(a.left.id)][0]:
                                        left = ast.Attribute(value=Name(id='self', ctx=Load()),attr=a.left.id,ctx=Load())
                                    else:
                                        left = ast.Name(id=a.left.id, ctx=Load())
                                elif isinstance(a.left, Constant):
                                    left = ast.Constant(value=a.left.value)
                                # segundo right
                                if isinstance(a.right, Name):
                                    if self.ass[str(a.right.id)][0]:
                                        right = ast.Attribute(value=Name(id='self', ctx=Load()),attr=a.right.id,ctx=Load())
                                    else:
                                        right = ast.Name(id=a.right.id, ctx=Load())
                                elif isinstance(a.right, Constant):
                                    right = ast.Constant(value=a.right.value)

                                new_args.append(ast.BinOp(left=left,op=a.op,right=right))

                            elif isinstance(a, Call):
                                if isinstance(a.func, Attribute):
                                    if isinstance(a.func.value, Name):
                                        if self.ass[str(a.func.value.id)][0] and self.ass[str(a.func.value.id)][3]:
                                            new_args.append(ast.Call(func=Attribute(value=Attribute(value=Name(id='self', ctx=Load()),attr=str(a.func.value.id),ctx=Load()),attr=str(a.func.attr),ctx=Load()),args=a.args,keywords=a.keywords))
                            

                        new_body.append(Expr(value=Call(
                            func=Attribute(
                                value=Name(id=id, ctx=Load()),
                                attr= nombre,
                                ctx=Load()),
                            args=new_args,
                            keywords= key)))

                    case Assign(
                targets=[
                    Name(id=id, ctx=Store())],
                value=Constant(value=value)):
                        if ("id" in self.ass) and (value == self.ass["id"][1]) and (not self.ass["id"][0]):
                            new_body.append(ast.Assign(
                                targets=[
                                    Name(id=id, ctx=Store())],
                                    value=Constant(value=value)))                       

            node.body = new_body

    # Recolectar variables
    def crear_setup(self, body):

        set_up_body = []

        for value in self.ass.values():
            if value[0] and not value[3]:
                set_up_body.append(ast.Assign(
                    targets=[
                        Attribute(
                            value=Name(id='self', ctx=Load()),
                            attr=value[2],
                            ctx=Store())],
                            value=Constant(value=value[1])))
                
            elif value[0] and value[3]:
                set_up_body.append(ast.Assign(
                    targets=[
                        Attribute(
                            value=Name(id='self', ctx=Load()),
                            attr=value[2],
                            ctx=Store())],
                            value=Call(
                                func=Name(id=value[4], ctx=Load()),
                                args=value[5],
                                keywords=[])))


        
        set_up = ast.FunctionDef(
               name='setUp',
               args=arguments(
                  posonlyargs=[],
                  args=[
                     arg(arg='self')],
                  kwonlyargs=[],
                  kw_defaults=[],
                  defaults=[]),
               body= set_up_body,
               decorator_list=[])
        
        body.insert(0, set_up)
         


        

class ExtractSetupCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, tree):
        new_tree = fix_missing_locations(ExtractSetupTransformer().visit(tree))
        return new_tree

    @classmethod
    def name(cls):
        return 'extract-setup'
    