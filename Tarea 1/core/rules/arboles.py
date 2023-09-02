import ast

sourceCode ="""def test_x(self):
    x = 2
    y = True
    self.assertTrue(True)
    self.assertTrue(y)"""

print(ast.dump(ast.parse(sourceCode), indent=3))