"""
see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/305690
see http://tgolden.sc.sabren.com/python/win32_how_do_i/print.html

win32print.SetDefaultPrinter(printer_name)
win32api.ShellExecute(0, "print", file_path, None, ".", 0)

"""
import os
import socket
import win32print
import win32api

__all__ = ['Printers', 'PrinterNotFoundError']

class PrinterNotFoundError(Exception):
	pass


def getDefaultPrinterName():
	"""
	Get the default printer
	"""
	try:
		return win32print.GetDefaultPrinter()
	except RuntimeError, e:
		raise PrinterNotFoundError, str(e)


def getDefaultPrinterNetworkName():
	"""
	Constructs network name for default printer
	"""
	name = getDefaultPrinterName()
	if not name.startswith('\\\\'):
		return "\\\\%s\\%s"	% (socket.gethostbyname(socket.gethostname()), name)
		#return "\\\\%s\\%s"	% (socket.gethostname(), name)
	return name


def printRaw(raw_data, printer_name = None):
	if printer_name is None:
		printer_name = getDefaultPrinterName()

	hPrinter = win32print.OpenPrinter(printer_name)
	try:
		hJob = win32print.StartDocPrinter(hPrinter, 1, ("test of raw data", None, "RAW"))
		try:
			win32print.WritePrinter(hPrinter, raw_data)
		finally:
			win32print.EndDocPrinter(hPrinter)
	finally:
		win32print.ClosePrinter(hPrinter)


SHELL_ERRORS = {
	0  : (None, 'The operating system is out of memory or resources.'),
	5  : ('SE_ERR_ACCESSDENIED',    'The operating system denied access to the specified file.'),
	27 : ('SE_ERR_ASSOCINCOMPLETE', 'The file name association is incomplete or invalid.'),
	30 : ('SE_ERR_DDEBUSY',         'The DDE transaction could not be completed because other DDE transactions were being processed.'),
	29 : ('SE_ERR_DDEFAIL',         'The DDE transaction failed.'),
	28 : ('SE_ERR_DDETIMEOUT',      'The DDE transaction could not be completed because the request timed out.'),
	32 : ('SE_ERR_DLLNOTFOUND',     'The specified DLL was not found.'),
	2  : ('SE_ERR_FNF',             'The specified file was not found.'),
	31 : ('SE_ERR_NOASSOC',         'There is no application associated with the given file name extension. This error will also be returned if you attempt to print a file that is not printable.'),
	8  : ('SE_ERR_OOM',             'There was not enough memory to complete the operation.'),
	3  : ('SE_ERR_PNF',             'The specified path was not found.'),
	26 : ('SE_ERR_SHARE',           'A sharing violation occurred.'),
}

def shellExecutePrint(filename):
	"""
	only to default printer, weird 
	"""
	rc = win32api.ShellExecute(
		0,				# hwnd
		"print",		# lpOperation
		filename,		# lpFile
		None,			# lpParameters
		".",			# lpDirectory
		0				# nShowCmd
	)
	if rc <= 32:
		raise RuntimeError, "ShellExecute error " + ', '.join(filter(None, (str(rc),) + SHELL_ERRORS.get(rc, ())))
		

def printPdf(filename, printer=None, gsprint_path=None):
	if gsprint_path is None:
		gprint_path = os.path.abspath(__file__)
		for i in range(4):
			gprint_path = os.path.dirname(gprint_path)
		gprint_path = os.path.join(gprint_path, 'bin', 'gs', 'gsprint.exe')
	
	parameters = ['-dPDFFitPage']
	
	if printer:
		parameters.append('-printer %s' % printer)

	parameters.append(filename)

	command = "%s %s" % (gprint_path, ' '.join(parameters))

	os.system(command)


if __name__== "__main__":
	DATA = """%!PS-Adobe-2.0
%%Creator: cpierce1@ford.com
%%EndComments
/mainfont /Courier findfont 12 scalefont def
mainfont setfont
%%EndProlog
%%Page: ? 1
20 763 moveto
(Hello, World!) show
showpage
%%Pages: 1
"""

	#print getDefaultPrinterName()
	#print getDefaultPrinterNetworkName()
	#printRaw(DATA)

	printPdf(r'Z:\projects\wm\share\gnue\pdf\busy.pdf')
