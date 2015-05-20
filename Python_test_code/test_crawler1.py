import requests
from bs4 import BeautifulSoup

# first level of the crawler
# when given url it will print and visit all of the links on the page and store them into a list
def main_crawler(url):
    link_list = []
    # use requests to visit the webpage
    source_code = requests.get(url)
    # format source code of webpage
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    # find all links on the current webpage and add them to the list of links
    # if statements used to create valid links if the domain is not included, or not create link if the value is None
    for link in soup.findAll('a'):
        if link.get('href') is None:
            break
        elif link.get('href')[0] == '/':
            href = "https://spsu.edu" + link.get('href')
        elif link.get('href')[0] == '?':
            href = "https://spsu.edu" + link.get('href')
        else:
            href = link.get('href')
        link_list.append(href)
        # visit the link and call other method
        # follow_link(href)
    for link in link_list:
        print(link)

# second level crawler
# called by first level crawler
# used to visit each of the links found on the first page and continue visting links found in all subsequent pages
def follow_link(url):
    link_list = []
     # use requests to visit the webpage
    source_code = requests.get(url)
    # print out status of webpage
    # can be used later to determine if the webpage is a broken link
    print (source_code.status_code)
    # format source code of webpage
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    # find all links on the current webpage and print them
    # if statements used to create valid links if the domain is not included, or not create link if the value is None
    for link in soup.findAll('a'):
            if link.get('href') is None:
                break
            elif link.get('href')[0] == '/':
                href = "https://spsu.edu" + link.get('href')
            elif link.get('href')[0] == '?':
                href = "https://spsu.edu" + link.get('href')
            elif link.get('href')[0] == '#':
                href = "https://spsu.edu" + link.get('href')
            elif link.get('href')[0] == 'h':
                href = link.get('href')
            else:
                break
            # link_list.append(href)
            print (href)
    # for i in link_list :
    #     print (i)


main_crawler("https://spsu.edu/")












