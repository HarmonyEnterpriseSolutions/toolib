import wx
from toolib.wx.TestApp import TestApp
import wx.aui

class XNotebookTips(object):

	def __init__(self, *args, **kwargs):
		super(XNotebookTips, self).__init__(*args, **kwargs)

		self.Bind(wx.EVT_MOTION, self.__onLabelMotion)

		self.__lastIndex = None

	def __onLabelMotion(self, event):

		if not event.Dragging():

			x, y = event.GetPosition()

			index, where = self.HitTest((x, y))

			if self.__lastIndex != index:

				text = self.getTipValue(index)
					
				tip = event.GetEventObject().ToolTip
				if text:
					if tip:
						tip.SetTip(text)
					else:
						tip = event.GetEventObject().ToolTip = wx.ToolTip(text)
				elif tip:
					tip.SetTip("")

				self.__lastIndex = index

		event.Skip()




if __name__ == '__main__':

	class TestNotebook(XNotebookTips, wx.Notebook):

		def getTipValue(self, index):
			return "Tip %s" % (index + 1)

	def oninit(self):

		self.nb = TestNotebook(self, wx.ID_ANY)
		for i in xrange(5):
			page = wx.Button(self.nb, -1, 'test')
			self.nb.AddPage(page, "Page %s" % (i+1), True)
		
		self.nb.SetSelection(0)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
