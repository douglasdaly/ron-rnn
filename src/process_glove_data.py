#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 11:01:17 2018

@author: doug
"""
#
#   Imports
#
import os
import zipfile
import pickle

import numpy as np


#
#   Functions
#

def load_glove_file(filename):
    """ Loads the raw Glove Embeddings File """
    words = set()
    word_to_embedding = dict()

    with open(filename, 'r') as fin:
        for line in fin:
            line = line.strip().split()
            word = line[0]
            words.add(word)
            word_to_embedding[word] = np.array(line[1:], dtype=np.float64)

    return words, word_to_embedding


def extract_glove_file(zip_file, target_file):
    """ Extracts the target file from the zip archive """
    ret = None
    with zipfile.ZipFile(zip_file) as f:
        if target_file in f.namelist():
            ret = f.extract(target_file, path=os.path.abspath('data'))
    return ret


def main():
    """ Main script function """
    zip_file = 'data/glove.6B.zip'
    target_file = 'glove.6B.50d.txt'
    glove_file = extract_glove_file(zip_file, target_file)

    words, word_to_embedding = load_glove_file(glove_file)

    words_fpath = os.path.join('processed', 'glove_words.pkl')
    with open(words_fpath, 'wb') as fout:
        pickle.dump(words, fout)

    word_to_embedding_fpath = os.path.join('processed',
                                           'glove_word2embedding.pkl')
    with open(word_to_embedding_fpath, 'wb') as fout:
        pickle.dump(word_to_embedding, fout)

#
#   Main Script Entry-Point
#
if __name__ == "__main__":
    main()
