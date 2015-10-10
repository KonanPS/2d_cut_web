import sqlite3

conn = sqlite3.connect('my_test_app.db')
c = conn.cursor()

c.execute('''CREATE TABLE creds
             (date text, username text, password text)''')

c.execute('''INSERT INTO creds VALUES ('04-10-2015', 'admin', 'admin') ''')

conn.commit()
conn.close()
