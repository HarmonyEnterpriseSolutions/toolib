"""
"""

def splitformat(pattern, d, splitter='~'):
	"""
	works like pyformat but excludes shunks delimited with splitter if at list one parameter
	if empty (None or '')
	"""
    # remove empty parameters from dict
	d = dict((item[0], unicode(item[1])) for item in d.iteritems() if item[1] not in (None, ''))
	return ''.join(filter(None, (_formatsafe(p, d) for p in pattern.split(splitter))))

def _formatsafe(p, d):
	try:
		return p % d
	except KeyError:
		return None

if __name__ == '__main__':
	print repr(splitformat('hello~ %(what)s world', { 'what' : 'dear' }))
	print repr(splitformat('hello~ %(what)s world', { 'what' : None }))
	print repr(splitformat('hello~ %(what)s world', { 'what' : '' }))
	print repr(splitformat('hello~ %(what)s world', { 'what' : 0 }))
