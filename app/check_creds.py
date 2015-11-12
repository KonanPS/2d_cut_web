# -*- coding: utf-8 -*-
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

    print 'QUERY_STRING: ', qs

    if qs:
        qs_dict = parse_qs(qs)

        print 'qs_dict: ', qs_dict

    else:
        return [b'No parameters']

    print 'username: ', qs_dict['username']
    print 'password: ', qs_dict['password']

    c.execute('''SELECT username, password FROM creds WHERE username=? ''', (qs_dict['username'][0],))
    sel_res = c.fetchone() # vs. fetchmany. username must be unique

    # start_response('2000 OK', [('Content-Type','text/html')])
    #     return [sel_res]
    
    print 'sel_res: ', sel_res

    if sel_res and sel_res[1] == qs_dict['password'][0]:

        #session. generates and stores cookies
        import time
        s_token = qs_dict['username'][0] + '_' + str(time.time())
        c.execute('''UPDATE creds SET session_token=? WHERE username=? ''', (s_token, qs_dict['username'][0]))
        conn.commit()
        conn.close()
        #session.

        template_file = open('../templates/pallet_spec.html', 'r')
        tmp = template_file.readlines()
        res = Template(''.join(tmp))
        template_file.close()

        cook_val = 'sessionToken=' + s_token
        start_response('200 OK', [('Content-Type','text/html'),('Set-Cookie',cook_val)])
        return [res.substitute(username=qs_dict['username'][0], some_text='Введите данные для рассчет', button_name='Раcсчитать')]
        
    else:
        conn.close()

        template_file = open('../templates/failed_login.html', 'r')
        tmp = template_file.readlines()
        #res = ''.join(tmp)
        template_file.close()

        start_response('2000 OK', [('Content-Type','text/html')])
        return tmp