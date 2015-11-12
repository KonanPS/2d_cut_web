import sqlite3

conn = sqlite3.connect('my_test_app.db')
c = conn.cursor()

s_token = '123adc'
username = 'admin'


c.execute('''SELECT username, password FROM creds WHERE username=? ''', (username,))
sel_res = c.fetchone()

print sel_res

c.execute('''UPDATE creds SET session_token=? WHERE username=? ''', (s_token, username))
conn.commit()

c.execute('''SELECT username FROM creds WHERE session_token=? ''', (s_token,))
sel_res = c.fetchone()

print sel_res[0]