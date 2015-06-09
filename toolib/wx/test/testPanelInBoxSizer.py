"""
Bug in ALT linux 2.8.6.1 build with python 2.5

Traceback in
	frame.GetSizer().Add(panel, 1, wx.EXPAND)

Wrong SWIG assertion that panel is not instance of correct class

"""
import wx

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = wx.Frame(None, -1, 'test frame')
	panel = wx.Panel(frame, -1)
	frame.SetSizer(wx.BoxSizer(wx.VERTICAL))
	frame.GetSizer().Add(panel, 1, wx.EXPAND)
	frame.Show()
	app.MainLoop()
