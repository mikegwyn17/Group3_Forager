import requests
import requests.exceptions
from bs4 import BeautifulSoup
import sqlite3
import socket

def crawler(domain):
    db = sqlite3.connect("pydb.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS report_1")
    c.execute("CREATE TABLE report_1 (id integer primary key autoincrement, url text, parent_url text, error_type text)")
    start_page = "http://" + domain
    to_search = set()
    searched = set()
    current_page = ''
    to_search.add(start_page)
    while len(to_search) != 0:
        parent_page = current_page
        current_page = to_search.pop()
        if current_page in searched:
            continue
        # sql2 = "SELECT * FROM searched WHERE link = ? LIMIT 1"
        # c.execute(sql2,[(current_page)])
        # temp = c.fetchone()
        # if temp == None:
        #     pass
        # elif temp[0] == current_page:
        #     continue
        try:
            source_code = requests.get(current_page,timeout = 1,stream=True)
            status_code = source_code.status_code
            print(current_page)
            print(status_code)
            if status_code is not 200:
                insert(current_page,parent_page,status_code,c,db)
            contentType = source_code.headers.get('content-type')
            if contentType is None:
                print("None content type: " + current_page)
                insert(current_page,parent_page,"None content-type",c,db)
                continue
            elif 'text/html' not in contentType and 'application/xhtml+xml' not in contentType and 'application/xml' not in contentType:
                print(contentType)
                print ("Wrong content-type on url, not parsing: " + current_page)
                searched.add(current_page)
                continue
            response = ''
            for chunk in source_code.iter_content(chunk_size=1024,decode_unicode=True):
                if chunk:
                    response += chunk
        except requests.exceptions.ConnectTimeout:
            print ("Timeout error on url: " + current_page)
            # sql = "INSERT INTO searched (link) VALUES (?)"
            # c.execute(sql,(current_page,))
            # db.commit()
            insert(current_page,parent_page,"Connection Timeout",c,db)
            searched.add(current_page)
            continue
        except requests.exceptions.ConnectionError:
            print ("Connection error on url: " + current_page)
            # sql = "INSERT INTO searched (link) VALUES (?)"
            # c.execute(sql,(current_page,))
            # db.commit()
            searched.add(current_page)
            insert(current_page,parent_page,"Connection Error",c,db)
            continue
        except requests.exceptions.TooManyRedirects :
            print ("Too many redirects from url: " + current_page)
            # sql = "INSERT INTO searched (link) VALUES (?)"
            # c.execute(sql,(current_page,))
            # db.commit()
            searched.add(current_page)
            insert(current_page,parent_page,"Too Many Redirects",c,db)
            continue
        except socket.timeout:
            print ("timeout at url: " + current_page)
            # sql = "INSERT INTO searched (link) VALUES (?)"
            # c.execute(sql,(current_page,))
            # db.commit()
            searched.add(current_page)
            insert(current_page,parent_page,"Socket Timeout",c,db)
            continue
        except requests.exceptions.ReadTimeout:
            print ("Read timeout on url: " + current_page)
            searched.add(current_page)
            insert(current_page,parent_page,"Read Timeout",c,db)
        # sql = "INSERT INTO searched (link) VALUES (?)"
        # c.execute(sql,(current_page,))
        # db.commit()
            continue
        except requests.exceptions.InvalidSchema:
            print("Invalid Url: " + current_page)
            searched.add(current_page)
            insert(current_page,parent_page,"Invalid Schema",c,db)
            continue
        searched.add(current_page)
        if domain not in current_page:
            print(current_page + " not contained in domain: " + domain)
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
            elif href[0:2] == '..':
                puppies = start_page + href
            elif href[0:4] == 'http' or href[0:5] == 'https':
                puppies = href
            else:
                puppies = start_page + href
            to_search.add(puppies)

def insert (url, parent, error_type, c, db):
    sql = "INSERT INTO report_1 (url,parent_url,error_type) VALUES (?,?,?)"
    c.execute(sql, (url,parent,error_type))
    db.commit()


crawler("spsu.edu/")












