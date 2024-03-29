import ast
from models.preprocessing.cleantext import *
from models.algorithms.winnowing import get_text_from_file
from models.algorithms.ast_algorithm.astt import detect
def as_tree(node, indent="  "):
    """
    Returns an eval-able string representing a node tree.
    The result is the same as given by `ast.dump()`,
    except that the elements of the tree are put on separate lines
    and indented with `indent`s so that the whole tree is more human-readable.
    """
    visitor = ASTPrinter(indent)
    visitor.visit(node)
    return visitor.dumps()


class ASTPrinter(ast.NodeVisitor):

    def __init__(self, indent):
        self.result = []
        self.indentation = 0
        self.indent_with = indent

    def dumps(self):
        return "".join(self.result)

    def write(self, text):
        self.result.append(text)

    def generic_visit(self, node):

        if isinstance(node, list):
            nodestart = "["
            nodeend = "]"
            children = [("", child) for child in node]
        else:
            nodestart = type(node).__name__ + "("
            nodeend = ")"
            children = sorted(
                [(name + "=", value) for name, value in ast.iter_fields(node)])

        if len(children) > 1:
            self.indentation += 1

        self.write(nodestart)
        for i, pair in enumerate(children):
            attr, child = pair
            if len(children) > 1:
                self.write("\n" + self.indent_with * self.indentation)
            if isinstance(child, (ast.AST, list)):
                self.write(attr)
                self.visit(child)
            else:
                self.write(attr + repr(child))

            if i != len(children) - 1:
                self.write(",")
        self.write(nodeend)

        if len(children) > 1:
            self.indentation -= 1
string_types = str


file1 = 'Tests\\set\\first_lab_Avakyan.py'
file2 = 'Tests\\set\\first_lab_Avakyan.py'
tokens = tokenize(file1)
tree1 = ast.parse(get_text_from_file(file1))
tree2 = ast.parse(get_text_from_file(file1))

try:
    detect([get_text_from_file(file1),get_text_from_file(file1)])
except:
    pass