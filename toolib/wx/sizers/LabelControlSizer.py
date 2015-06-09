import wx

class LabelControlSizer(wx.FlexGridSizer):

	def __init__(self, controlHost, gap = 10):
		self.__controlHost = controlHost
		self.__gap = gap
		wx.FlexGridSizer.__init__(self, -1, 2, 0, 0)
		self.AddGrowableCol(1, 0)


	def add(self, *args, **kwargs):
		return self.insert(-1, *args, **kwargs)

	def insert(self, position, id, label, control, validator=None):
		self.__controlHost.registerControl(id, control, validator, label)

		BORDER = wx.TOP | wx.LEFT | wx.RIGHT

		argsLabel = (wx.StaticText(control.GetParent(), -1, label or ''), 0, BORDER, self.__gap)
		argsControl = (control, 0, wx.GROW|BORDER, self.__gap)

		if position == -1:
			self.Add(*argsLabel)
			self.Add(*argsControl)
		else:
			self.Insert(position*2, *argsLabel)
			self.Insert(position*2+1, *argsControl)
	
if __name__ == '__main__':
	import sys
	sys.path.insert(0, 'z:\\projects\\rata\\py')

	from toolib.wx.dialogs.OkCancelDialog import OkCancelDialog
	from toolib.wx.util.ControlHost import ControlHost

	class TestDialog(ControlHost, OkCancelDialog):

		def __init__(self, *p, **pp):
			ControlHost.__init__(self)
			OkCancelDialog.__init__(self, *p, **pp)
		
		def createContentSizer(self):
			sizer = LabelControlSizer(self)

			sizer.add('a', 'aaa aa aasdfasdfasdfasdf', wx.TextCtrl(self, -1))
			sizer.add('b', 'aaa aa a', wx.TextCtrl(self, -1))
			sizer.add('c', 'aaa aa adsfffffffffffff', wx.TextCtrl(self, -1))
			sizer.insert(2, 'd', '!!! aa a', wx.TextCtrl(self, -1, 'hehehe'))

			print self.getLabel('a')

			return sizer


	class TestApp(wx.PySimpleApp):
		def OnInit(self):
			dlg = TestDialog(None, -1, "")
			dlg.ShowModal()
			dlg.Destroy()
			return True

	TestApp().MainLoop()

	