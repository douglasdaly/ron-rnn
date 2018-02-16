#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 21:49:57 2018

@author: doug
"""
#
#   Imports
#
import os
import pickle

import numpy as np

from keras import Model

from train_network import build_model


#
#   Functions
#

def load_final_model(char_mapping):
    """ Loads the final Model from file """
    fpath = os.path.join("checkpoints", "ron_rnn_model-final.h5")

    model = build_model(char_mapping)
    model.load_weights(fpath)

    return model


def load_char_mapping():
    """ Loads the character mapping object """
    fpath = os.path.join("processed", "unq_chars.pkl")
    with open(fpath, "rb") as fin:
        ret = pickle.load(fin)

    return ret


def get_formatted_data(sentence, char_mapping, sequence_length):
    """ Formats the given string into a matrix to feed to the network """
    ret = np.zeros((1, sequence_length, len(char_mapping)))
    i = 0
    for ch in sentence.lower():
        ret[0, i, (char_mapping == ch).argmax()] = 1
        i += 1

    return ret


def generate_quote(model, start_letters, char_mapping, sequence_length):
    """ Generates a quote given the starting letter(s) """
    ret = start_letters
    curr = start_letters
    next_letter = ""

    i = len(start_letters) - 1
    while next_letter not in ('.', '!', '?'):
        t_out = model.predict(get_formatted_data(curr, char_mapping, sequence_length))
        next_letter = char_mapping[t_out[0, i, :].argmax()]
        i = min(sequence_length-1, i+1)
        ret += next_letter
        curr += next_letter
        if len(curr) > 20:
            curr = curr[-20:-1]

    return ret
