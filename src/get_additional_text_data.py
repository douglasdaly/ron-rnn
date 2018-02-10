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

moby_dick_url = "https://www.gutenberg.org/files/2701/2701-0.txt"


def download_file(filename, url):
    """ Downloads a file if not already downloaded """
    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url, filename)


def main():
    """ Main script routine """
    download_file("data/moby_dick.txt", moby_dick_url)


#
#   Script Entry Point
#
if __name__ == "__main__":
    main()
