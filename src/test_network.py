# -*- coding: utf-8 -*-
"""
Generate a quote with the trained network
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
    fpath = "ron_rnn_model-final.h5"

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
        next_letter = char_mapping[np.random.choice(range(len(char_mapping)),
                                                    1, p=t_out[0, i, :])[0]]
        i = min(sequence_length-1, i+1)

        ret += next_letter
        curr += next_letter
        if len(curr) > sequence_length:
            curr = curr[-sequence_length:]

    return ret


def main(input_text=None):
    """ Main script method """
    sequence_length = 30
    char_mapping = load_char_mapping()

    probabilities = np.array([0.08167, 0.01492, 0.02782, 0.04253, 0.12702,
                              0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
                              0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
                              0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
                              0.02758, 0.00978, 0.02360, 0.00150, 0.01974,
                              0.00074])
    probabilities = probabilities / probabilities.sum()

    if input_text is None:
        first_letter = char_mapping[np.random.choice(range(len(probabilities)),
                                                     1, p=probabilities)+4][0]
    else:
        first_letter = input_text[0:sequence_length]

    model = load_final_model(char_mapping)

    quote = generate_quote(model, first_letter, char_mapping, sequence_length)

    print("Quote:", quote)


#
#   Script Entry Point
#
if __name__ == "__main__":
    main()
