import wx.lib.customtreectrl


HITTEST_NAME = {}
for i in dir(wx.lib.customtreectrl):
	if i.startswith('TREE_HITTEST_') and i != 'TREE_HITTEST_ONITEM':
		HITTEST_NAME[getattr(wx.lib.customtreectrl, i)] = i
		#rint i, '%08X' % getattr(wx.lib.customtreectrl, i)
del i


TREE_HITTEST_IGNORED = (
	  wx.TREE_HITTEST_ONITEMUPPERPART 
	| wx.TREE_HITTEST_ONITEMLOWERPART
)

class XTips(object):
	"""
	Adds hit testing functionality to wx.grid.Grid

	Requires:
		getColLabelTipValue
	"""
	
	def __init__(self, *args, **kwargs):
		super(XTips, self).__init__(*args, **kwargs)
		#allowed = self.tipsAllowed()
		window = self.GetMainWindow() if hasattr(self, 'GetMainWindow') else self
		window.Bind(wx.EVT_MOTION, self.__onMotion, window)
		self.__lastHit = None

	#def tipsAllowed(self):
	#	return ('tree',)

	def hitTest(self, pos):
		#rint self.HitTest(pos)
		return list(self.HitTest(pos))

	def __onMotion(self, event):
		if not event.Dragging():
			hit = self.hitTest(event.GetPosition())

			hit[1] = hit[1] & ~TREE_HITTEST_IGNORED

			if hit != self.__lastHit:

				text = self.getTipValue(*hit)
					
				tip = event.GetEventObject().ToolTip
				if text:
					if tip:
						tip.SetTip(text)
					else:
						tip = event.GetEventObject().ToolTip = wx.ToolTip(text)
				elif tip:
						tip.SetTip("")

				self.__lastHit = hit

		event.Skip()

	def getTipValue(self, item, hit):
		names = [name for value, name in HITTEST_NAME.iteritems() if value & hit]
		names.sort()
		return "item=%s, hit=%s" % (item, '|'.join(names))
