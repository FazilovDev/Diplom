"""
Python code clone detector,
using Abstract Syntax Trees.
"""

import ast
import collections
import argparse
import itertools
from typing import Container
from models.algorithms.winnowing import *


class Position(ast.NodeVisitor):
    '''
    Find a clone position in the code (its line-span).
    Count child nodes.
    Найдите позицию клона в коде (его диапазон строк).
    Подсчитайте дочерние узлы.
    '''

    def init(self, clone):
        '''
        Lazy initialization.
        '''
        self.begin_line = self.end_line = clone.node.lineno
        self.node_count = 0
        self.generic_visit(clone.node)

    def visit(self, node):
        '''
        Find node's line and column span.
        '''
        if hasattr(node, 'lineno'):
            self.begin_line = min(self.begin_line, node.lineno)
            self.end_line = max(self.end_line, node.lineno)
            self.node_count += 1
            self.generic_visit(node)
            


class Clone(collections.namedtuple('Clone', 'node file position')):
    '''
    A set of code.
    '''

    def source(self, indent=''):
        '''
        Retrieve original source code
        Получить исходный исходный код..
        '''
        if not hasattr(self.position, 'begin_line'):
            self.position.init(self)
        lines = self.file.source[
            self.position.begin_line-1:self.position.end_line]
        return (self.position.begin_line, self.position.end_line,
                '\n'.join(indent + line.rstrip() for line in lines))


class Clones(list):
    '''
    A list of identical code snippets.
    Список идентичных фрагментов кода.
    '''

    def score(self):
        '''
        Provide a score for ordering clones while reporting.
        This sorts by number of nodes in the subtree, number
        of clones of the node, and code size.
        Укажите оценку для заказа клонов во время отчетности.
        Это сортирует по количеству узлов в поддереве, число
        клонов узла и размер кода.
        '''
        candidate = self[0]  # Pick the first clone.
        size = len(candidate.source()[-1])
        return (candidate.position.node_count, len(self), size)


class File:
    '''
    A source file.
    '''

    def __init__(self, name, source):
        '''
        Create a file with name and source-code.
        '''
        self.name = name
        self.source = source


def get_hash_from_gram(node):
    h = 0
    k = 273

    mod = 10 ** 9 + 7# 2**64
    m = 1
    for letter in node:
        x = ord(letter) - ord('a') + 1
        h = (h + m * x) % mod
        m = (m * k) % mod
    return h


def digest(node):
    '''
    Return an unambiguous string representation of a sub-tree in node.
    Emulates ast.dump(node, False).
    Возвращает однозначное строковое представление поддерева в узле.
    Эмулирует ast.dump(node, False).        
    '''
    if isinstance(node, ast.AST):
        if not hasattr(node, '_cached'):
            node._cached = '%s(%s)' % (node.__class__.__name__, ', '.join(
                digest(b) for a, b in ast.iter_fields(node)))
        return node._cached
    elif isinstance(node, list):
        return '[%s]' % ', '.join(digest(x) for x in node)
    return repr(node)


class Index(ast.NodeVisitor):
    '''
    A source code repository.
    '''

    def __init__(self, exclude):
        '''
        Create a new file indexer.
        '''
        self.nodes = collections.defaultdict(Clones)
        self.blacklist = frozenset(exclude)

    def add(self, file):
        '''
        Add a file to the index and parse it.
        '''
        source = open(file).readlines()
        tree = ast.parse(''.join(source))
        self._file = File(file, source)
        self.generic_visit(tree)

    def visit(self, node):
        '''
        Walk the Abstract Syntax Tree of a file.
        Convert each sub-tree to a string, which is used
        as a key in the clones dictionnary.
        '''
        if hasattr(node, 'lineno'):
            if node.__class__.__name__ not in self.blacklist:
                expr = digest(node)
                self.nodes[expr].append(
                    Clone(node, self._file, Position()))
        self.generic_visit(node)

    def clones(self):
        '''
        Returns a list of duplicate constructs.
        '''
        return sorted(((expr, nodes)
                       for expr, nodes in self.nodes.items() if len(nodes) > 1),
                      key=lambda n: n[1].score(), reverse=True)

def merge_lines_for_tree(lines):
    points = []
    start = 0
    end = 0
    for point in lines:
        if point[0] > start and point[1] < end:
            continue
        if point[0] > start:
            start = point[0]
            end = point[1]
            points.append([start, end])
            continue
        if point[0] < start:
            continue
        if point[1] > end:
            end = point[1]
            continue
        if point[1] <= end:
            continue
        start = point[0]
        end = point[1]
        points.append([start, end])
    return points



def get_clones(files):
    sources = Index('Name')
    for file in files:
        sources.add(file)
    
    res_files = dict()
    for expr, clones in sources.clones():
            if len(clones) >= 0:
                files = []
                for file, group in itertools.groupby(clones,
                                                    lambda clone: clone.file.name):
                    files.append(file)
                if len(files) < 2:
                    continue
                print("+%d repetitions of: %s ->" %
                    (len(clones), expr))
                for file, group in itertools.groupby(clones,
                                                    lambda clone: clone.file.name):
                    if file not in res_files.keys():
                        res_files[file] = list()
                    print("  - in %s" % file)
                    for clone in group:
                        begin, end, source = clone.source(' '*8)
                        if begin == end:
                            line = 'line %d' % begin
                            res_files[file].append([begin,begin])
                        else:
                            line = 'lines %d to %d' % (begin, end)
                            res_files[file].append([begin,end])
                        print('%s:\n%s' % (line, source))
    for file in res_files.keys():
        res_files[file] = sorted(res_files[file])
    return res_files

#f1 = 'Tests\\Python\\test1.py'
#f2 = 'Tests\\Python\\test2.py'
#get_clones([f1,f2])

def get_points_clones(files):
    clones = get_clones(files)
    for file in clones:
        clones[file]= merge_lines_for_tree(clones[file])
    return clones

def get_source_code_lines_from_file(filename):
    file = open(filename, 'r')
    code = file.readlines()
    file.close()
    return code


def get_str_from_list_code(list_code, start, end):
    if start == end:
        return list_code[start]
    res = ''
    for i in range(start, end):
        res += list_code[i]
    return res

def get_fragments_code(code, points):
    fragments = ''
    for i in range(len(points)):
        start = points[i][0]-1
        end = points[i][1]-1
        fragments += get_str_from_list_code(code, start, end)
    return fragments

def get_plag_combination(filename1, filename2, k, q, w, k2, q2, w2):
    fg = get_fingerprints(filename1, filename2, k, q, w)
    if fg[2] > 0.5:
        clones = get_points_clones([filename1, filename2])
        code1 = get_source_code_lines_from_file(filename1)
        code2 = get_source_code_lines_from_file(filename2)
        points1 = clones[filename1]
        points2 = clones[filename2]
        frag1 = get_fragments_code(code1, points1)
        frag2 = get_fragments_code(code2, points2)
        fg2 = get_fingerprints_no_file(frag1, frag2, k2, q2, w2)
        return [fg[2], fg2[2]]
    return None

'''
directory = '.\\Tests\\Python\\'
file1 = directory + 'test3.py'
file2 = directory + 'test2.py'

clones = get_clones([file1, file2])
#print(get_points_clones([file1, file2]))
code1 = get_source_code_lines_from_file(file1)
code2 = get_source_code_lines_from_file(file2)
points1 = get_points_clones([file1, file2])[file1]
points2 = get_points_clones([file1,file2])[file2]
frag1 = get_fragments_code(code1, points1)
frag2 = get_fragments_code(code2, points2)
fg = get_fingerprints(file1, file2, 7, 703, 4)
fg2 = get_fingerprints_no_file(frag1, frag2, 7, 703, 4)
print(fg)
print(fg2)
print(len(points1) / len(code1))
get_plag_combination(file1, file2, 7, 703, 4)


if __name__ == '__main__':
    import argparse
    import itertools

    # Parse command-line arguments.
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('files',
                      metavar='FILE', nargs='+',
                      help='set of Python files to check for duplicate code')
    args.add_argument('--ignore', '-i',
                      metavar='NODE', nargs='+', default=['Name'],
                      help='skip some syntactic constructs (default: Name)')
    args.add_argument('--min', '-m',
                      metavar='N', type=int, default=0,
                      help='report items duplicated at least N times')
    input = args.parse_args()

    # Process files.
    sources = Index(input.ignore)
    for file in input.files:
        sources.add(file)

    # Report clones.
    for expr, clones in sources.clones():
        if len(clones) >= input.min:
            print("+%d repetitions of: %s ->" %
                  (len(clones), expr))
            for file, group in itertools.groupby(clones,
                                                 lambda clone: clone.file.name):
                print("  - in %s" % file)
                for clone in group:
                    begin, end, source = clone.source(' '*8)
                    if begin == end:
                        line = 'line %d' % begin
                    else:
                        line = 'lines %d to %d' % (begin, end)
                    print('%s:\n%s' % (line, source))
'''