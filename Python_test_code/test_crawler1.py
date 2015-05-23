import requests
from bs4 import BeautifulSoup

to_search = []
searched = []
# first level of the crawler
# when given url it will print and visit all of the links and print them
def main_crawler(url):
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
            href = url + link.get('href')
        elif link.get('href')[0] == '?':
            href = url + link.get('href')
        elif link.get('href')[0] == '#':
            href = url + link.get('href')
        else:
            href = link.get('href')
        print(href)
        # visit the link and call other method
        follow_link(href,url)

# second level crawler
# called by first level crawler
# used to visit each of the links found on the first page and continue visting links found in all subsequent pages
def follow_link(url,domain):
     # use requests to visit the webpage
    source_code = requests.get(url)
    print (source_code.headers.get('content-type'))

    return 0
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
                href = domain + link.get('href')
            elif link.get('href')[0] == '?':
                href = domain + link.get('href')
            elif link.get('href')[0] == '#':
                href = domain + link.get('href')
            elif link.get('href')[0] == 'h':
                href = link.get('href')
            else:
                break
            # link_list.append(href)
            print (href)
            follow_link(href,domain)
    # for i in link_list :
    #     print (i)

main_crawler("https://www.google.com/search?site=&tbm=isch&source=hp&biw=1366&bih=633&q=test&oq=test&gs_l=img.3..0l10.423.823.0.930.4.4.0.0.0.0.76.273.4.4.0....0...1ac.1.64.img..0.4.269.kRK2_3znP08#imgrc=VQUlLl0xPZERiM%253A%3BSxKw7cjibJVeiM%3Bhttp%253A%252F%252Fwww.pbs.org%252Fnewshour%252Fwp-content%252Fuploads%252F2014%252F08%252FTesting.jpg%3Bhttp%253A%252F%252Fwww.pbs.org%252Fnewshour%252Fmaking-sense%252Fask-the-headhunter-an-insiders-tips-for-approaching-employment-tests%252F%3B1050%3B701")
































































































































