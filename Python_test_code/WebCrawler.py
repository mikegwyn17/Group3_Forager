import socket
import requests
import requests.exceptions
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import tldextract

def crawler(start_page):
    domain = str(tldextract.extract(start_page).domain)
    requests.packages.urllib3.disable_warnings()
    client = MongoClient('localhost',27017)
    db = client.Reports_Database
    report_number = db.Report_Data.count() + 1
    print(report_number)
    start_time = str(datetime.utcnow().date()) + " / "
    start_time += str(datetime.utcnow().time())
    insert_report_data(db,report_number,start_time, end_time="")
    to_search = []
    searched = set()
    parents = []
    to_search.append(start_page)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
    while len(to_search) != 0:
        current_page = to_search.pop()
        current_domain = str(tldextract.extract(current_page).domain)
        if len(parents) != 0:
            parents.pop()
        if current_page in searched:
            continue
        try:
            source_code = requests.head(current_page, headers = headers, allow_redirects = True, verify = False)
            contentType = source_code.headers.get('content-type')
            searched.add(current_page)
            status_code = source_code.status_code
            print(current_page)
            print(status_code)
            if status_code is not 200:
                insert_report(report_number,current_page, parents[0], str(status_code), db)
                update_report_data(db,report_number,"error_count")
                continue
            if contentType is None:
                print("None content type: " + current_page)
                insert_report(report_number, current_page, parents[0], "None content-type",db)
                update_report_data(db,report_number,"error_count")
                continue
            elif 'text/html' not in contentType and 'application/xhtml+xml' not in contentType and 'application/xml' not in contentType:
                print(contentType)
                print("Wrong content-type on url, not parsing: " + current_page)
                searched.add(current_page)
                continue
        except requests.exceptions.ConnectTimeout:
            print("Timeout error on url: " + current_page)
            insert_report(report_number, current_page, parents[0], "Connection Timeout", db)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.ConnectionError:
            print("Connection error on url: " + current_page)
            insert_report(report_number, current_page, parents[0], "Connection Error", db)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects from url: " + current_page)
            insert_report(report_number, current_page, parents[0], "Too Many Redirects", db)
            update_report_data(db,report_number,"error_count")
            continue
        except socket.timeout:
            print("timeout at url: " + current_page)
            insert_report(report_number, current_page, parents[0], "Socket Timeout", db)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.ReadTimeout:
            print("Read timeout on url: " + current_page)
            insert_report(report_number, current_page, parents[0], "Read Timeout", db)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.InvalidURL:
            print("Invalid URL: " + current_page)
            insert_report(report_number, current_page, parents[0], "Invalid URL", db)
            update_report_data(db,report_number,"error_count")
        searched.add(current_page)
        if current_domain not in domain:
            print(current_page + " not contained in domain: " + domain)
            continue
        plain_text = requests.get(current_page, headers = headers, verify = False, allow_redirects = True)
        plain_text = plain_text.text
        reaper = BeautifulSoup(plain_text)
        for image in reaper.findAll('img'):
            src = image.get('src')
            if src is None:
                break
            elif src[0:4] == 'http' or src[0:5] == 'https':
                src = src
            else:
                src = start_page + src
            update_report_data(db,report_number,"page_count")
            print(src)
            try :
                image_status_code = requests.head(src, allow_redirects = True, verify = False).status_code
                print(image_status_code)
                if image_status_code is not 200:
                    insert_report(report_number, src, current_page, "Missing Image", db)
                    update_report_data(db,report_number,"error_count")
            except requests.exceptions.ConnectionError:
                insert_report(report_number, src, current_page, "Missing Image", db)
                update_report_data(db,report_number,"error_count")
            except:
                insert_report(report_number, src, current_page, "Missing Image", db)
                update_report_data(db,report_number,"error_count")
        for css in reaper.findAll('link'):
            href = css.get('href')
            if href is None:
                break
            elif href[0:4] == 'http' or href[0:5] == 'https':
                href = href
            else:
                href = start_page + href
            update_report_data(db,report_number,"page_count")
            print(href)
            try:
                css_status_code = requests.head(href, allow_redirects = True, verify = False).status_code
                print(css_status_code)
                if css_status_code is not 200:
                    insert_report(report_number, href, current_page, "Missing CSS File", db)
                    update_report_data(db,report_number,"error_count")
            except requests.exceptions.ConnectionError:
                insert_report(report_number, href, current_page, "Missing CSS File", db)
                update_report_data(db,report_number,"error_count")
            except :
                insert_report(report_number, href, current_page, "Missing CSS File", db)
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
            elif href[0:10] == 'javascript':
                break
            else:
                puppies = start_page + href
            to_search = [puppies] + to_search
            parents = [current_page] + parents
        update_report_data(db,report_number,"page_count")
    update_report_data(db,report_number,"end_time")

def insert_report(report_number, url, parent, error_type, db):
    Reports = db.Reports
    # taco = Reports.find_one({"$and":[{'parent_url': parent}, {'report_number': report_number})]})
    taco = Reports.find_one({"$and": [{"parent_url":parent}, {"report_number":report_number}]})
    if taco is None:
        report = {"report_number": report_number,
        "parent_url": parent,
        "errors": [],
        "error_count": 0}
        reports_id = Reports.insert(report)
        reports_id
    Reports.update_one({"$and": [{"parent_url":parent}, {"report_number":report_number}]}, {'$push': {'errors': {'url': url, "error_type": error_type}}})
    Reports.update({"$and": [{"parent_url":parent}, {"report_number":report_number}]}, {'inc': {"error_count": 1}})
    # Reports.find( { "$orderby": { "error_count" : 1 } } )
    Reports.find({"report_number": report_number}).sort("error_count",1)

def insert_report_data(db, report_number, start_time, end_time):
    report_data = {"report_number": report_number,
                    "error_count": 0,
                   "page_count": 0,
                   "start_time": start_time,
                   "end_time": end_time }
    reports_data = db.Report_Data
    report_data_id = reports_data.insert(report_data)
    report_data_id
    # reports_data.find( {"$orderby": { "report_number" : 1 } } )
    reports_data.find().sort("report_number", 1)

def update_report_data (db, report_number, update_type):
    report_data = db.Report_Data
    if update_type is "error_count":
        report_data.update({'report_number': report_number}, {'$inc': {'error_count': 1}})
    elif update_type is "page_count":
        report_data.update({'report_number': report_number}, {'$inc': {'page_count': 1}})
    else:
        end_time = str(datetime.utcnow().date()) + " / "
        end_time += str(datetime.utcnow().time())
        report_data.update({'report_number': report_number}, {'$set': {'end_time': end_time}})

crawler("https://www.spsu.edu/")
