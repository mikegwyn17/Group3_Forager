from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.Reports_Database

def insert_report(report_number, url, parent, error_type,db):
    report = {"report_number": report_number,
              "parent_url": parent,
              "errors": []}
    Reports = db.Reports
    reports_id = Reports.insert(report)
    Reports.update({'report_number': 1}, {'$push': {'errors': {'url': url, "error_type": error_type}}})
    reports_id
    taco = Reports.find_one({'parent_url': parent}, {'report_number': report_number})
    print(taco)
    if taco is None:
        print("tacos")

insert_report(1,"1","2","3",db)