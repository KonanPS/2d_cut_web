def check_creds(env, start_response):

    from cgi import parse_qs, escape
    from string import Template

	'''
	takes env and start_response. Select password from db by username and compare it with specified.
	depending on results returns success or not page.
	'''
	import sqlite3
	
	conn = sqlite3.connect('my_test_app.db')
	c = conn.cursor()

	qs = env.get('QUERY_STRING', '')
	if qs:
		qs_dict = parse_qs(qs)
	else:
		return [b'No parameters']

	c.execute('''SELECT username, password FROM creds WHERE username=? ''', (escape(qs_dict['username']),))
	sel_res = c.fetchone() # vs. fetchmany. username must be unique
	
	if sel_res[1] == qs_dict['password']:

		conn.close()

		template_file = open('../templates/success_login.html', 'r')
		tmp = template_file.readlines()
		res = Template(''.join(tmp))
		template_file.close()

		return [res.substitute(escape(qs_dict['username']))]
		
	else:
		conn.close()

		template_file = open('../templates/failed_login.html', 'r')
		tmp = template_file.readlines()
		#res = ''.join(tmp)
		template_file.close()

		return tmp