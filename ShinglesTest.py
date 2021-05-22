from models.algorithms.winnowing import get_text_from_file
from models.algorithms.Shingles import *
from models.preprocessing.cleantext import *
from strsimpy.qgram import QGram
from strsimpy.ngram import NGram
from strsimpy.metric_lcs import MetricLCS
from strsimpy.longest_common_subsequence import LongestCommonSubsequence
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from strsimpy.cosine import Cosine

file1 = 'Tests\\set\\first_lab_Avakyan.py'
file2 = 'Tests\\set\\lab-1-fedyashov.py'
text1 = toText(tokenize(file1))
text2 = toText(tokenize(file2))

tokens1 = toList(tokenize(file1))
tokens2 = toList(tokenize(file2))

shingle1 = ShingledText(tokens1)
shingle2 = ShingledText(tokens2)
print('Shingles: {}'.format(shingle1.similarity(shingle2)))

norm_levenshtein = NormalizedLevenshtein()
lcs = LongestCommonSubsequence()
ngram = NGram(5)
qgram = QGram(5)
lcs_metric = MetricLCS()
print('Levenshtein: {}'.format(norm_levenshtein.similarity(text1, text2)))
print('Longest Common Sub: {}'.format(lcs.distance(text1, text2)))
print('NGram: {}'.format(ngram.distance(text1,text2)))
print('QGram: {}'.format(qgram.distance(text1, text2)))
cosine = Cosine(5)
p0 = cosine.get_profile(text1)
p1 = cosine.get_profile(text2)
print('Cos: {}'.format(cosine.similarity_profiles(p0,p1)))
print('lcs metric: {}'.format(lcs_metric.distance(text1, text2)))

