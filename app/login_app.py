def login_app(env, start_response):

	import re

    ulrs = [(r'^$', index),
            (r'^login\?.*', check_creds)
            ]

    path = env.get('PATH_INFO', '').lstrip()

    for regex, callback in urls:

        match = re.search(regex, path)

        if match is not None:
            return callback(env, start_response)

    # if env.get('PATH_INFO','') == '/login':
    # 	qs_dict = parse_qs(env.get('QUERY_STRING',''))
    # 	return check_creds(qs_dict[username], qs_dict[password])

    # s = ''
    # for item in env.items():
    #     s = s + str(item) + '<br>'

    # start_response('200 OK', [('Content-Type','text/html')])

    # return [s]
