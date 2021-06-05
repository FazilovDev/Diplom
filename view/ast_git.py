import ast
import collections
import itertools
from models.algorithms.winnowing import *


class Position(ast.NodeVisitor):
    def init(self, clone):
        self.begin_line = self.end_line = clone.node.lineno
        self.node_count = 0
        self.generic_visit(clone.node)

    def visit(self, node):
        if hasattr(node, 'lineno'):
            self.begin_line = min(self.begin_line, node.lineno)
            self.end_line = max(self.end_line, node.lineno)
            self.node_count += 1
            self.generic_visit(node)
            


class Clone(collections.namedtuple('Clone', 'node file position')):
    def source(self, indent=''):
        if not hasattr(self.position, 'begin_line'):
            self.position.init(self)
        lines = self.file.source[
            self.position.begin_line-1:self.position.end_line]
        return (self.position.begin_line, self.position.end_line,
                '\n'.join(indent + line.rstrip() for line in lines))


class Clones(list):
    def score(self):
        candidate = self[0]  # Pick the first clone.
        size = len(candidate.source()[-1])
        return (candidate.position.node_count, len(self), size)


class File:
    def __init__(self, name, source):
        self.name = name
        self.source = source


def digest(node):
    if isinstance(node, ast.AST):
        if not hasattr(node, '_cached'):
            node._cached = '%s(%s)' % (node.__class__.__name__, ', '.join(
                digest(b) for a, b in ast.iter_fields(node)))
        return node._cached
    elif isinstance(node, list):
        return '[%s]' % ', '.join(digest(x) for x in node)
    return repr(node)


class Index(ast.NodeVisitor):
    def __init__(self, exclude):
        self.nodes = collections.defaultdict(Clones)
        self.blacklist = frozenset(exclude)

    def add(self, file):
        source = open(file).readlines()
        tree = ast.parse(''.join(source))
        self._file = File(file, source)
        self.generic_visit(tree)

    def visit(self, node):
        if hasattr(node, 'lineno'):
            if node.__class__.__name__ not in self.blacklist:
                expr = digest(node)
                self.nodes[expr].append(
                    Clone(node, self._file, Position()))
        self.generic_visit(node)

    def clones(self):
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
