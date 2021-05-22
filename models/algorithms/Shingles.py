from os import read
import mmh3
from nltk import ngrams
import random


def generate_random_seeds(n, seed=5):
    random.seed(seed)
    return random.sample(range(1, n + 1), n)


def minhash_similarity(minhash_a, minhash_b):
    match_count = 0
    for a_item, b_item in zip(minhash_a, minhash_b):
        if a_item == b_item:
            match_count += 1
    return match_count / len(minhash_a)

class ShingledText:
    def __init__(self, text, random_seed=5, shingle_length=5, minhash_size=200):
        split_text = text#.split()
        if len(split_text) < shingle_length:
            raise ValueError(u'input text is too short for specified shingle length of {}'.format(shingle_length))

        self.minhash = []
        self.shingles = ngrams(split_text, shingle_length)

        for hash_seed in generate_random_seeds(minhash_size, random_seed):
            min_value = float('inf')
            for shingle in ngrams(split_text, shingle_length):
                value = mmh3.hash(' '.join(shingle), hash_seed)
                min_value = min(min_value, value)
            self.minhash.append(min_value)

    def similarity(self, other_shingled_text):
        return minhash_similarity(self.minhash, other_shingled_text.minhash)

