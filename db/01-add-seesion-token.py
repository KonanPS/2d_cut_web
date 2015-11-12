import sqlite3

conn = sqlite3.connect('my_test_app.db')
c = conn.cursor()

c.execute('''ALTER TABLE creds ADD session_token text''')

conn.commit()
conn.close()