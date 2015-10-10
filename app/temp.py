from string import Template

f = open('../templates/success_login.html', 'r')

username = 'Pavel'

tmp = f.readlines()
res = Template(''.join(tmp))

print res.substitute(username=username)