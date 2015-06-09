from TextReportTemplate import TextReportTemplateBlock

"""
"""

class TextReport(object):
	
	def __init__(self, templateText, textFormatFactory):
		assert isinstance(templateText, basestring), repr(templateText)

		self._template = TextReportTemplateBlock(None, 'root', templateText, textFormatFactory)

	def format(self, data):
		iteratorClass = self.getIteratorClass()
		assert issubclass(iteratorClass, TextReportIterator), iteratorClass
		return self._template.format(iteratorClass(data), None)

	def getIteratorClass(self):
		raise NotImplementedError, 'abstract'


class TextReportIterator(object):

	def __init__(self, data):
		pass

	def nextRow(self, block):
		"""
		return dict with data
		or None, means end of block
		"""
		return None


