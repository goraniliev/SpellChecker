# -*- coding: utf-8 -*-
import time
from create_model import get_all_words, train
import sys
sys.stdout = open('result.txt', 'w')

__author__ = 'goran'

# text_path = '/home/goran/Desktop/data/dataset-hw.txt'
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
    # print '\t'.join([str(i) for i in row])

    return dp[M][N]


def edits(model, word, unique_words):
    suggestions = []
    print 'Unique Words Count {}'.format(len(unique_words))
    for w in unique_words:
        if levenshtein(w, word) < 2:
            suggestions.append(w)

    return sorted(suggestions, key=lambda x: -model[x])


def test():
    s = time.time()
    words = get_all_words()
    e = time.time()
    print 'Words loaded from file in %f seconds' %(e - s)
    # print(type(words), words[:3])
    unique_words = set(words)
    s = time.time()
    model = train(words)
    e = time.time()
    print 'Model built in %f seconds' % (e - s)

    # Spell Checking
    s = time.time()
    suggestions = edits(model, 'чвек'.decode('utf-8'), unique_words)
    for w in suggestions:
        print w
    e = time.time()
    print 'Edit dist one word suggestions found in %f seconds' % (e - s)


if __name__ == '__main__':
    test()