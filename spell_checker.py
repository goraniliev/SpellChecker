# -*- coding: utf-8 -*-
import time
from create_model import get_all_words, train


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
    new_model = {}
    for w in unique_words:
        if abs(len(w) - len(word)) <= 2:
            distance = levenshtein(w, word)
            if distance <= 2:
                suggestions.append(w)
                new_model[w] = distance
    # return sorted(suggestions, key=lambda x: -model[x])
    return sorted(suggestions, key=lambda x: (-model[x], new_model[x]))[0: min(len(suggestions), 10)]


def test():
    s = time.time()
    words = get_all_words()
    e = time.time()
    print 'Words loaded from file in %f seconds' % (e - s)

    unique_words = set(words)
    print 'Number of unique words: {}'.format(len(unique_words))

    s = time.time()
    model = train(words)
    e = time.time()
    print 'Model built in %f seconds' % (e - s)

    # Spell Checking
    while True:
        query_word = raw_input("Enter a word: ")
        if query_word == 'Х':
            break
        suggestions = edits(model, query_word.decode('utf-8'), unique_words)
        for w in suggestions:
            print w


if __name__ == '__main__':
    test()
