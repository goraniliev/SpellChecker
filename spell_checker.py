# -*- coding: utf-8 -*-
import time

__author__ = 'goran'

# text_path = '/home/goran/Desktop/data/dataset-hw.txt'

text_path = '../../Domasni/dataset-hw.txt'
separated_words_path = '../dataset.txt'
all_words_path = '../all_words.txt'

def extract(line):
    word = []
    words = []

    for c in line:
        if c.isalpha():
            word.append(c)
        elif word:
                words.append(''.join(word).lower())
                word = []

    if word:
        words.append(''.join(word).lower())

    return words


def train(features):
    model = {}

    for f in features:
        model[f] = model.get(f, 1) + 1

    return model


def get_words(path=separated_words_path):
    words = []
    with open(path, 'r') as fin:
        for line in fin:
            category, content = line.split('\t')
            words += content.split(' ')

    return words

def transform_dataset(path=text_path, res_path=separated_words_path):
    # create empty file
    open(res_path, 'w').close()

    with open(path, 'r') as fin:
        with open(res_path, 'a') as fout:
            for line in fin:
                try:
                    category, content = line.decode('utf-8').split('\t')
                except ValueError:
                    print line
                    break
                fout.write(category + '\t' + ' '.join(extract(content.decode('utf-8'))).encode('utf-8') + '\n')


def all_words_toghether(path=all_words_path):
    words = get_words()
    with open(path, 'w') as fout:
        fout.write(' '.join(words))


def get_all_words(path=all_words_path):
    with open(path, 'r') as fin:
        words = fin.read().decode('utf-8').split(' ')
    return words
# start = time.time()
# transform_dataset()
# end = time.time()

# 108.331707954 fout ako ja otvaram i zatvaram cesto
# 92.1931741238 fout ako ja otvoram porano
# print end - start

# all_words_toghether()


alphabet = 'abcdefgh'

def levenshtein(x, y):
    M = len(x)
    N = len(y)

    MAX = 100000000000

    dp = [[MAX for i in xrange(N + 1)] for j in xrange(M + 1)]

    dp[0] = [j for j in xrange(N + 1)]
    for i in xrange(M + 1):
        dp[i][0] = i

    for i in xrange(1, M + 1):
        for j in xrange(1, N + 1):
            dp[i][j] = min(min(dp[i - 1][j], dp[i][j - 1]) + 1, dp[i - 1][j - 1] + (0 if x[i - 1] == y[j - 1] else 2))

    # for row in dp:
    #     print '\t'.join([str(i) for i in row])

    return dp[M][N]

s = time.time()
words = get_all_words()
e = time.time()
print 'Words loaded from file in %f seconds' %(e - s)
unique_words = set(words)
s = time.time()
model = train(words)
e = time.time()
print 'Model built in %f seconds' %(e - s)

def edits(word):
    suggestions = []
    for w in unique_words:
        if levenshtein(w, word) < 2:
            suggestions.append(w)

    return sorted(suggestions, key=lambda x: -model[x])

s = time.time()
suggestions = edits('чвек'.decode('utf-8'))
for w in suggestions:
    print w
e = time.time()
print 'Edit dist one word suggestions found in %f seconds' %(e - s)


