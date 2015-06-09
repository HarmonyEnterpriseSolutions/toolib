import wx


class MMultiRootTree(object):
	"""
	internally has TR_HIDE_ROOT style
	but acts like tree without TR_HIDE_ROOT style
	except allows to add multiple root nodes
	"""

	def __init__(self):
		#assert self.GetWindowStyleFlag() & wx.TR_HIDE_ROOT, 'please, set TR_HIDE_ROOT style to Tree'
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
		self.__rootItem = super(MMultiRootTree, self).AddRoot("HIDDEN ROOT")

	def DeleteAllItems(self):
		self.SetEvtHandlerEnabled(False)
		rc = super(MMultiRootTree, self).DeleteAllItems()
		self.SetEvtHandlerEnabled(True)
		self.__initRoot()
		return rc

	def IsEmpty(self):
		return not self.GetFirstChild(self.__rootItem)[0].IsOk()

	def AddRoot(self, text, image = -1, selectedImage = -1, data = None):
		return self.AppendItem(self.__rootItem, text, image=image, selectedImage=selectedImage, data=data)

	# this is not compattible with CustomTreeCtrl
	def GetRootItem(self):
		return self.GetFirstChild(self.__rootItem)[0]


if __name__ == '__main__':

	class MultiRootTree(MMultiRootTree, wx.TreeCtrl):
		def __init__(self, parent):
			wx.TreeCtrl.__init__(self, parent, -1, style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
			MMultiRootTree.__init__(self)


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

