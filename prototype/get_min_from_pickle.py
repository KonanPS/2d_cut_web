import pickle, copy, os

min_residue = float('inf')

cwd = os.getcwd()

files_in_cwd = os.listdir(cwd)

for f in files_in_cwd:
	r = 0

	try:
		l = pickle.load(open(f, 'rb'))
	except:
		continue

	print f

	for e in l[1:]:
		r += e[1]

	if r <= min_residue:
		min_residue = r
		best = copy.deepcopy(l)

print 'Best residue: %s' % min_residue
print 'Best combi: %s' % best