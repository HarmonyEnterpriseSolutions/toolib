import wx
try: _
except: _ = lambda s: s

class ClipboardError(Exception):
	_('ClipboardError')
	pass


class TClipboardDataObject(object):
	"""
	successor class must be wx.DataObject
	and have getData method
	and have constructor from data
	"""

	@classmethod
	def setClipboardData(cls, data):

		if not wx.TheClipboard.Open():
			raise ClipboardError, _("Can't open clipboard")
		
		wx.TheClipboard.SetData(cls(data))
		wx.TheClipboard.Close()

	@classmethod
	def getClipboardData(cls):

		if not wx.TheClipboard.Open():
			raise ClipboardError, _("Can't open clipboard")

		dataObject = TableDataObject()
		wx.TheClipboard.GetData(dataObject)

		try:
			return dataObject.getData()
		finally:
			wx.TheClipboard.Close()


class TableDataObject(wx.TextDataObject, TClipboardDataObject):
	
	def __init__(self, table=None):
		wx.TextDataObject.__init__(self)
		if table:
			text = u'\r\n'.join([
				'\t'.join(row)
				for row in table
			]) + '\r\n'

			# if wxPython is non-unicode we have problem with encoding when language set to en
			self.SetText(text)

	def getData(self):
		text = self.GetText()
		if text.endswith('\r\n'):
			text = text[:-2]
		return clipboard_join_newlines([row.split('\t') for row in text.split('\r\n')])


def clipboard_join_newlines(data):

	filtered = False
	for i, row in enumerate(data):
		if row is not None:

			while True:

				last_value = row[-1]

				if not last_value.startswith('"'):
					break
				
				# check string is only starts with " and have only ""quoted"" quotes
				if '"' in last_value[1:].replace('""', ''):
					break

				chunks = [last_value[1:]]
				
				d = 1

				while True:
					try:
						next_row = data[i+d]
					except:
						chunks = None
						break

					if next_row is None:
						d += 1
						continue

					# this is chunk
					if len(next_row) == 1 and '"' not in next_row[0].replace('""', ''):
						# suspecting multiple nl in value
						chunks.append(next_row[0].replace('""', '"'))
						d += 1
						continue

					try:
						next_value = next_row[0]
					except:
						chunks = None
						break
	
					if not next_value.endswith('"'):
						chunks = None
						break
					
					if '"' in next_value[:-1].replace('""', ''):
						chunks = None
						break

					chunks.append(next_value[:-1].replace('""', '"'))
					break

				if chunks:
					data[i] = data[i][:-1] + ['\n'.join(chunks).replace('""', '"')] + data[i+d][1:]

					for c in range(i+1, i+1+d):
						data[c] = None
					
					filtered = True

				else:
					break

	if filtered:
		data = [row for row in data if row is not None]

	return data	


if __name__ == '__main__':

	data = [
		['1', '2', '3'],
		['1', '"2'],
		['a'],
		['hello ""b"" darling'],
		['c"', "3"],
		['1', '2', '3'],
	]


	data = [
		[u'"JC66-00600A-Foshan'], 
		[u'"', u'"Foshan-Yat-Sing Samsung ML1510'], 
		[u'"', u'1', u'10,99', u'17,00', u'qwe'],
	]

	for i in clipboard_join_newlines(data):
		print i

