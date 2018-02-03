# -*- coding: utf-8 -*-
"""
Get all Ron Swanson quotes from www.tvfanatic.com
"""
#
#   Imports
#
import os
import urllib.request

from bs4 import BeautifulSoup


#
#   Variables and Functions
#

base_url = "https://www.tvfanatic.com/quotes/characters/ron-swanson/page-{}.html"

def get_ron_quotes_html(page):
    url = base_url.format(page)
    request = urllib.request.urlopen(url)
    return BeautifulSoup(request, "lxml")


def get_rons_lines(quotes):
    ron_lines = list()
    for quote in quotes:
        paragraphs = quote.find_all("p")
        for p in paragraphs:
            for s in p.stripped_strings:
                first_word = s.split()[0]
                if first_word.endswith(":"):
                    if first_word[:-1].lower() != "ron":
                        continue
                    s = s.replace(first_word, "").strip()
                ron_lines.append(s)
    return ron_lines


def get_ron_quotes():
    pages = range(1, 26)
    all_lines = list()
    for i in pages:
        t_page = get_ron_quotes_html(i)
        quotes = t_page.find("div", id="infinite").find_all("blockquote")
        all_lines.extend(get_rons_lines(quotes))
    return all_lines


def main():
    all_lines = get_ron_quotes()
    filepath = os.path.join("data", "ron_quotes.txt")
    with open(filepath, "w") as fout:
        fout.writelines(all_lines)


#
#   Script Entry-Point
#

if __name__ == "__main__":
    main()

