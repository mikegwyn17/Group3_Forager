import socket
import requests
import requests.exceptions
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

def crawler(domain):
    client = MongoClient('localhost',27017)
    db = client.Reports_Database
    report_number = db.report_data.count() + 1
    print(report_number)
    error_count = 0
    page_count = 0
    start_time = str(datetime.utcnow().date()) + " / "
    start_time += str(datetime.utcnow().time())
    print(start_time)
    insert_report_data(db,report_number,error_count,page_count,start_time, end_time="")
    start_page = "http://" + domain
    to_search = []
    searched = set()
    parents = []
    to_search.append(start_page)
    count = 0
    while len(to_search) != 0:
        current_page = to_search.pop()
        if len(parents) != 0:
            parents.pop()
        if current_page in searched:
            continue
        try:
            source_code = requests.get(current_page, stream=True)
            status_code = source_code.status_code
            print(current_page)
            print(status_code)
            if status_code is not 200:
                count += 1
                insert_report(current_page, parents[0], str(status_code), db, count)
                update_report_data(db,report_number,"error_count")
                continue
            contentType = source_code.headers.get('content-type')
            if contentType is None:
                print("None content type: " + current_page)
                count += 1
                insert_report(current_page, parents[0], "None content-type", db, count)
                update_report_data(db,report_number,"error_count")
                continue
            elif 'text/html' not in contentType and 'application/xhtml+xml' not in contentType and 'application/xml' not in contentType:
                print(contentType)
                print("Wrong content-type on url, not parsing: " + current_page)
                searched.add(current_page)
                continue
            response = ''
            for chunk in source_code.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    response += chunk
        except requests.exceptions.ConnectTimeout:
            print("Timeout error on url: " + current_page)
            count += 1
            insert_report(current_page, parents[0], "Connection Timeout", db, count)
            update_report_data(db,report_number,"error_count")
            searched.add(current_page)
            continue
        except requests.exceptions.ConnectionError:
            print("Connection error on url: " + current_page)
            searched.add(current_page)
            count += 1
            insert_report(current_page, parents[0], "Connection Error", db, count)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects from url: " + current_page)
            searched.add(current_page)
            count += 1
            insert_report(current_page, parents[0], "Too Many Redirects", db, count)
            update_report_data(db,report_number,"error_count")
            continue
        except socket.timeout:
            print("timeout at url: " + current_page)
            searched.add(current_page)
            count += 1
            insert_report(current_page, parents[0], "Socket Timeout", db, count)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.ReadTimeout:
            print("Read timeout on url: " + current_page)
            searched.add(current_page)
            count += 1
            insert_report(current_page, parents[0], "Read Timeout", db, count)
            update_report_data(db,report_number,"error_count")
            continue
        except requests.exceptions.InvalidURL:
            print("Invalid URL: " + current_page)
            searched.add(current_page)
            count += 1
            insert_report(current_page, parents[0], "Invalid URL", db, count)
            update_report_data(db,report_number,"error_count")
        searched.add(current_page)
        if domain not in current_page:
            print(current_page + " not contained in domain: " + domain)
            continue
        plain_text = response
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
            elif href[0:10] == 'javascript':
                break
            else:
                puppies = start_page + href
            to_search = [puppies] + to_search
            parents = [current_page] + parents
        update_report_data(db,report_number,"page_count")
    update_report_data(db,report_number,"end_time")


def insert_report(url, parent, error_type,db, error_number):
    report = {"report_number": 1,
              "error_number": error_number,
              "url": url,
              "parent_url": parent,
              "error_type": error_type}
    Reports = db.Reports
    reports_id = Reports.insert(report)
    reports_id

def insert_report_data(db, report_number, error_count, page_count, start_time, end_time):
    report_data = {"report_number": report_number,
                   "error_count": error_count,
                   "page_count": page_count,
                   "start_time": start_time,
                   "end_time": end_time }
    reports_data = db.Report_Data
    report_data_id = reports_data.insert(report_data)
    report_data_id

def update_report_data (db, report_number, update_type):
    report_data = db.Report_Data
    if update_type is "error_count":
        report_data.update({'report_number': report_number}, {'$inc': {'error_count': 1}})
    elif update_type is "page_count":
        report_data.update({'report_number': report_number}, {'$inc': {'page_count': 1}})
    else:
        end_time = str(datetime.utcnow().date()) + " / "
        end_time += str(datetime.utcnow().time())
        report_data.update({'report_number': report_number}, {'$set': {'end_time': end_time }})

crawler("spsu.edu/")
