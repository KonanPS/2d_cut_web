def application(env, start_response):

    import re
    import check_creds, index

    urls = [(r'^$', index.index),
            (r'^login\?.*', check_creds.check_creds)
            ]

    path = env.get('PATH_INFO', '').lstrip('/')
    print path
    for regex, callback in urls:

        match = re.search(regex, path)

        if match is not None:
            return callback(env, start_response)

    start_response('200 OK', [('Content-Type','text/html')])  

    return [b'Something wrong!']

    # if env.get('PATH_INFO','') == '/login':
    # 	qs_dict = parse_qs(env.get('QUERY_STRING',''))
    # 	return check_creds(qs_dict[username], qs_dict[password])

    # s = ''
    # for item in env.items():
    #     s = s + str(item) + '<br>'

    # start_response('200 OK', [('Content-Type','text/html')])

    # return [s]
