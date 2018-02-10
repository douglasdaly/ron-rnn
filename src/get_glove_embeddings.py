# -*- coding: utf-8 -*-
"""
Download GloVe Embeddings Data
"""
#
#   Imports
#
import os
import urllib.request


#
#   Functions
#

glove_url = "http://nlp.stanford.edu/data/glove.6B.zip"


def download_file(filename, url):
    """ Downloads a file if not already downloaded """
    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url, filename)


def main():
    filename = "data/glove.6B.zip"
    download_file(filename, glove_url)


#
#   Script Entry-Point
#
if __name__ == "__main__":
    main()
