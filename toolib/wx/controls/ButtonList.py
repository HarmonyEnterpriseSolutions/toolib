import wx

class ButtonList(wx.Panel):
	
	def __init__(self, parent, *args, **kwargs):
		self.__style = kwargs.pop('style', 0)
		self.__gap = kwargs.pop('gap', 5)
		super(ButtonList, self).__init__(parent, *args, **kwargs)
		self.__buttons = []
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.Bind(wx.EVT_BUTTON, self.onButton)

	def onButton(self, event):
		print event.GetEventObject().GetLabel()



	def Append(self, item, clientData=None):
		"""
		Adds the item to the control, associating the given data with the item if not None.
		"""
		button = wx.Button(self, -1, item, style=self.__style)
		button._clientData_ = clientData
		self.GetSizer().Add(button, 0, wx.EXPAND | wx.TOP, self.__gap if self.__buttons else 0)
		self.GetSizer().Layout()
		self.__buttons.append(button)

	def AppendItems(self, strings):
		"""
		Apend several items at once to the control.
		"""
		for s in strings:
			self.Append(s)

	def Clear(self):
		"""
		Removes all items from the control.
		"""
		for i in xrange(self.GetCount()-1,-1,-1):
			self.Delete(i)

  	def Delete(self, n):
		"""Deletes the item at the zero-based index 'n' from the control."""
		button = self.__buttons[n]
		del self.__buttons[n]
		self.GetSizer().Remove(button)
		button.Destroy()

	def FindString(self, s):
		"""Finds an item whose label matches the given string."""
		for i, b in enumerate(self.__buttons):
			if b.GetLabel() == s:
				return i
		return -1

	def getButtonAt(self, index):
		return self.__buttons[index]

	def getButtons(self):
		return self.__buttons

	def getButtonIndex(self, button):
		return self.__buttons.index(button)

	def GetClientData(self, n):
		"""Returns the client data associated with the given item, (if any.)"""
		return self.__buttons[n]._clientData_

	def GetCount(self):
		"""Returns the number of items in the control."""
		return len(self.__buttons)

	def GetItems(self):
		"""Return a list of the strings in the control"""
		return [b.GetLabel() for b in self.__buttons]

	def GetSelection(self):
		"""Returns the index of the selected item or wx.NOT_FOUND if no item is selected."""
		return wx.NOT_FOUND

	def GetString(self, n):
		"""Returns the label of the item with the given index."""
		return self.__buttons[n].GetLabel()

	def GetStrings(self):
		return self.GetItems()

	def GetStringSelection(self):
		"""Returns the label of the selected item or an empty string if no item is selected."""
		return ""

	def Insert(self, item, pos, clientData=None):
		"""Insert an item into the control before the item at the pos index, optionally associating some data object with the item."""
		button = wx.Button(self, -1, item, style=self.__style)
		button._clientData_ = clientData
		self.__buttons.insert(pos, button)
		self.GetSizer().Insert(pos, button, 0, wx.EXPAND | wx.TOP, self.__gap)# if pos > 0 else 0)
		
	def IsEmpty(self):
		"""Returns True if the control is empty or False if it has some items."""
		return bool(self.__buttons)

	def Select(self, n):
		"""This is the same as SetSelection and exists only because it is slightly more natural for controls which support multiple selection."""
		pass

	def SetClientData(self, n, clientData):
		"""Associate the given client data with the item at position n."""
		self.__buttons[n]._clientData_ = clientData

	def SetItems(self, items):
		"""Clear and set the strings in the control from a list"""
		for i, s in enumerate(items):
			try:
				self.__buttons[i].SetLabel(s)
				self.__buttons[i]._clientData_ = None
				print "change", i
			except IndexError:
				self.Append(s)
				print "append", i

		for i in xrange(len(self.__buttons) - 1, len(items) - 1, -1):
			self.Delete(i)
			print "remove", i

	def SetSelection(self, n):
		"""Sets the item at index 'n' to be the selected item."""
		pass

	def SetString(self, n, s):
		"""Sets the label for the given item."""
		self.__buttons[n].SetLabel(s)


if __name__ == '__main__':

	from wx import TextCtrl
	
	def test():
		def oninit(self):
			self.Size = 800, 600
			self.c = ButtonList(self, -1, style=wx.NO_BORDER)
			#self.c.Append("One")
			#self.c.Insert("Two", 0)
			self.c.SetItems(['111111111111111111111111111111111111111', '22222222222', '3', '4', '5'])
			self.c.Fit()

		def ondestroy(self):
			pass

		def ontimer(self):
			#self.n2.SetSelection(-1,-1)
			#self.n2.SetFocus()
			#self.c.Clear()
			if self.c.GetCount() == 5:
				self.c.SetItems(['3'*20, '4'*100, '5'])
			else:
				self.c.SetItems(['4', '5'*100, '6'*50, '7', '8', '9'])
			self.c.Fit()

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()
	
	test()
