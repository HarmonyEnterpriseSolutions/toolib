class CatchOutput(object):

	def __init__(self, out, text):
		self.__out = out
		self.__text = text

	def write(self, text):
		if self.__text in text:
			raise Exception, text
		else:
			return self.__out.write(text)

	def __getattr__(self, name):
		return getattr(self.__out, name)


if __name__ == '__main__':
	import sys
	sys.stdout = CatchOutput(sys.stdout, 'bebe')
	print 'hello'
	print 'bebe'