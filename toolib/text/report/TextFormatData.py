class TextFormatData(object):

	def __init__(self, variables):
		self._variables = variables

	def get(self, name, default=None):
		return eval(name, {}, self._variables)
