# -*- coding: utf-8 -*-
import time

__author__ = 'goran'

text_path = '../SpellCheckingData/dataset-hw.txt'
separated_words_path = '../SpellCheckingData/dataset.txt'
all_words_path = '../SpellCheckingData/all_words.txt'


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
                # print type(content)
                extracted = extract(content)
                # print(' '.join(extract(content.decode('utf-8'))))
                fout.write((category + '\t' + ' '.join(extracted) + '\n').encode('utf-8'))


def all_words_toghether(path=all_words_path):
    words = get_words()
    with open(path, 'w') as fout:
        fout.write(' '.join(words))


def get_all_words(path=all_words_path):
    words = list()
    with open(path, 'r') as fin:
        for line in fin:
            words.append(line.decode('utf-8').split(' '))
    return words


def test():
    start = time.time()
    transform_dataset()
    end = time.time()

    # 108.331707954 fout ako ja otvaram i zatvaram cesto
    # 92.1931741238 fout ako ja otvoram porano
    print end - start

    all_words_toghether()


if __name__ == '__main__':
    test()
