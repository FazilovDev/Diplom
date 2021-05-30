import models.algorithms.AST as ast
import astunparse
from models.algorithms.winnowing import *

#file1 = 'Tests\\Python\\test6.py'
#file2 = 'Tests\\Python\\test7.py'
#file3 = 'Tests\\set\\first_lab_Avakyan.py'

def get_plag_combination_with_ast(filename1, filename2, k, q, w, k2, q2, w2):
    fg = get_fingerprints(filename1, filename2, k, q, w)
    if fg[2] > 0.5:
        plag, text1, text2 = ast.get_source_code_from_ast_detect(filename1, filename2)
        frag1 = ''.join(text1)
        frag2 = ''.join(text2)
        fg2 = get_fingerprints_no_file(frag1, frag2, k2, q2, w2)
        combRes = fg[2]

        return [fg[2], combRes]
    return [fg[2], 0]

#print(get_plag_combination1(file1,file2, 7,277,5,5,703,3))
'''
def get_source_code_from_file(filename):
    file = open(filename, 'r')
    code = file.read()
    file.close()
    return code
pycode_string = get_source_code_from_file(file1)
#results = ast.detect([pycode_string, pycode_string], diff_method=ast.TreeDiff, keep_prints=False, module_level=False)

#import ast
#my_tree = ast.parse(pycode_string)
#print(astunparse.dump(my_tree))

from models.algorithms.winnowing import *

token1 = tokenize(file1)
text1proc = toText(token1)
token2 = tokenize(file2)
text2proc = toText(token2)
#token3 = tokenize(file3)
#text3proc = toText(token3)


k = 5
q = 2**64
w = 4
#get_fingerprints(file1, text3proc, k, q, w)

from strsimpy.qgram import QGram

qgram = QGram(5)
print(qgram.distance(text1proc, text2proc))

#print(text1proc)
s = 'abrakadabra'

from strsimpy.normalized_levenshtein import NormalizedLevenshtein
norm = NormalizedLevenshtein()
print(norm.similarity(text1proc, text2proc))


s = 'abrakadabra'
token1 = tokenize(file1)
text1proc = toText(token1)
grams1 = get_k_grams_from_text(text1proc, 8, 2**10)

#get_fingerprints(file1, file1,8,1,3)#8

from math import *
kl = [i for i in range(1, 21)]
wl = [i for i in range(1, 16)]

for k in kl:
    for w in wl:
        d, nd = get_fing(file1, file2, k, 259, w)
        if abs(d-nd) < 1e-7:
            print('k:{0}, w:{1}\n{2} = {3}'.format(k,w,d,nd))
'''