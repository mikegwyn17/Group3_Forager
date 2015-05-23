import sqlite3

def database ():
    db = sqlite3.connect(":memory:")
    c = db.cursor()
    page = 'http://spu.edu/'
    page = str(page)
    # c.execute("DROP TABLE searched")
    c.execute("CREATE TABLE searched (link text)")
    sql = "INSERT INTO searched (link) VALUES (?)"
    c.execute(sql,(page,))
    db.commit()
    sql2 = "SELECT * FROM searched WHERE link = ?"
    c.execute(sql2,[(page)])
    temp = c.fetchone()
    print (temp[0])

database()