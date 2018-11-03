import sqlite3
dbPath="C:\\Users\\10134838\\Desktop\\prodDB.db" # path to product database
conn = sqlite3.connect(dbPath)
c=conn.cursor()
# create table: shelf life is in months
table='''CREATE TABLE if not exists products(catNum int, desc text, symbol text, shelfLife int, primary key (catNum))'''
c.execute(table)
# add a row to the table
c.execute("INSERT INTO products values (?,?,?,?)" , (515100,'PROTECTOR','P14',60))
c.execute("INSERT INTO products values (?,?,?,?)" , (515306, 'ADAPTER', 'C100', 48))
c.execute("INSERT INTO products values (?,?,?,?)" , (515003, 'INJECTOR', 'N35', 30))
c.execute("select * from products")
a=c.fetchone()
conn.commit()
conn.close()
