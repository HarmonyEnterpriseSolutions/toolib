import inspect

def signature(function):
	"""
	returns a list for arguments, as in source code
	"""

	argnames, args, kwargs, defaults = inspect.getargspec(function)

	if defaults:
		ldefaults = len(defaults)
		sign = argnames[:-ldefaults]
	else:
		ldefaults = 0
		defaults = []
		sign = argnames

	for i in zip(argnames[-ldefaults:], defaults):
		sign.append('%s = %s' % i)

	if args:
		sign.append('*' + args)

	if kwargs:
		sign.append('**' + kwargs)

	return sign



if __name__ == '__main__':

	from gnue.forms.GFForm import GFForm

	print signature(GFForm.show_message)

	def x(a, b, *bazbaz, **ubladi):
		pass

	print signature(x)
