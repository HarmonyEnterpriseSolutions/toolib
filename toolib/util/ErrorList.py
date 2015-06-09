import sys

class ErrorList(list):

	def printStackTraces(self):
		for excinfo in self:
			sys.excepthook(*excinfo)


class ErrorRaiserList(object):
	
	def append(self, excinfo):
		raise excinfo[0], excinfo[1], excinfo[2]

ErrorRaiserList.instance = ErrorRaiserList()


if __name__ == '__main__':
	
	l = ErrorList()
	#l = ErrorRaiser.instance

	for i in xrange(3):
		try:
			1/0
		except:
			l.append(sys.exc_info())

	l.printStackTraces()
