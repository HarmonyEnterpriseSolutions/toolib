import sys
import wx
import win32com.client
from toolib import debug


class UserControlExcelApplication(object):

	def __init__(self, parent):
		"""
		needs wx parent window to setup timer to break references to bad excel
		"""
		self.__dict__['_excelApp'] = None
		self.__dict__['_running'] = True
		self.__dict__['wasVisible'] = False
		
		self.__dict__['_timer'] = wx.Timer(parent, -1)
		self.__dict__['_timer'].Start(200)
		parent.Bind(wx.EVT_TIMER, self._OnTimer)

	def _getExcelApplication(self):
		if self.__dict__['_excelApp'] is None:
			self.__dict__['_excelApp'] = win32com.client.DispatchEx("Excel.Application")
		return self.__dict__['_excelApp']

	def __getattr__(self, name):
		return getattr(self._getExcelApplication(), name)

	def __setattr__(self, name, value):
		setattr(self._getExcelApplication(), name, value)

	def close(self):
		self.__dict__['_excelApp'] = None

	def _OnTimer(self, event):
		"""
		Null reference if excel was visible and then become invisible. 
		It means user closed it
		"""
		if self.__dict__['_excelApp'] is not None:
			try:
				visible = self.__dict__['_excelApp'].Visible
			except:
				visible = False
			if self.__dict__['wasVisible'] and not visible:
				self.__dict__['_excelApp'] = None
				self.__dict__['wasVisible'] = False
				debug.trace("Excel becomes invisible, reference set to None")
			else:
				self.__dict__['wasVisible'] = visible
		else:
			self.__dict__['wasVisible'] = False
		

if __name__ == '__main__':
	from toolib import startup
	startup.hookStd()
	#import time
	#app = UserControlExcelApplication()
	#try:
	#	while 1:
	#		app.Visible = True
	#		time.sleep(10)
	#except KeyboardInterrupt:
	#	app.close()

	import weakref

	excel = win32com.client.DispatchEx("Excel.Application")	
	excel.Visible = True
	excel.UserControl = True

	sys.stdin.readline()

	print excel
	excel = weakref.ref(excel)
	print excel

