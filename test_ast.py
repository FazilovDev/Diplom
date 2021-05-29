import ast
import collections
import argparse
import itertools
from typing import Container

def get_source_code_from_file(filename):
    file = open(filename, 'r')
    code = file.read()
    file.close()
    return code

def digest(node):
    '''
    Return an unambiguous string representation of a sub-tree in node.
    Emulates ast.dump(node, False).
    '''
    if isinstance(node, ast.AST):
        if not hasattr(node, '_cached'):
            node._cached = '%s(%s)' % (node.__class__.__name__, ', '.join(
                digest(b) for a, b in ast.iter_fields(node)))
        return node._cached
    elif isinstance(node, list):
        return '[%s]' % ', '.join(digest(x) for x in node)
    return repr(node) 

file = 'Tests\\Python\\test5.py'
tree = ast.parse(get_source_code_from_file(file))
for children in ast.iter_child_nodes(tree):
    for ch in ast.iter_child_nodes(children):
        print(digest(ch))