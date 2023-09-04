import ast

print(" ")
print("------------Código 1 --------------")
print(" ")
sourceCode1 = """class TestX(TestCase):
    def test_x(self):
        x = 2
        y = 2
        self.assertEquals(x,y)
    def test_y(self):
        x = 2
        y = 2
        self.assertEquals(y,x)"""
print(ast.dump(ast.parse(sourceCode1), indent=4))

print(" ")
print("------------Código 2 --------------")
print(" ")
sourceCode = """class TestX(TestCase):
    def test_x(self):
        x = 2
        y = 2
        z = 5
        self.assertEquals(x,y)
    def test_y(self):
        x = 2
        g = 2
        z = 5
        f = 5
        self.assertEquals(y,x)"""
print(ast.dump(ast.parse(sourceCode), indent=3))

print(" ")
print("-----------Código 3 -----------")
print(" ")
sourceCode2 ="""class TestX(TestCase):
    def test_x(self):
        x = 1
        y = 2
        z = 5
        self.assertEquals(x,y)
    def test_y(self):
        x = 2
        g = 2
        z = 5
        f = 5
        self.assertEquals(y,x)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))

print(" ")
print("-----------Código 4 -----------")
print(" ")
sourceCode2 ="""class TestX(TestCase):
    def test_x(self):
        x = 5
        g = 3
        z = 1
        f = "a"
        self.assertEquals(z,f)
    def test_y(self):
        x = 5
        g = 3
        z = 1
        f = "a"
        self.assertEquals(z,f)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))
print(" ")
print("-----------Código 5 -----------")
print(" ")
sourceCode2 ="""class TestX(TestCase):
    def test_x(self):
        x = 5
        g = 3
        self.assertEquals(x,5)
    def test_y(self):
        x = 5
        g = 3
        self.assertEquals(g,3)
    def test_z(self):
        x = 5
        g = 3
        f = "a"
        self.assertEquals(x+g,8)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))
print(" ")
print("-----------Código 6 -----------")
print(" ")
sourceCode2 ="""
class TestX(TestCase):
    def test_x(self):
        y = 5
        h = 3
        self.assertEquals(y,5)
    def test_y(self):
        x = 5
        g = 3
        self.assertEquals(g,3)
    def test_z(self):
        x = 5
        g = 3
        f = "a"
        self.assertEquals(x+g,8)"""
print(ast.dump(ast.parse(sourceCode2), indent=3))
