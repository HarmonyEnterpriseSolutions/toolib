import os
import wx
import wx.grid
import wx.calendar
import wx.lib.masked
import wx.aui

from toolib.dbg import introspection
from toolib.util import lang

def dump(module):
	try:
	    os.mkdir('index')
	except:
		pass
	for i in dir(module):
		c = getattr(module, i)
		if lang.isCastable(c, wx.Window):

			fname = str(c)[8:-2] + ".txt"
			if '._' in fname:
				fname = c.__name__ + ".txt"

			introspection.dump_class(c, file(fname, 'wt'))
			introspection.dump_class(c, file(os.path.join('index', fname), 'wt'), False)



if __name__ == '__main__':
	dump(wx)
	dump(wx.grid)
	dump(wx.calendar)
	dump(wx.lib.masked)
	dump(wx.aui)
