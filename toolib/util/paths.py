import re
import os

SEP = os.path.sep
SEPS = '\\/'


def reCompileFilePattern(fmask):
	"""
	@param fmask: file mask with '*?' characters
    @return: compiled regexp
	"""
	return re.compile(re.escape(fmask).replace('\\*', '.*').replace('\\?', '.') + '$')


def correctSep(path):
	"""
	replaces other separators with os.path.sep
	removes repeated separators
	"""
	for sep in SEPS:
		if sep != SEP:
			path = path.replace(sep, SEP)

	oldPath = None

	while oldPath != path:
		oldPath = path
		path = path.replace(SEP*2, SEP)
		
	return path


def iterFilePaths(path, fmask=None, recursive=True, dirs=False, exclude_fmask=None):
	"""
	@param path: 'dir\**\*?.ext' or 'dir' if fmask defined
	@param fmask: '*?.ext' or compiled regexp
	@param recursive: boolean
	@return: generator of file paths
	"""
	path = correctSep(path)

	if fmask is None:
		try:
			path, fmask = path.split(SEP + '**' + SEP)
			recursive = True
		except ValueError:
			path, fmask = os.path.split(path)
			recursive = False

	if isinstance(fmask, basestring):
		fmask = reCompileFilePattern(fmask)
	
	if isinstance(exclude_fmask, basestring):
		exclude_fmask = reCompileFilePattern(fmask)

	def _iter(dir):

		for i in os.listdir(dir):
			if exclude_fmask is not None and exclude_fmask.match(i):
				continue

			path = os.path.join(dir, i)
			if recursive and os.path.isdir(path):
				for i in _iter(path):
					yield i
			if (dirs or not os.path.isdir(path)) and fmask.match(i):
				yield path

	return _iter(path)
