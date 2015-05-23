import requests
import requests.exceptions
from bs4 import BeautifulSoup
import sqlite3

def crawler(domain):
    db = sqlite3.connect(":memory:")
    c = db.cursor()
    # c.execute("DROP TABLE IF EXISTS searched")
    c.execute("CREATE TABLE searched (link text) ")
    start_page = "http://" + domain
    to_search = []
    to_search.append(start_page)
    while len(to_search) != 0:
        current_page = to_search.pop(0)
        sql2 = "SELECT * FROM searched WHERE link = ? LIMIT 1"
        c.execute(sql2,[(current_page)])
        temp = c.fetchone()
        if temp == None:
            pass
        elif temp[0] == current_page:
            continue
        try:
            source_code = requests.get(current_page,timeout = 1,stream=True)
            contentType = source_code.headers.get('content-type')
            if not 'text/html' in contentType and not 'application/xhtml+xml' in contentType and not 'application/xml' in contentType:
                print(contentType)
                print ("Wrong content-type on url, not parsing: " + current_page)
                print(source_code.status_code)
                sql = "INSERT INTO searched (link) VALUES (?)"
                c.execute(sql,(current_page,))
                db.commit()
                continue
            response = ''
            for chunk in source_code.iter_content(chunk_size=1024,decode_unicode=True):
                if(chunk):
                    response += chunk

        except requests.exceptions.ConnectTimeout:
            print ("Timeout error on url: " + current_page)
            sql = "INSERT INTO searched (link) VALUES (?)"
            c.execute(sql,(current_page,))
            db.commit()
            continue
        except requests.exceptions.ConnectionError:
            print ("Connection error on url: " + current_page)
            sql = "INSERT INTO searched (link) VALUES (?)"
            c.execute(sql,(current_page,))
            db.commit()
            continue
        except requests.exceptions.TooManyRedirects :
            print ("Too many redirects from url: " + current_page)
            sql = "INSERT INTO searched (link) VALUES (?)"
            c.execute(sql,(current_page,))
            db.commit()
            continue
        except :
            print ("some error occurred at url: " + current_page)
            sql = "INSERT INTO searched (link) VALUES (?)"
            c.execute(sql,(current_page,))
            db.commit()
            continue
        sql = "INSERT INTO searched (link) VALUES (?)"
        c.execute(sql,(current_page,))
        db.commit()
        print(current_page)
        print(source_code.status_code)
        if not domain in current_page:
            print (current_page + " not contained in domain: " + domain)
            continue

        plain_text = response#source_code.text
        reaper = BeautifulSoup(plain_text)
        for link in reaper.findAll('a'):
            href = link.get('href')
            if href is None:
                break
            elif href == '':
                break
            elif href[0:7] == 'mailto:':
                break
            elif href[0] == '/':
                puppies = start_page + href
            elif href[0] == '?':
                puppies = start_page + href
            elif href[0] == '#':
                break
            elif href[0] == 'h':
                puppies = href
            #elif href[0] == '@':
            #    puppies = start_page + href
            elif href[0:2] == '..':
                puppies = start_page + href
            else:
                puppies = href
            to_search.append(puppies)

crawler("spsu.edu/")










