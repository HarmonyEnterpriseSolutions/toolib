"""
NumCtrl
	+ creation time localization
	* behaviour fixed:
		* HOME key sets cursor to first symbol
		* BACKSPACE does nothing if cursor at first symbol
		* LEFT AND UP can't go before first symbol
		* RIGHT AND DOWN go to first symbol if cursor is before (except Shift-DOWN)
"""

import wx
from wx.lib.masked import NumCtrl as BaseNumCtrl
import locale
locale.setlocale(locale.LC_ALL, "")

FLOAT_PRECISION = 16

class NumCtrl(BaseNumCtrl):
	"""
	localized numeric control
	"""
	
	__THOUSANDS_SEP_KEY = 'thousands_sep'
	ALLOW_NEGATIVE   = NotImplemented
	INTEGER_WIDTH    = NotImplemented
	FRACTION_WIDTH   = NotImplemented

	@classmethod
	def updateDefaultParams(cls, args, kwargs, defaultParams=None):
		#print "------------------------"
		#print locale.getlocale()
		#for k, v in locale.localeconv().iteritems():
		#	print k, repr(v)

		thsep = locale.localeconv()[cls.__THOUSANDS_SEP_KEY]

		params = {
			'groupDigits'   : bool(thsep),
			'allowNegative' : True,
			'decimalChar'   : locale.localeconv()['decimal_point'],
			'allowNegative' : cls.ALLOW_NEGATIVE,
			'integerWidth'  : cls.INTEGER_WIDTH,
			'fractionWidth' : cls.FRACTION_WIDTH,
		}

		if thsep:
			params['groupChar'] = thsep

		if defaultParams:
			params.update(defaultParams)

		for key, value in params.iteritems():
			if not kwargs.has_key(key) and value is not NotImplemented:
				kwargs[key] = params[key]

		return args, kwargs

	def __init__(self, *args, **kwargs):
		args, kwargs = self.updateDefaultParams(args, kwargs)
		BaseNumCtrl.__init__(self, *args, **kwargs)

		self.Bind(wx.EVT_CHAR, self.__onChar)

	def getHomePosition(self):
		v = super(BaseNumCtrl, self).GetValue()
		return len(v) - len(v.lstrip(' '))

	def __onChar(self, event):
		key = event.GetKeyCode()

		if key == wx.WXK_HOME:
			p = self.GetInsertionPoint()
			hp = self.getHomePosition()
			textCtrl = super(BaseNumCtrl, self)
			if event.ShiftDown() and hp < p:
				textCtrl.SetInsertionPoint(hp)
				textCtrl.SetSelection(p, hp)
			else:
				textCtrl.SetInsertionPoint(hp)
		elif key in (wx.WXK_LEFT, wx.WXK_UP):
			ip = self.GetInsertionPoint()
			hp = self.getHomePosition()
			if ip > hp:
				event.Skip()
			elif ip != hp:
				self.SetInsertionPoint(hp)
		elif key in (wx.WXK_RIGHT, wx.WXK_DOWN):
			if self.GetInsertionPoint() >= self.getHomePosition():
				event.Skip()
			else:
				# preserve Shift-Up and Shift-Down
				if event.ShiftDown() and key == wx.WXK_DOWN:
					event.Skip()
				else:
					self.SetInsertionPoint(self.getHomePosition())
		elif key == wx.WXK_BACK:
			if self.GetInsertionPoint() > self.getHomePosition():
				event.Skip()
		else:
			event.Skip()


class CurrencyControl(NumCtrl):
	"""
	positive localized currency control, not international
	INTEGER_WIDTH defaults to 16 - fractional width = 14
	"""
	
	__THOUSANDS_SEP_KEY = 'mon_thousands_sep'

	@classmethod
	def updateDefaultParams(cls, args, kwargs, defaultParams=None):

		params = {}

		frac = locale.localeconv()['frac_digits']
		# when locale is not set have 127, assume to 2
		if frac == 127:
			frac = 2

		if cls.FRACTION_WIDTH is NotImplemented: params['fractionWidth'] = frac
		if cls.INTEGER_WIDTH  is NotImplemented: params['integerWidth']  = FLOAT_PRECISION - frac

		if defaultParams:
			params.update(defaultParams)

		return IntControl.updateDefaultParams(args, kwargs, params)


# DEPRECATED

class IntControl(NumCtrl):
	"""
	positive int control
	deprecated.
	"""
	ALLOW_NEGATIVE = False



if __name__ == '__main__':

	from wx import TextCtrl
	
	def test():
		def oninit(self):
			self.panel = wx.Panel(self, -1)
			self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))

			self.n1 = TextCtrl(
				self.panel, 
				-1,
			)
			self.n2 = NumCtrl(
				self.panel, 
				-1,
				fractionWidth = 2,
			)
			self.n3 = IntControl(
				self.panel, 
				-1,
			)
			self.n4 = CurrencyControl(
				self.panel, 
				-1,
			)
			self.n5 = TextCtrl(
				self.panel, 
				-1,
			)

			self.panel.GetSizer().Add(self.n1)
			self.panel.GetSizer().Add(self.n2)
			self.panel.GetSizer().Add(self.n3)
			self.panel.GetSizer().Add(self.n4)
			self.panel.GetSizer().Add(self.n5)

			
		def ondestroy(self):
			pass

		def ontimer(self):
			#self.n2.SetSelection(-1,-1)
			#self.n2.SetFocus()
			pass

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()
	
	test()
