import wx
import wx.lib.ogl as ogl


class LinkShape(ogl.LineShape):

	def __init__(self, canvas, link):
		self.canvas = canvas
		self.__link = link
		ogl.LineShape.__init__(self)
		#self.SetCanvas(canvas)

		#line.SetPen(wx.BLACK_PEN)
		#line.SetBrush(wx.BLACK_BRUSH)
		self.AddArrow(ogl.ARROW_ARROW)
		self.MakeLineControlPoints(3)

		self._updateX()
		self._updateY()

		#shapeActivityFrom.AddLine(self, shapeActivityTo)

	def _updateX(self):
		#rint '*** _updateX', self, self.canvas.getDx()

		a1 = self.canvas._getShape(self.__link.getActivityFrom())
		a2 = self.canvas._getShape(self.__link.getActivityTo())
		p1, p2, p3 = self.GetLineControlPoints()
		
		p1[0] = a1.GetX() + a1.GetWidth() / 2.
		p2[0] = p3[0] = a2.GetX() - a2.GetWidth() / 2. + self.canvas.getDx() / 3.
		

	def _updateY(self):
		a1 = self.canvas._getShape(self.__link.getActivityFrom())
		a2 = self.canvas._getShape(self.__link.getActivityTo())
		p1, p2, p3 = self.GetLineControlPoints()
		
		p1[1] = p2[1] = a1.GetY()
		p3[1] = a2.GetY() + a2.GetHeight() / 2. * (1 if a1.GetY() > a2.GetY() else -1)
		
	def getMaxPoint(self):
		return map(max, zip(*map(tuple, self.GetLineControlPoints())))

	def __str__(self):
		for o, s in self.canvas._shapes.iteritems():
			if s is self:
				return "<LinkShape %s>" % o
		return "<LinkShape>"


if __name__ == '__main__':
	from test import test
	test()
