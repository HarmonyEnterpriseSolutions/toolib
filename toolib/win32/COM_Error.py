from toolib._ import *
import pywintypes

def hresult(e):
	hr = e[COM_Error.ID_HR]
	if hr < 0: hr += 0x100000000L
	return hr

class COM_Error(Exception):
	"""
        except pythoncom.com_error, (hr, msg, exc, arg):
            print "The Excel call failed with code %d: %s" % (hr, msg)
            if exc is None:
                print "There is no extended error information"
            else:
                wcode, source, text, helpFile, helpId, scode = exc
                print "The source of the error is", source
                print "The error message is", text
                print "More info can be found in %s (id=%d)" % (helpFile, helpId)
	"""

	ID_HR			= 0
	ID_MESSAGE		= 1
	ID_EXT			= 2
	ID_ARG			= 3

	IDX_WCODE		= 0
	IDX_SOURCE		= 1
	IDX_TEXT		= 2
	IDX_HELPFILE 	= 3
	IDX_HELPID		= 4
	IDX_CODE		= 5

	def __init__(self, com_error):
		Exception.__init__(self)

		assert isinstance(com_error, (pywintypes.com_error, tuple)) 

		self.args = tuple(com_error)
		
	def getHResult(self):
		return hresult(self)

	def getMessage(self):
		return self[self.ID_MESSAGE]
		
	def getSource(self):
		if not self[self.ID_EXT] is None:
			return self[self.ID_EXT][self.IDX_SOURCE]

	def getExtendedMessage(self):
		if not self[self.ID_EXT] is None:
			return self[self.ID_EXT][self.IDX_TEXT]

	# python			
	def getText(self):
		if self.getExtendedMessage():
			return "%s\n%s" % (self.getMessage(), self.getExtendedMessage())
		else:
			return self.getMessage()

	def __str__(self):
		hr = self.getHResult()
		text = self.getText()
		src = self.getSource()
		if src:
			return _("COM error 0x%8X in %s: %s") % (hr, src, text)
		else:
			return _("COM error 0x%8X: %s") % (hr, text)

if __name__ == '__main__':
	import sys
	import toolib.win32.excel as excel
	from toolib.startup import hookStd
	hookStd()

	def wrapError(error):
		if isinstance(error, pywintypes.com_error):
			return COM_Error(error)
		else:
			return error

	try:
		book = excel.ExcelBook('bebe')
	except Exception, e:
		raise wrapError(e)
