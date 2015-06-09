import pyodbc
import pymongo
from pymongo import MongoClient

# def database ():
client = MongoClient('localhost', 27017)
db = client.Reports_Database
collection = client.report_data
# report = {"report_number": 1,
#           "error_number": 1,
#           "url": "spsu.edu",
#           "parent_url": "spsu.edu",
#           "error_type": "404"}
report_data = db.report_data
report_data.update({'report_number': 1}, {'$inc': {'error_number': 1}})
print(report_data.find_one({'report_number': 2}))

# def update_report_number(db, report_number):
#
# # database()
# update_report_number(db, 1)
