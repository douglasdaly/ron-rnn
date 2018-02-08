# -*- coding: utf-8 -*-
"""
Process Ron Swanson Quote Raw Data into Machine-Usable Form
"""
#
#   Imports
#
import os
import pickle

import numpy as np


#
#   Functions
#

def get_all_quote_files():
    """ Gets the filenames from the given directory """
    data_files = [f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))]
    ret = [f for f in data_files if f.find('quotes') > -1]
    return ret


def load_text_file(filename):
    """ Loads all lines from given text file """
    filepath = os.path.join("data", filename)
    with open(filepath, 'r') as fin:
        ret = fin.readlines()
    return ret


def clean_line(line):
    """ Cleans a single line of text """
    ret = ''
    for ch in line.lower():
        if ch.isalpha():
            ret += ch
        elif ch == ' ':
            ret += ch
        elif ch in ('.', '?', '!'):
            ret += " <EOL> "
    return ret.strip()


def clean_file_text(file_lines):
    """ Cleans the given file contents """
    ret = list()
    for line in file_lines:
        ret.append(clean_line(line))
    return ret


def process_all_lines():
    """ Get all lines from all relevant files """
    files = get_all_quote_files()
    all_lines = list()
    for file in files:
        t_lines = load_text_file(file)
        all_lines.extend(clean_file_text(t_lines))
    return all_lines


def get_unique_words(all_lines):
    """ Get all unique words from the given lines """
    unq_lines = set()
    for line in all_lines:
        unq_lines = unq_lines.union(line.split())
    return np.array(sorted(unq_lines))


def get_indices(all_lines, unq_words):
    """ Get Indices of words for each sentence """
    all_indices = list()
    for line in all_lines:
        words = line.strip().split()
        t_indices = [(unq_words == w).argmax() for w in words]
        all_indices.append(t_indices)
    return all_indices


def main():
    """ Main script function """
    all_lines = process_all_lines()
    unq_words = get_unique_words(all_lines)
    all_indices = get_indices(all_lines, unq_words)

    unq_words_fpath = os.path.join('processed', 'unq_words.pkl')
    with open(unq_words_fpath, 'wb') as fout:
        pickle.dump(unq_words, fout)

    indices_fpath = os.path.join('processed', 'all_indices.pkl')
    with open(indices_fpath, 'wb') as fout:
        pickle.dump(all_indices, fout)


#
#   Entry Point
#

if __name__ == "__main__":
    main()
