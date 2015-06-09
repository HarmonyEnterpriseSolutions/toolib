# -*- coding: Cp1251 -*-

import os
from cStringIO import StringIO
import tempfile
from datetime import datetime, time
from toolib import debug
import tuples_from_file
from toolib.util.iters import DictIterator, ensure_has_next, ExcelColumns

_PARSERS = {}

###############################################################################
# DBF
try:
	import ydbf
except ImportError:
	debug.warning("parsing DBF is not supported, please, install ydbf")
else:
	def parse_ydbf(fp, *args, **kwargs):

		if not hasattr(fp, 'read'):
			fp = StringIO(fp)

		return ydbf.open(fp, *args, **kwargs)

	_PARSERS['DBF'] = parse_ydbf
	del parse_ydbf


def parse_generic(format, fp_or_text, columns=None, **kwargs):
	records = ensure_has_next(tuples_from_file.parse(format, fp_or_text, **kwargs))
	if not columns:
		columns = records.next()
	return DictIterator(records, columns)


def parse(format, fp_or_text, **kwargs):
	"""
	fp_or_text: opened file of its content as str
	encoding: encoding to override [dbf]

	TODO: support csv, xls via tuples_from_file
	TODO: col_names: list column names. if None, first row may be used to get column names [csv, xls]
	TODO: sheet_index: sheet index [xls]
	"""
	#rint '>>> parse', repr(format), repr(fp_or_text), repr(kwargs)
	try:
		parse_format = _PARSERS[format]
	except KeyError:
		return parse_generic(format, fp_or_text, **kwargs)
	else:
		return parse_format(fp_or_text, **kwargs)


if __name__ == '__main__':
	data = open(r'Z:\test.xls', 'rb')
	format = 'XLS'

	for row in parse(format, data):	#, columns=ExcelColumns()):
		for k, v in row.items():
			print "%20s: %s" % (k, v)
		print


# TODO: replace ydbf, it has bug when writing dbf
# TODO: not replaced because of some bug?
#def parse_dbfpy(fp, *args, **kwargs):
#	from dbfpy.dbf import Dbf
#	return Dbf(fp, readOnly=True)
#
#PARSERS['DBFPY'] = parse_dbfpy
#del parse_dbfpy
