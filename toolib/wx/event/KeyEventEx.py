"""
Note: setup locale before importing
"""

import wx
import locale


TRANSLATE_NUMPAD = {
	wx.WXK_NUMPAD_ADD       : wx.WXK_ADD,
	#wx.WXK_NUMPAD_BEGIN     : None,
	wx.WXK_NUMPAD_DELETE    : wx.WXK_DELETE,
	wx.WXK_NUMPAD_DIVIDE    : wx.WXK_DIVIDE,
	wx.WXK_NUMPAD_DOWN      : wx.WXK_DOWN,
	wx.WXK_NUMPAD_END       : wx.WXK_END,
	wx.WXK_NUMPAD_ENTER     : wx.WXK_RETURN,		# non trivial
	wx.WXK_NUMPAD_F1        : wx.WXK_F1,
	wx.WXK_NUMPAD_F2        : wx.WXK_F2,
	wx.WXK_NUMPAD_F3        : wx.WXK_F3,
	wx.WXK_NUMPAD_F4        : wx.WXK_F4,
	wx.WXK_NUMPAD_HOME      : wx.WXK_HOME,
	wx.WXK_NUMPAD_INSERT    : wx.WXK_INSERT,
	wx.WXK_NUMPAD_LEFT      : wx.WXK_LEFT,
	wx.WXK_NUMPAD_MULTIPLY  : wx.WXK_MULTIPLY,
	wx.WXK_NUMPAD_NEXT      : wx.WXK_NEXT,
	wx.WXK_NUMPAD_PAGEDOWN  : wx.WXK_PAGEDOWN,
	wx.WXK_NUMPAD_PAGEUP    : wx.WXK_PAGEUP,
	wx.WXK_NUMPAD_PRIOR     : wx.WXK_PRIOR,
	wx.WXK_NUMPAD_RIGHT     : wx.WXK_RIGHT,
	wx.WXK_NUMPAD_SEPARATOR : wx.WXK_SEPARATOR,
	wx.WXK_NUMPAD_SPACE     : wx.WXK_SPACE,
	wx.WXK_NUMPAD_SUBTRACT  : wx.WXK_SUBTRACT,
	wx.WXK_NUMPAD_TAB       : wx.WXK_TAB,
	wx.WXK_NUMPAD_UP        : wx.WXK_UP,
}

CODE_TO_CHAR = {
	wx.WXK_NUMPAD0          : '0',
	wx.WXK_NUMPAD1          : '1',
	wx.WXK_NUMPAD2          : '2',
	wx.WXK_NUMPAD3          : '3',
	wx.WXK_NUMPAD4          : '4',
	wx.WXK_NUMPAD5          : '5',
	wx.WXK_NUMPAD6          : '6',
	wx.WXK_NUMPAD7          : '7',
	wx.WXK_NUMPAD8          : '8',
	wx.WXK_NUMPAD9          : '9',

	# WHILE wxTextCtrl prints dot on wx.WXK_NUMPAD_DECIMAL here will remain dot
	wx.WXK_NUMPAD_DECIMAL   : '.', 	#locale.localeconv()['decimal_point'],
	wx.WXK_NUMPAD_EQUAL     : '=',
	
	wx.WXK_DIVIDE			: '/',
	wx.WXK_MULTIPLY			: '*',
	wx.WXK_SUBTRACT			: '-',
	wx.WXK_ADD				: '+',
}

class KeyEventEx(object):

	@staticmethod
	def getChar(event):
		"""
		1. translate numpad codes into keyboard
		2. translates known codes into chars
		"""
		code = event.GetKeyCode()
		code = TRANSLATE_NUMPAD.get(code, code)
		if code < 256:
			return chr(code)
		else:
			char = CODE_TO_CHAR.get(code)
			if char is None:
				return unichr(code)
			else:
				return char





if __name__ == '__main__':
	def dumpRESOLVE_NUMPAD():
		print "TRANSLATE_NUMPAD = {"
		for name in filter(lambda name: name.startswith('WXK_NUMPAD'), dir(wx)):
			value = None
			name2 = 'WXK' + name[len("WXK_NUMPAD"):]
			if hasattr(wx, name2):
				value = "wx." + name2
			print "\twx.%-20s : %s," % (name, value)
		print "}"


	def dumpUPPER():
		print "UPPER = {"
		for name in filter(lambda name: name.startswith('WXK_') and not name.startswith('WXK_NUMPAD'), dir(wx)):
			code = getattr(wx, name)
			value = None
			if code > 256:
				print "\twx.%-20s : %s," % (name, value)
		print "}"

	dumpRESOLVE_NUMPAD()
	dumpUPPER()
	