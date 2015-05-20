import requests
import re
from bs4 import BeautifulSoup

def crawler(domain):
    to_search = []
    searched = []
    to_search.append(domain)
    while (len(to_search) != 0):
        current_page = to_search.pop(0)
        print(current_page)
        if current_page in searched:
            continue
        source_code = requests.get(current_page)
        print(source_code.status_code)
        searched.append(current_page)
        plain_text = source_code.text
        reaper = BeautifulSoup(plain_text)
        for link in reaper.findAll('a'):
            # if (link.has_attr('href')):
            #     print(link['href'])
            if link.get('href') is None:
                break
            elif link.get('href') == '':
                break
            elif link.get('href')[0] == '/':
                puppies = domain + link.get('href')
                # print(link.get('href'))
            elif link.get('href')[0] == '?':
                puppies = domain + link.get('href')
            elif link.get('href')[0] == '#':
                puppies = domain + link.get('href')
            elif link.get('href')[0] == 'h':
                puppies = link.get('href')
            elif link.get('href')[0] == '@':
                puppies = domain + link.get('href')
            elif link.get('href')[0:2] == '..':
                puppies = domain + link.get('href')
            else:
                break
            to_search.append(puppies)
    for link in searched:
        print(link)
    for link in to_search:
        print(link)

crawler("https://spsu.edu")







