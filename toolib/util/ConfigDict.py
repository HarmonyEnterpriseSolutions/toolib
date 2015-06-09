from OrderDict import OrderDict

__all__ = ['dictrepr', 'ConfigDict']

class ConfigDict(OrderDict):
	"""
	Order dict, but inits from tuple of tuples
	"""
	def __init__(self, data):
		OrderDict.__init__(self)
		for t in data:
			try:
				key, value, default = t
			except ValueError:
				key, value = t
				default = NotImplemented
			if value != default:
				self[key] = value

	def __dictrepr__(self):
		return self

def dictrepr(obj):
	if hasattr(obj, '__dictrepr__'):
		return obj.__dictrepr__()
	else:
		assert False, 'Object has no __dictrepr__ method'