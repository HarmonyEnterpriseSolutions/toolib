import wx


class MultiRootTree(wx.TreeCtrl):
	"""
	internally has TR_HIDE_ROOT style
	but acts like tree without TR_HIDE_ROOT style
	except allows to add multiple root nodes
	"""

	def __init__(self, 
			parent,
			id        = -1,
			pos       = wx.DefaultPosition,
			size      = wx.DefaultSize,
			style     = wx.TR_DEFAULT_STYLE,
			**kwargs
		):
		assert not(style & wx.TR_HIDE_ROOT), 'TR_HIDE_ROOT style not supported (root already hiden)'
		super(MultiRootTree, self).__init__(parent, id, pos, size, style | wx.TR_HIDE_ROOT, **kwargs)
		self.__initRoot()

		# fixes issue when tree with TR_HIDE_ROOT style sends selection events on deletion
		parent = self
		while parent.GetParent(): parent = parent.GetParent()
		parent.Bind(wx.EVT_CLOSE, self.__onClose)

	def __onClose(self, event):
		try:
			self.SetEvtHandlerEnabled(False)
		except wx.PyDeadObjectError:
			pass
		event.Skip()

	def __initRoot(self):
		self.__rootItem = super(MultiRootTree, self).AddRoot("")

	def DeleteAllItems(self):
		self.SetEvtHandlerEnabled(False)
		rc = super(MultiRootTree, self).DeleteAllItems()
		self.SetEvtHandlerEnabled(True)
		self.__initRoot()
		return rc

	def IsEmpty(self):
		return not self.GetFirstChild(self.__rootItem)[0].IsOk()

	def AddRoot(self, text, image = -1, selectedImage = -1, data = None):
		return self.AppendItem(self.__rootItem, text, image, selectedImage, data)

	def GetRootItem(self):
		return self.GetFirstChild(self.__rootItem)[0]


if __name__ == '__main__':

	def test():

		def oninit(self):
			t = MultiRootTree(self)
			
			for i in xrange(3):
				root = t.AddRoot(str(i+1))
				for j in xrange(3):
					t.AppendItem(root, str((i+1)*10+j))

			t.Bind(wx.EVT_TREE_SEL_CHANGED, __onSelectionChanged)

		def __onSelectionChanged(event):
			t = event.GetEventObject()
			print "SEL CHANGED:", t.GetItemText(event.GetItem()), event.GetItem().IsOk()

		def ondestroy(self):
			pass

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy).MainLoop()


	def testBase():

		def oninit(self):
			self.t = t = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

			p = t

			while p.GetParent():
				p = p.GetParent()
			
			vroot = t.AddRoot("ROOT")

			for i in xrange(3):
				root = t.AppendItem(vroot, str((i+1)))
				for j in xrange(3):
					t.AppendItem(root, str((i+1)*10+j))

			t.Bind(wx.EVT_TREE_SEL_CHANGED, __onSelectionChanged)

		def __onSelectionChanged(event):
			t = event.GetEventObject()
			print "SEL CHANGED:", t.GetItemText(event.GetItem()), event.GetItem().IsOk()
			event.Skip()

		def ondestroy(self):
			pass

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy).MainLoop()


	test()

