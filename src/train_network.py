# -*- coding: utf-8 -*-
"""
Create and Train an RNN
"""
#
#   Imports
#
#%%
import os
import pickle

import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation
from keras.layers.wrappers import TimeDistributed
from keras.callbacks import ModelCheckpoint


#
#   Function Definitions
#

def get_data():
    """ Gets the X and Y data to use """
    chars_fpath = os.path.join("processed", "unq_chars.pkl")
    with open(chars_fpath, "rb") as fin:
        char_mapping = pickle.load(fin)

    addl_fpath = os.path.join("processed", "addl_onehots.pkl")
    with open(addl_fpath, "rb") as fin:
        addl_data = pickle.load(fin)

    quotes_fpath = os.path.join("processed", "quote_onehots.pkl")
    with open(quotes_fpath, "rb") as fin:
        quote_data = pickle.load(fin)

    return char_mapping, quote_data, addl_data


def get_training_data(data, sequence_length):
    """ Converts the given Data into Training Data of given Length """
    x_data = list()
    y_data = list()
    samples = 0
    for line in data:
        if line.shape[0] < sequence_length + 1:
            continue
        for i in range(line.shape[0]-sequence_length-1):
            samples += 1
            x_data.append(line[i:i+sequence_length, :])
            y_data.append(line[(i+1):(i+sequence_length+1), :])

    full_x = np.zeros((samples, sequence_length, data[0].shape[1]))
    full_y = np.zeros(full_x.shape)
    for i in range(samples):
        full_x[i, :, :] = x_data[i]
        full_y[i, :, :] = y_data[i]

    return full_x, full_y


def build_model(char_mapping):
    """ Constructs the RNN Model """
    model = Sequential()

    # - First Layer
    model.add(LSTM(512, input_shape=(None, len(char_mapping)),
                   return_sequences=True))
    model.add(Dropout(0.3))

    # - Next Layer
    model.add(TimeDistributed(Dense(len(char_mapping))))
    model.add(Activation("softmax"))

    # - Compile
    model.compile("adam", "categorical_crossentropy")

    return model


def main():
    """ Main script routine """
    seq_len = 30
    char_mapping, quote_data, addl_data = get_data()
    x_quote, y_quote = get_training_data(quote_data, seq_len)
    x_addl, y_addl = get_training_data(addl_data, seq_len)

    model = build_model(char_mapping)

    # - Any existing checkpoints to work off of?
    start_epoch = 0
    for _, _, filenames in os.walk("checkpoints"):
        for filename in filenames:
            if filename.startswith('ron_rnn_model-addl-'):
                t_epoch = int(filename.split('.')[0].split('-')[-1])
                if t_epoch > start_epoch:
                    start_epoch = t_epoch

    if start_epoch > 0:
        filename = os.path.join("checkpoints", "ron_rnn_model-addl-" +
                                str(start_epoch) + ".h5")
        model.load_weights(filename)

    # - Model Checkpoint Callbacks
    addl_checkpoint = \
        ModelCheckpoint("checkpoints/ron_rnn_model-addl-{epoch:02d}.h5")
    quote_checkpoint = \
        ModelCheckpoint("checkpoints/ron_rnn_model-quote-{epoch:02d}.h5")

    # - Fit Addl Data
    print("Training on Moby Dick Data...")
    batch_size = 2048
    addl_epochs = 1000
    addl_history = model.fit(x=x_addl, y=y_addl, batch_size=batch_size,
                             epochs=addl_epochs-start_epoch,
                             callbacks=[addl_checkpoint], verbose=1)

    # - Fit Quote Data
    print("Training on Ron Data...")
    quote_epochs = 2 * addl_epochs
    quote_history = model.fit(x=x_quote, y=y_quote, batch_size=batch_size,
                              epochs=quote_epochs,
                              callbacks=[quote_checkpoint], verbose=1)

    model.save(os.path.join("checkpoints", "ron_rnn_model-final.h5"))


#
#   Script Entry Point
#
if __name__ == "__main__":
    main()
