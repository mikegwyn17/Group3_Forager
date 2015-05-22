import requests
from bs4 import BeautifulSoup


def crawler(domain):
    start_page = "http://" + domain
    to_search = []
    searched = []
    to_search.append(start_page)
    while (len(to_search) != 0):
        current_page = to_search.pop(0)
        if current_page in searched:
            # print(current_page + " already searched")
            continue
        try:
            source_code = requests.get(current_page,timeout = 1)
        except TimeoutError:
            print ("Timeout error on url: " + current_page)
            searched.append(current_page)
            continue
        except ConnectionError:
            print ("Connection error on url: " + current_page)
            searched.append(current_page)
            continue
        except :
            print ("some error occurred at url: " + current_page)
            searched.append(current_page)
            continue
        searched.append(current_page)
        print(current_page)
        print(source_code.status_code)
        if not domain in current_page:
            print (current_page + " not contained in domain: " + domain)
            continue
        plain_text = source_code.text
        reaper = BeautifulSoup(plain_text)
        for link in reaper.findAll('a'):
            if link.get('href') is None:
                break
            elif link.get('href') == '':
                break
            elif link.get('href')[0] == '/':
                puppies = start_page + link.get('href')
            elif link.get('href')[0] == '?':
                puppies = start_page + link.get('href')
            elif link.get('href')[0] == '#':
                puppies = start_page + link.get('href')
            elif link.get('href')[0] == 'h':
                puppies = link.get('href')
            elif link.get('href')[0] == '@':
                puppies = start_page + link.get('href')
            elif link.get('href')[0:2] == '..':
                puppies = start_page + link.get('href')
            else:
                puppies = link.get('href')
            to_search.append(puppies)

crawler("spsu.edu/")










