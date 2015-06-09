import wx
import sys
import traceback
import weakref
import re

CallAfter = wx.CallAfter

QUIET_ERRORS = (
	(
		wx.PyDeadObjectError, 
		re.compile("""The C\+\+ part of the NumCtrl object has been deleted\, attribute access no longer allowed"""),
	),
)

def CallAfterSafe(callable, *args, **kwargs):
	def f():
		try:
			callable(*args, **kwargs)
		except (wx.PyDeadObjectError, weakref.ReferenceError, TypeError):
			et, e, tb = sys.exc_info()

			for errorType, regexp in QUIET_ERRORS:
				if isinstance(e, errorType) and regexp.match(str(e)):
					return

			# expected TypeError: in method 'TextCtrl_SetSelection', expected argument 1 of type 'wxTextCtrl *'
			# do not suppress other errors
			if et is TypeError and 'expected argument 1 of type' not in str(e):
				raise

			print ''.join(['Warning: traceback in wx.CallAfter:\n'] + traceback.format_list(traceback.extract_tb(tb, 2)[1:]) + traceback.format_exception_only(et, e))
	
	CallAfter(f)

wx.CallAfter = CallAfterSafe
