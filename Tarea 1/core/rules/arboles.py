import ast

print(" ")
print("------------Código 1 --------------")
print(" ")
sourceCode1 = """def test_x(self):
                    x = 2
                    y = 2
                    z = False
                    self.assertTrue(z)"""
print(ast.dump(ast.parse(sourceCode1), indent=4))

print(" ")
print("------------Código 2 --------------")
print(" ")
sourceCode = """def test_x(self):
                    x = 2
                    y = 3 + 2 * x
                    z = False
                    self.assertTrue(z)"""
print(ast.dump(ast.parse(sourceCode), indent=3))

print(" ")
print("-----------Código 3 -----------")
print(" ")
sourceCode2 ="""def test_x(self):
                    x = 2 
                    self.assertTrue(x)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 4 -----------")
print(" ")
sourceCode2 ="""class TestCase():
    def test_x(self):
        x = 2
        y = 2
        z = False
        self.assertTrue(z)

    def test_y(self):
        x = 2
        a = 3
        y = x + a
        z = False
        self.assertTrue(z)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))