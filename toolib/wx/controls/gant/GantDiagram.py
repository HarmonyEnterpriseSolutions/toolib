import wx
import wx.lib.ogl as ogl


class GantDiagram(ogl.Diagram):

	def __init__(self, model):
		super(GantDiagram, self).__init__()
		self._model = model

	def Redraw(self, dc):
		canvas = self.GetCanvas()

		dc.SetPen(wx.BLACK_PEN)
		dc.SetFont(ogl._basic.NormalFont)

		sf = self._model.getScaleFactor()
		w, h = canvas.Size

		i = 0
		while 1:
			x = canvas.borderLeft + canvas.getDx() * i
			time = i * sf

			if x < w:
				if time % 60 == 0:
					dc.DrawLine(x-1, 0, x-1, canvas.scaleHeight3)
					dc.DrawLine(x,   0, x,   canvas.scaleHeight3)
					dc.DrawLine(x+1, 0, x+1, canvas.scaleHeight3)
					dc.DrawText(self.getTimeText(time, 0), x + 3, canvas.scaleHeight3-12)

				elif time % 10 == 0:
					dc.DrawLine(x,   0, x,   canvas.scaleHeight2)
					dc.DrawText(self.getTimeText(time, 2), x + 3, canvas.scaleHeight2-12)
				
				else:
					dc.DrawLine(x, 0, x, canvas.scaleHeight1)
				i += 1
			else:
				break

		super(GantDiagram, self).Redraw(dc)

	def getTimeText(self, time, level):
		return ' '.join([
			'%s%s' % (x, name) 
			for (x, name) in (
				(time / 60 / 24, 'd'), 
				(time / 60 % 24, 'h'), 
				(time % 60,      'm'),
			)[level:]
			if x
		]) or '0'

if __name__ == '__main__':
	from test import test
	test()
