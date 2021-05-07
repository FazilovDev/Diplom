from models.preprocessing.cleantext import *

class Gram:
    def __init__(self, path_to_file, text, hash_gram, start_pos, end_pos):
        self.path_to_file = path_to_file
        self.text = text
        self.hash = hash_gram
        self.start_pos = start_pos
        self.end_pos = end_pos


def get_text_from_file(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()
    return text

def get_text_processing(text):
    stop_symbols = [' ', ',']
    return ''.join(j for j in text if not j in stop_symbols)

def get_hash_from_gram(gram, q):
    h = 0
    k = len(gram)
    for char in gram:
        x = int(ord(char)-ord('a') + 1)
        h = (h * k + x) % q
    return h

def get_k_grams_from_text(text, k = 25, q = 31):
    grams = []
    for i in range(0, len(text)-k+1):
        hash_gram = get_hash_from_gram(text[i:i+k], q)
        gram = Gram(text[i:i+k], hash_gram, i, i+k)
        grams.append(gram)
    return grams


def get_hashes_from_grams(grams):
    hashes = []
    for gram in grams:
        hashes.append(gram.hash)
    return hashes

def min_index(window):
    min_ = window[0]
    min_i = 0
    for i in range(len(window)):
        if window[i] < min_:
            min_ = window[i]
            min_i = i
    return min_i

def winnow(hashes, w):
    n = len(hashes)
    prints = []
    windows = []
    prev_min = 0
    current_min = 0
    for i in range(n - w):
        window = hashes[i:i+w]
        windows.append(window)
        current_min = i + min_index(window)
        if not current_min == prev_min:
            prints.append(hashes[current_min])
            prev_min = current_min
    return prints

def get_points(fp1, fp2, token, hashes, grams):
    points = []
    for i in fp1:
        for j in fp2:
            if i == j:
                flag = 0
                startx = endx = None
                match = hashes.index(i)
                newStart = grams[match].start_pos
                newEnd = grams[match].end_pos

                for k in token:
                    if k[2] == newStart: 
                        startx = k[1]
                        flag = 1
                    if k[2] == newEnd:
                        endx = k[1]
                if flag == 1 and endx != None:
                    points.append([startx, endx])
    points.sort(key = lambda x: x[0])
    points = points[1:]
    return points

def get_merged_points(points):
    mergedPoints = []
    mergedPoints.append(points[0])
    for i in range(1, len(points)):
        last = mergedPoints[len(mergedPoints) - 1]
        if points[i][0] >= last[0] and points[i][0] <= last[1]:
            if points[i][1] > last[1]:
                mergedPoints = mergedPoints[: len(mergedPoints)-1]
                mergedPoints.append([last[0], points[i][1]])
            else:
                pass
        else:
            mergedPoints.append(points[i])
    return mergedPoints

def get_fingerprints(file1, file2, k, q, w):

    token1 = tokenize(file1)
    token2 = tokenize(file2)

    text1proc = toText(token1)
    text2proc = toText(token2)

    grams1 = get_k_grams_from_text(text1proc, k, q)
    grams2 = get_k_grams_from_text(text2proc, k, q)

    hashes1 = get_hashes_from_grams(grams1)
    hashes2 = get_hashes_from_grams(grams2)

    fp1 = winnow(hashes1, w)
    fp2 = winnow(hashes2, w)

    points1 = get_points(fp1, fp2, token1, hashes1, grams1)
    points2 = get_points(fp1, fp2, token2, hashes2, grams2)
    
    merged_points1 = get_merged_points(points1)
    merged_points2 = get_merged_points(points2)
    return (merged_points1, merged_points2)


path_to_test = 'Tests\\fazilov\\OMPBegin19.cpp'
def get_text_from_file(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()
    return text
def get_text_fingers(text, stopwords, k):
    H = []
    for loc in range(0, len(text)-k):
        length = k
        kgram = text[loc:loc+length]
        while len(kgram) < k:
            length = length + (k-len(kgram))
            kgram = text[loc:loc+length]
            kgram.replace(kgram, stopwords,'')
        H.append([kgram, loc, length])
    return H

def str_replace(text, stopwords):
    for word in stopwords:
        text = text.replace(word, '') 

def fingerprint_extraction(filename, text, stopwords, k, q):
    h = list()
    for i in range(0, len(text)-k):
        ln = k
        kgram = text[i:i+ln]
        #kgram = str_replace(kgram, stopwords)
        while len(kgram) < k:
            ln = ln + (k-len(kgram))
            kgram = text[i:i+ln]
            #kgram = str_replace(kgram, stopwords)
        hhash = get_hash_from_gram(kgram, q)
        h.append(Gram(filename, kgram, hhash, i,i+ln))
    return h

def extended_winnowing(H, t, k):
    w = t + 1 - k
    n = len(H)
    min_i = -1
    premin_index = -1
    HS = list()
    for i in range(0, len(H)-w):
        tmp_min = H[i].hash
        for j in range(i, i+w):
            if H[j].hash <= tmp_min:
                min_i = j
                tmp_min = H[j].hash
        if min_i != premin_index:
            premin_index = min_i
            HS.append(H[min_i])
    return HS

def get_merged_points(points):
    mergedPoints = []
    mergedPoints.append(points[0])
    for i in range(1, len(points)):
        last = mergedPoints[len(mergedPoints) - 1]
        if points[i].hash >= last.hash and points[i][0] <= last[1]:
            if points[i][1] > last[1]:
                mergedPoints = mergedPoints[: len(mergedPoints)-1]
                mergedPoints.append([last[0], points[i][1]])
            else:
                pass
        else:
            mergedPoints.append(points[i])
    return mergedPoints

def finger(file1, file2, k, q, t):

    token1 = tokenize(file1)
    token2 = tokenize(file2)

    text1proc = toText(token1)
    text2proc = toText(token2)

    fp1 = fingerprint_extraction(file1, text1proc, [' ',','], k, q)
    fp2 = fingerprint_extraction(file2, text2proc, [' ', ','], k, q)

    points1 = extended_winnowing(fp1, t, k)
    points2 = extended_winnowing(fp2, t, k)

    merged_points1 = get_merged_points(points1)
    merged_points2 = get_merged_points(points2)
    return (merged_points1, merged_points2)

filename1 = 'Tests\\fazilov\\OMPBegin19.cpp'
filename2 = 'Tests\\fazilov\\OMPBegin22.cpp'
#points = finger(filename1, filename2, 5, 971, 10)

fp = fingerprint_extraction(filename1, toText(tokenize(filename1)), [' ', ','], 5, 971)
points = extended_winnowing(fp, 10, 5)

