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

from sklearn.preprocessing import OneHotEncoder


#
#   Functions
#

def get_all_quote_files():
    """ Gets the filenames from the given directory """
    data_files = [f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f))]
    ret = [f for f in data_files if f.find('quotes') > -1]
    return ret


def get_moby_dick_lines():
    """ Gets Moby Dick text training files """
    moby_dick_file = os.path.join("data", "moby_dick.txt")
    ret = list()
    with open(moby_dick_file, 'r') as fin:
        file_lines = fin.readlines()

    book_started = False

    start_string = "CHAPTER 1. Loomings."
    end_string = "End of Project Gutenberg’s Moby Dick; or The Whale, by Herman Melville"

    for line in file_lines:
        line = line.strip()
        if not book_started:
            if line == start_string:
                book_started = True
            continue

        if line == end_string:
            break

        if line.lower().startswith("chapter") or len(line) < 2:
            continue

        ret.append(line)

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
            ret += ch
    return ret.strip()


def clean_file_text(file_lines):
    """ Cleans the given file contents """
    ret = list()
    for line in file_lines:
        ret.append(clean_line(line))
    return ret


def process_all_lines(files):
    """ Get all lines from all relevant files """
    all_lines = list()
    for file in files:
        t_lines = load_text_file(file)
        all_lines.extend(clean_file_text(t_lines))
    return all_lines


def get_unique_characters(all_lines):
    """ Get all unique characters from the given lines """
    unq_chars = set()
    for line in all_lines:
        unq_chars = unq_chars.union([ch for ch in line])
    return np.array(sorted(unq_chars))


def get_indices(all_lines, unq_chars):
    """ Get Indices of words for each sentence """
    all_indices = list()
    for line in all_lines:
        t_indices = np.array([(unq_chars == ch).argmax()
                              for ch in line if ch in unq_chars])
        if len(t_indices) < 2:
            continue

        all_indices.append(t_indices.reshape(-1, 1))
    return all_indices


def convert_indices_to_one_hot_vectors(indices, char_mapping):
    """ Converts the list of indices to one-hot vectors """
    ohe = OneHotEncoder(len(char_mapping))
    ret = list()
    for arr in indices:
        ret.append(ohe.fit_transform(arr).todense())
    return ret


def main():
    """ Main script function """
    files = get_all_quote_files()
    all_lines = process_all_lines(files)

    unq_chars = get_unique_characters(all_lines)[:30]

    all_indices = get_indices(all_lines, unq_chars)
    del all_lines
    all_onehots = convert_indices_to_one_hot_vectors(all_indices, unq_chars)
    del all_indices

    addl_lines = clean_file_text(get_moby_dick_lines())
    addl_indices = get_indices(addl_lines, unq_chars)
    del addl_lines
    addl_onehots = convert_indices_to_one_hot_vectors(addl_indices, unq_chars)
    del addl_indices

    unq_chars_fpath = os.path.join('processed', 'unq_chars.pkl')
    with open(unq_chars_fpath, 'wb') as fout:
        pickle.dump(unq_chars, fout)

    quote_fpath = os.path.join('processed', 'quote_onehots.pkl')
    with open(quote_fpath, 'wb') as fout:
        pickle.dump(all_onehots, fout)

    addl_fpath = os.path.join('processed', 'addl_onehots.pkl')
    with open(addl_fpath, 'wb') as fout:
        pickle.dump(addl_onehots, fout)


#
#   Entry Point
#
if __name__ == "__main__":
    main()
