class MEvtHandlerUserData(object):
	"""
	Adds userData parameter to Connect
	
	hovever event.GetUserData() will still not work

	use self.getEventUserData(event)
	"""
	
	def Connect(self, id, lastId, eventType, func, userData = None):
		self.__dict__.setdefault('_MEvtHandlerUserData__userData', {})[id] = userData
		return super(MEvtHandlerUserData, self).Connect(id, lastId, eventType, func)

	def getEventUserData(self, event):
		return self.__dict__.setdefault('_MEvtHandlerUserData__userData', {}).get(event.GetId())


if __name__ == '__main__':
	
	class Window(object):
		def Connect(self, id, lastId, eventType, func):
			print "super connect!!!"


	class MyWindow(MEvtHandlerUserData, Window):
		pass


	w = MyWindow()

	w.Connect(-1, -1, 555, None, "user data")

