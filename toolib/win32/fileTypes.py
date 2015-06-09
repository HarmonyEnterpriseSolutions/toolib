"""

TODO: 
	User can't even read registry if has no DEFAULT_ACCESS

"""
from toolib.win32.registry import *
import win32con
import os, sys

def register(
		document_extensions,
		open_script,
		icon_source=None,
		icon_index=0,
		project_path=None,
		document_name=None,
	):

	if not document_name:
		document_name = document_extensions[0][1:] + "file"

	for ext in document_extensions:
		key = RegKey(None, "HKEY_CLASSES_ROOT\\"+ext, create=1)
		key.value("").setValueIfChanged(document_name)
		key.close()

	key = RegKey(None, "HKEY_CLASSES_ROOT\\"+document_name, create=1)
	key.value("").setValueIfChanged("Excel Bookmarks Document")
	key.value("EditFlags").setValueIfChanged('\0\0\0\0', win32con.REG_BINARY)

	if icon_source:
		if not os.path.isabs(icon_source):
			icon_source = os.path.join(project_path, icon_source)
		hkDefaultIcon = RegKey(key, "DefaultIcon", create=1)
		hkDefaultIcon.value("").setValueIfChanged("%s,%s" % (icon_source, icon_index))
		hkDefaultIcon.close()

	hkShell = RegKey(key, "Shell", create=1)
	hkShell.value("").setValueIfChanged("open")

	hkOpen = RegKey(hkShell, "open", create=1)
	hkOpen.value("EditFlags").setValueIfChanged('\1\0\0\0', win32con.REG_BINARY)

	hkCommand = RegKey(hkOpen, "command", create=1)

	if not os.path.isabs(open_script):
		open_script = os.path.join(project_path, open_script)

	ext = os.path.splitext(open_script)[1].lower()

	if ext in ('.py', '.pyc', '.pyo'):
		pythonw = os.path.join(sys.prefix, "pythonw.exe")
		options = ['']
		if ext == '.pyo': options.append('-OO')
		open_script = '"%s"%s "%s"' % (pythonw, ' '.join(options), open_script)
	else:
		open_script = '"%s"' % (open_script,)

	hkCommand.value("").setValueIfChanged(open_script + ' "%1"')
	hkCommand.close()

	hkOpen.close()
	hkShell.close()

	key.close()


def unregister(document_extensions):
	doc_names = {}

	HKCR = RegKey(None, "HKEY_CLASSES_ROOT")

	for ext in document_extensions:
		try:
			key = RegKey(HKCR, ext)
			doc_names[key.getDefaultValue()] = None
			key.remove()
			key.close()
		except KeyError:
			pass

	for doc_name in doc_names.keys():
		if doc_name:
			try:
				key = RegKey(HKCR, doc_name)
				key.remove()
				key.close()
			except KeyError:
				pass

if __name__ == '__main__':
	unregister(('.xb',))
	#register(
	#   ('.xb',),
	#   "py\\xlbookmarks\\main.pyc",
	#   "py\\xlbookmarks\\res\\images\\xlbm_doc.bmp",
	#
	#   project_path = "z:\\rata")

