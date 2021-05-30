from models.preprocessing.cleantext import *

class Gram:
    def __init__(self, text, hash_gram, start_pos, end_pos):
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

def get_hash_from_gram1(gram, q):
    h = 0
    k = len(gram)
    for char in gram:
        x = int(ord(char)-ord('a') + 1)
        h = (h * k + x) % q
    return h

def get_hash_from_gram2(str,q):
     
    # P and M
    p = 31
    m = 1e9 + 9
    power_of_p = 1
    hash_val = 0
 
    # Loop to calculate the hash value
    # by iterating over the elements of string
    for i in range(len(str)):
        hash_val = ((hash_val + (ord(str[i]) -
                                 ord('a') + 1) *
                              power_of_p) % m)
 
        power_of_p = (power_of_p * p) % m
 
    return int(hash_val)

def get_hash_from_gram(gram, q):
    h = 0
    k = 273

    mod = 10 ** 9 + 7# 2**64
    m = 1
    for letter in gram:
        x = ord(letter) - ord('a') + 1
        h = (h + m * x) % mod
        m = (m * k) % mod
    return h


import hashlib

def get_hash_from_gram1(gram, q):
    hashval = hashlib.sha1(gram.encode('utf-8'))
    hashval = hashval.hexdigest()[-4 :]
    hashval = int(hashval, 16)  #using last 16 bits of sha-1 digest
    return hashval


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
    #print(token)
    for i in range(len(fp1)):
        for j in range(i, len(fp2)):
            if fp1[i] == fp2[j]:
                #print('i: {0} j:{1} fp1:{2} fp2:{3}'.format(i,j,fp1[i],fp2[j]))
                flag = 0
                startx = endx = None
                match = hashes.index(fp1[i])
                newStart = grams[match].start_pos
                newEnd = grams[match].end_pos

                #print('newStart:{0} newEnd:{1}'.format(newStart,newEnd))
                
                for k in token:
                    if k[2] == newStart:
                        #print('token: {0} newStart: {1}'.format(k[2], newStart))
                        startx = k[1]
                        flag = 1
                    if k[2] == newEnd:
                        #print('token: {0} newEnd: {1}'.format(k[2], newEnd))
                        endx = k[1]
                newEnd = k
                if flag == 1 and endx != None:
                    points.append([startx, endx])
                
                #points.append([newStart, newEnd])
    points.sort(key = lambda x: x[0])
    points = points[1:]
    #print('points = ',points)
    return points

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
                    elif k[2] == newEnd:
                        endx = k[1]
                if flag == 1 and endx != None:
                    points.append([startx, endx])
    points.sort(key = lambda x: x[0])
    points = points[1:]
    #print('points = ',points)
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
    #print('merged = ', mergedPoints)
    return mergedPoints

def distance_simpson(A, B):
    res = []
    a = set(A)
    b = set(B)
    return len(a.intersection(b)) / min(len(a), len(b))


def get_fingerprints(file1, file2, k, q, w):

    token1 = tokenize(file1)
    token2 = tokenize(file2)

    text1proc = toText(token1)
    text2proc = toText(token2)

    grams1 = get_k_grams_from_text(text1proc, k, q)
    grams2 = get_k_grams_from_text(text2proc, k, q)


    hashes1 = get_hashes_from_grams(grams1)
    hashes2 = get_hashes_from_grams(grams2)


    #print('hashes: {0}'.format(hashes1))
    fp1 = winnow(hashes1, w)
    fp2 = winnow(hashes2, w)

    #print('fp1: {0}'.format(fp1))
    #print('fp2: {0}'.format(fp2))

    points1 = get_points(fp1, fp2, token1, hashes1, grams1)
    points2 = get_points(fp2, fp1, token2, hashes2, grams2)
    merged_points1 = get_merged_points(points1)
    merged_points2 = get_merged_points(points2)
    return (merged_points1, merged_points2, distance_simpson(fp1, fp2))

def get_fingerprints_no_file(code1, code2, k, q, w):

    token1 = tokenize_code(code1)
    token2 = tokenize_code(code2)

    text1proc = toText(token1)
    text2proc = toText(token2)

    grams1 = get_k_grams_from_text(text1proc, k, q)
    grams2 = get_k_grams_from_text(text2proc, k, q)



    hashes1 = get_hashes_from_grams(grams1)
    hashes2 = get_hashes_from_grams(grams2)


    #print('hashes: {0}'.format(hashes1))
    fp1 = winnow(hashes1, w)
    fp2 = winnow(hashes2, w)

    #print('fp1: {0}'.format(fp1))
    #print('fp2: {0}'.format(fp2))

    points1 = get_points(fp1, fp2, token1, hashes1, grams1)
    points2 = get_points(fp2, fp1, token2, hashes2, grams2)
    
    merged_points1 = get_merged_points(points1)
    merged_points2 = get_merged_points(points2)
    return (merged_points1, merged_points2, distance_simpson(fp1, fp2))


def get_fing(file1, file2, k, q, w):

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


    return (len(fp1))/len(hashes1), 2/(w+1)
