# -*- coding: utf-8 -*-
"""
Script to get Quotes from swansonquotes.com
"""
#
#   Imports
#
import os
import time
import urllib.request

from bs4 import BeautifulSoup


#
#   Variables and Functions
#

first_url = "http://swansonquotes.com/quotes/season01/ep-01-pilot-bobby-knight/"

def get_ron_quotes_html(page):
    """ Gets the Raw Page HTML """
    try:
        request = urllib.request.urlopen(page)
        return BeautifulSoup(request, "lxml")
    except:
        return None


def get_quotes_on_page(start_page):
    """ Extracts the quotes from the page HTML """
    cnt = 0
    soup = None
    while soup is None and cnt < 3:
        cnt += 1
        soup = get_ron_quotes_html(start_page)
        if soup is None:
            time.sleep(15)
            continue

    if soup is None:
        return ([], None)

    test_div = soup.find("div", class_="entry-content")

    temp_list = list()
    b_is_ron = False
    for p in test_div.find_all('p'):
        if p.get('class', "") == ['introblurb']:
            continue
        elif p.get('class', "") == ['quotelabel']:
            if p.string.strip() == "Ron Swanson:":
                b_is_ron = True
                continue
            else:
                b_is_ron = False
                continue

        if b_is_ron:
            temp_list.append(p.get_text())

    next_page = soup.find("div", class_="next").find('a')

    if next_page is not None:
        next_page = next_page.attrs.get('href', None)

    return (temp_list, next_page)


def get_all_lines():
    """ Iterate through pages """
    all_lines = list()
    next_page = first_url
    while next_page is not None:
        temp_contents, next_page = get_quotes_on_page(next_page)
        if next_page is not None and not next_page.strip().split('/')[-2].startswith('ep-'):
            continue
        all_lines.extend(temp_contents)

    return all_lines


def main():
    """ Main script function """
    all_lines = get_all_lines()
    filepath = os.path.join('data', 'swansonquotes_quotes.txt')
    with open(filepath, 'w') as fout:
        fout.writelines(all_lines)


#
#   Script Entry-Point
#

if __name__ == "__main__":
    main()

