# -*- coding: utf-8 -*-

def index(env, start_response):
	""" returns index page"""

	template_file = open('../templates/index.html', 'r')
	tmp = template_file.readlines()
	template_file.close()

	start_response('200 OK', [('Content-Type','text/html; charset=utf-8;')])
	
	return tmp