''' Use this file to update the product database.
    The tbale field include:
    
         cat#,   Product description, Product code, Shelf life (in months)

    Example:        
         515100, PROTECTOR,           P14,         60

'''
import sqlite3

db_path = ""
conn = sqlite3.connect(db_path)
c = conn.cursor()
table = '''CREATE TABLE if not exists products(catNum text, desc text, code text, shelfLife int, primary key (catNum))'''
c.execute(table)
c.execute("INSERT INTO products values (?,?,?,?)" , ('515100','PROTECTOR','P14',60))
c.execute("INSERT INTO products values (?,?,?,?)" , ('515306', 'ADAPTER', 'C100', 48))
c.execute("INSERT INTO products values (?,?,?,?)" , ('515003', 'INJECTOR', 'N35', 30))
c.execute("INSERT INTO products values (?,?,?,?)" , ('515004', 'INJECTOR', 'N35C', 30))

conn.commit()
conn.close()

