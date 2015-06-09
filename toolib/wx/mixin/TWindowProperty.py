
###################################################################
# Trait
#
class TWindowProperty(object):
	"""
	Requires:
		GetParent
	Provides:
		getParentWindowProperty
	"""
	def getParentWindowProperty(self, name, default=NotImplemented):
		"""
		looks for property in parent windows chain

		Note:
			parent delegates child window, 	to avoid recursion stack overflow

			define in parents class a method
				__delegator__(self)

			it must retunrn child it's delegates
			so parent will be skipped
		"""
		getter = 'get' + name[0].upper() + name[1:]
		w = self
		parent = self.GetParent()
		while parent:
			if hasattr(parent, getter) and (not hasattr(parent, '__delegator__') or parent.__delegator__() is not w):
				return getattr(parent, getter)()
			w = parent
			parent = w.GetParent()

		if default is NotImplemented:
			raise AttributeError, "Parent windows has no property '%s'" % name
		else:
			return default


	def getWindowProperty(self, name, default=NotImplemented):
		"""
		looks for property in window and it's parent chain

		Note:
			if parent delegates to a child window,
			to avoid recursion stack overflow

			define in parents class a method
				__delegator__(self)

			it must retunrn child it's delegates
			so this parent will be skipped
		"""
		w = self
		while w:
			if not hasattr(w, '__delegator__') or w.__delegator__().GetParent() is not w:

				if hasattr(w, name):
					return getattr(w, name)

				# deprecated
				getter = 'get' + name[0].upper() + name[1:]
				if hasattr(w, getter):
					return getattr(w, getter)()
			
			w = w.GetParent()

		if default is NotImplemented:
			raise AttributeError, "Window and it's parent chain has no property '%s'" % name
		else:
			return default
		

#################################################################
# Static
#
getParentWindowProperty = TWindowProperty.getParentWindowProperty
getWindowProperty = TWindowProperty.getWindowProperty
