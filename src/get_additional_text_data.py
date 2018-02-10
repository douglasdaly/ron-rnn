# -*- coding: utf-8 -*-
"""
Download Additional Text Data
"""
#
#   Imports
#
import os
import urllib.request


#
#   Functions
#

text_url = "http://mattmahoney.net/dc/text8.zip"


def download_file(filename, url):
    """ Downloads a file if not already downloaded """
    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url, filename)


def main():
    """ Main script routine """
    download_file("data/text8.zip", text_url)


#
#   Script Entry Point
#
if __name__ == "__main__":
    main()
