import ast

class ASTChecker(ast.NodeVisitor):
    """
    Basic AST checker to detect forbidden patterns.
    You can expand this later if you add more tasks.
    """

    def __init__(self):
        self.found_imports = []
        self.found_literals = []

    def visit_Import(self, node):
        for alias in node.names:
            self.found_imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.found_imports.append(node.module)
        self.generic_visit(node)

    def visit_Constant(self, node):
        # Track literal numbers or strings
        if isinstance(node.value, (int, float, str)):
            self.found_literals.append(node.value)
        self.generic_visit(node)


def analyze_source(source_code: str):
    """
    Parse the source code and return an ASTChecker result.
    """
    tree = ast.parse(source_code)
    checker = ASTChecker()
    checker.visit(tree)
    return checker