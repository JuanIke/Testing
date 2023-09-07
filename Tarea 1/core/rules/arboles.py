import ast

print(" ")
print("------------Código 1A --------------")
print(" ")
sourceCode1 = """def test(self):
                    x = 3
                    self.assertEquals(x,2)"""
print(ast.dump(ast.parse(sourceCode1), indent=4))

print(" ")
print("------------Código 1D --------------")
print(" ")
sourceCode = """def test(self):
                    self.assertEquals(3,2)"""
print(ast.dump(ast.parse(sourceCode), indent=3))

print(" ")
print("-----------Código 2A -----------")
print(" ")
sourceCode2 ="""def test(self):
                    x = complex_method()
                    self.assertEquals(x,2)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 2D -----------")
print(" ")
sourceCode2 ="""def test(self):
                    self.assertEquals(complex_method(),2)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 3A -----------")
print(" ")
sourceCode2 ="""def test(self):
                    x = complex_method()
                    y = x + 2
                    self.assertEquals(y,2)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 3D -----------")
print(" ")
sourceCode2 ="""def test(self):
                    self.assertEquals(complex_method() + 2,2)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 4A -----------")
print(" ")
sourceCode2 ="""def test(self):
                    x = complex_method()
                    y = x + 2
                    z = x + y
                    self.assertEquals(z,2)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 4D -----------")
print(" ")
sourceCode2 ="""def test(self):
                    x = complex_method()
                    self.assertEquals(x + (x + 2), 2)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))
