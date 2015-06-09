import wx
from TColumnExtraWidth import TColumnExtraWidth


class XColumnExtraWidth(TColumnExtraWidth):
	
	def __init__(self, *args, **kwargs):
		super(XColumnExtraWidth, self).__init__(*args, **kwargs)

		self.Bind(wx.EVT_SIZE, self.__on_size)
		self.__prevWidth = 0
		self.__in_on_size = False

	def __on_size(self, event):
		if not self.__in_on_size:
			self.__in_on_size = True
			#rint self._gfTable.block, event.GetSize()
			width = event.GetSize()[0]
			if width > self.__prevWidth:
				self.distributeExtraWidth(getattr(self.GetTable(), 'getBaseDataCol', lambda: 0)())
				self.__prevWidth = width
			self.__in_on_size = False
		event.Skip()
