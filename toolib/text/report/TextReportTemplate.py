import re

REC_START = re.compile("""<!--\s*BLOCK\s+(\w+)\s*-->""", re.DOTALL)
RE_END =               """<!--\s*END\s+BLOCK\s+%s\s*-->"""


class TemplateFormatError(Exception):
	pass


class TextReportTemplate(object):

	def _addFields(self, set):
		raise NotImplementedError, 'abstract'


class TextReportTemplateText(TextReportTemplate):
	def __init__(self, text, textFormatFactory):
		self._format = textFormatFactory.newInstance(text)

	def dump(self, indent=0):
		print "%s%s" % ('\t' * indent, "TEXT")
		#print "[%s]" % self._text

	def _addFields(self, set):
		set.update(self._format.getFieldNames())

	def format(self, dataIteratorIgnored, row):
		"""
		dataIterator ignored
		"""
		return self._format.format(row)


class TextReportTemplateBlock(TextReportTemplate):
	"""
	block is list of template text and another blocks
	"""
	def __init__(self, parent, id, text, textFormatFactory):

		self._parent = parent
		self._id = id
		self._parts = []

		#print "PARSE", parentBlockId, text

		parts = []
		pos = 0

		while True:
			# search for block start
			matchStart = REC_START.search(text, pos)
			if matchStart:
				#print "START MATCH"

				# add first part
				preText = text[pos:matchStart.start()]
				if preText:
					self._parts.append(TextReportTemplateText(preText, textFormatFactory))

				groupId, = matchStart.groups()

				matchEnd = re.compile(RE_END % re.escape(groupId), re.DOTALL).search(text, matchStart.end())

				if matchEnd is None:
					raise TemplateFormatError("Block is not closed: %s" % groupId)

				blockText = text[matchStart.end():matchEnd.start()]
				#if blockText:
				self._parts.append(TextReportTemplateBlock(self, groupId, blockText, textFormatFactory))

				pos = matchEnd.end()

			else:
				# add last part
				postText = text[pos:]
				if postText:
					self._parts.append(TextReportTemplateText(postText, textFormatFactory))
				break


	def dump(self, indent=0):
		from toolib.util.lists import sorted
		print "%sBLOCK %s, parent=%s, %s" % ('\t' * indent, self._id, self._parent.getId() if self._parent else None, sorted(self.getFields()))
		for i in self._parts:
			i.dump(indent+1)

	def getFields(self):
		fields = set()
		for i in self._parts:
			i._addFields(fields)
		return tuple(fields)

	def getGroupingFields(self):
		fields = set()
		block = self.getParent()
		while block:
			fields.update(block.getFields())
			block = block.getParent()
		return tuple(fields)

	def _addFields(self, set):
		pass

	def format(self, dataIterator, rowIgnored=None):
		"""
		row ignored
		"""
		text = []
		while True:
			row = dataIterator.nextRow(self)
			if row:
				for part in self._parts:
					text.append(part.format(dataIterator, row))
			else:
				break
		return ''.join(text)
	
	def getId(self):
		return self._id

	def getParent(self):
		return self._parent

