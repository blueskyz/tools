#!/usr/bin/env python3
# coding: utf-8


import sys
import webbrowser


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('params err')

    chrome = webbrowser.get('chrome')

    if sys.argv[1] == 'google.com':
        search_url = 'http://www.google.com/search?q={}'.format(sys.argv[2])
    else:
        search_url = 'http://www.baidu.com/s?wd={}'.format(sys.argv[2])
    chrome.open_new_tab(search_url)

