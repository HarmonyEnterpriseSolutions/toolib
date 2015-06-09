import wx
from toolib 		import debug

class RadioBox(wx.RadioBox):
	"""
	wx.RadioBox with list functionality
	"""
	def __init__(self, *args, **kwargs):
		super(RadioBox, self).__init__(*args, **kwargs)
		self.__endPos = 0

	def SetValue(self, value):
		self.SetStringSelection(value)

	def Clear(self):
		self.__endPos = 0
		for i in xrange(self.GetCount()):
			self.EnableItem(i, False)
			self.SetItemLabel(i, "")
		self.SetSelection(0)

	def Append(self, value):
		if self.__endPos < self.GetCount():
			self.SetItemLabel(self.__endPos, value)
			self.EnableItem(self.__endPos, True)
			self.__endPos += 1
			return True
		else:
			debug.error("RadioBox is full. Can't Append")
			return False

if __name__ == '__main__':
	
	def test():
		def oninit(self):
			self.panel = wx.Panel(self, -1)
			self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))

			self.rb = RadioBox(
				self.panel, 
				-1,
				"Bebe", 
				majorDimension = 1,
				style = wx.RA_SPECIFY_COLS,
				choices = [' '] * 10,
			)

			self.panel.GetSizer().Add(self.rb, 1, wx.EXPAND)

			self.SetSize((self.GetSize()[0]+1, self.GetSize()[1]+1))

			self.rb.Clear()

			
		def ondestroy(self):
			pass

		def ontimer(self):
			if not self.rb.Append('Bebebebe'):
				self.rb.Clear()
			#self.panel.Refresh()
			#self.panel.Update()

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()
	
	test()
