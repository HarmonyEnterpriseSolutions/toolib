import wx
from GantModel import GantModel
from GantView import GantView


def test():

	def oninit(self):
		self.Size = 800, 600
		self.model = GantModel(1)
		self.view = GantView.createScrolledView(self, self.model)

		b = wx.Button(self, -1, "hello")
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.GetSizer().Add(self.view, 1, wx.GROW)
		self.GetSizer().Add(b)

		#self.model.createScale()

		a0 = self.model.addActivity(5, "a0 - veeeery long name")
		a1 = self.model.addActivity(7, "a1")
		#a2 = self.model.addActivity(9, "a2")
		#a3 = self.model.addActivity(3, "a3")

		a1.addPredecessor(a0)
		#a2.addPredecessor(a0)

		#a3.addPredecessor(a1)
		#a3.addPredecessor(a2)

		#a2.setRow(3)
		#a3.setRow(2)

		#for i in range(10):
		#	self.model.addActivity(3, "a3")

		#a0.remove()

		#a3.move(-2)
		#a0.move(2)


		#a0.getLinkTo(a2).remove()


			
	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
