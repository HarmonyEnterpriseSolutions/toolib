import wx
import datetime
from Calendar import Calendar

GAP = 5

class Label(wx.Panel):

	def __init__(self, parent, cellAttributes, text=''):
		super(Label, self).__init__(parent, -1)
		self.__cellAttributes = cellAttributes
		self.__text = text
		self.Bind(wx.EVT_PAINT,        self.__onPaint)
		self.Bind(wx.EVT_SIZE,         self.__onSize)

	def setText(self, text):
		if self.__text != text:
			self.__text = text
			self.Refresh()

	def __onPaint(self, event):
		self.__cellAttributes.drawCell(wx.PaintDC(self), self.GetClientRect(), self.__text)

	def __onSize(self, evt):
		self.Refresh(False)
		evt.Skip()
		 

class CalendarPanel(wx.Panel):
	
	def __init__(self, parent, id = -1, style=0, model=None, cellAttributesDict=None):
		super(CalendarPanel, self).__init__(parent, id)

		if cellAttributesDict is None:
			import config
			cellAttributesDict = config.CELL_ATTRIBUTES_DICT

		self.SetSizer(wx.BoxSizer(wx.VERTICAL))

		buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.__buttons = [wx.Button(self, -1, "", style=wx.TAB_TRAVERSAL) for i in xrange(4)]

		#self.__label = wx.StaticText(self, -1, "", style=labelAttributes.textAlign if labelAttributes.textAlign is not None else wx.ALIGN_CENTER)
		self.__label = Label(self, cellAttributesDict['label'])
		self.__calendar = Calendar(self, -1, style=style, model=model, cellAttributesDict = cellAttributesDict)

		#if labelAttributes.font:		self.__label.SetFont(labelAttributes.font)
		#if labelAttributes.textColor:	self.__label.SetForegroundColour(labelAttributes.textColor)
		#if labelAttributes.bgColor:		self.__label.SetBackgroundColour(labelAttributes.bgColor)

		for b in self.__buttons[:2]:
			buttonsSizer.Add(b, 0, wx.RIGHT | wx.BOTTOM, GAP)
		
		buttonsSizer.Add(self.__label, 1, wx.BOTTOM | wx.GROW, GAP)
		
		for b in self.__buttons[2:]:
			buttonsSizer.Add(b, 0, wx.LEFT | wx.BOTTOM, GAP)

		self.GetSizer().Add(buttonsSizer, 0, wx.GROW)
		self.GetSizer().Add(self.__calendar, 1, wx.GROW)

		self._updateButtons()

		self.__buttons[0].Bind(wx.EVT_BUTTON, lambda event: self.__calendar.getModel().incMonth(-12))
		self.__buttons[1].Bind(wx.EVT_BUTTON, lambda event: self.__calendar.getModel().incMonth(-1))
		self.__buttons[2].Bind(wx.EVT_BUTTON, lambda event: self.__calendar.getModel().incMonth( 1))
		self.__buttons[3].Bind(wx.EVT_BUTTON, lambda event: self.__calendar.getModel().incMonth( 12))

		self.__calendar.getModel().listeners.bind("propertyChanged", self.__onPropertyChange)


	def getCalendar(self):
		return self.__calendar


	def __onPropertyChange(self, event):
		if event.propertyName == 'dateFirst':
			self._updateButtons()
			

	def _updateButtons(self):
		
		date = self.__calendar.getModel().getDate()
        
		self.__buttons[0].SetLabel("%s <<" % (date.year - 1))
		self.__buttons[3].SetLabel(">> %s" % (date.year + 1))

		self.__label.setText(date.strftime("%B %Y"))

		self.__buttons[1].SetLabel((date - datetime.timedelta(date.day)).strftime("%B <"))
		self.__buttons[2].SetLabel((date + datetime.timedelta(32 - date.day)).strftime("> %B"))


	def __getattr__(self, name):
		return getattr(self.__calendar, name)
	                   
		
def test():

	def oninit(self):
		self.Size = 800, 600
		c = CalendarPanel(self)
			
	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
