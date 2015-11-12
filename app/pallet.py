# -*- coding: utf-8 -*-

from cgi import parse_qs, escape
from string import Template
import Cookie
import two_d_cut_web
import sqlite3

def pallet(env, start_response):
    template_file = open('../templates/pallet_spec.html', 'r')
    tmp = template_file.readlines()
    res = Template(''.join(tmp))
    template_file.close()

    cook = Cookie.SimpleCookie()
    cook.load(env.get('HTTP_COOKIE',''))
    s_token = cook["sessionToken"].value

    # NOT DRY
    conn = sqlite3.connect('my_test_app.db')
    c = conn.cursor()
    c.execute('''SELECT username FROM creds WHERE session_token=? ''', (s_token,))
    sel_res = c.fetchone()
    # NOT DRY
    uname = sel_res[0]

    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    return [res.substitute(some_text='Введите данные для рассчет', button_name='Раcсчитать', username=str(uname))]

def count(env, start_response):
    request_body_size = int(env.get('CONTENT_LENGTH', 0))
    request_body = env['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    print d

    data_str = d.get('elements','')
    
    print 'debug', data_str

    if data_str:
        cuts, total_residue = two_d_cut_web.main(data_str = data_str[0])

        template_file = open('../templates/result_cuts.html', 'r')
        tmp = template_file.readlines()
        res = Template(''.join(tmp))
        template_file.close()

        start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])


        data = data_str[0].split()
        PALLET_LEN = int(data[0]) 

        s = ''
        for cut in cuts:
            s += str(cut) + ' Остаток: ' + str(PALLET_LEN - sum(cut)) + '<br>'

        return[res.substitute(pallet_len=PALLET_LEN, cuts=s, total_residue=total_residue)]

    else:
        start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
        return['Enter data!']


    start_response('200 OK', [('Content-Type','text/html; charset=utf-8')])
    return ['Parsed!']

