import re
from toolib import debug

"""
simple db api 2.0 connection wrapper with iterable RecordSet
"""

REC_PARAMETER = re.compile(u'''(?u)%\((\w+)\)s''')

class MiscountRecordError(RuntimeError):
	pass

class NoRecordError(MiscountRecordError):
	pass

class MultipleRecordsError(MiscountRecordError):
	pass

class RecordSet(object):

	def __init__(self, cursor, encoding, encoding_errors, sql, parameters):
		self.__cursor = cursor
		self.__encoding = encoding
		self.__encoding_errors = encoding_errors
		self.__sql = sql               # for debug
		self.__parameters = parameters # for debug
		self.columns = [i[0] for i in cursor.description or ()]

	def __getattr__(self, name):
		return getattr(self.__cursor, name)

	def __iter__(self):
		return self

	# rowcount may be broken
	#def __len__(self):
	#	return self.__cursor.rowcount

	def next(self):
		if self.__cursor is None:
			raise StopIteration

		r = self.__cursor.fetchone()

		if r is None:
			#rint ">>> close cursor in next"
			self.__cursor.close()
			self.__cursor = None
			raise StopIteration

		if self.__encoding:
			r = tuple([i.decode(self.__encoding, self.__encoding_errors) if isinstance(i, str) else i for i in r])
		
		return r


	def getSingleRecord(self):
		rows = list(self)
		if not rows:
			raise NoRecordError, "Single record expected, got no records, sql = %s, parameters = %s" % (str_or_repr(self.__sql), repr(self.__parameters))
		elif len(rows) == 1:
			return rows[0]
		else:
			raise MultipleRecordsError,	"Single record expected, got %s records, sql = %s, parameters = %s" % (len(rows), str_or_repr(self.__sql), repr(self.__parameters))


	def getSingleValue(self, default=NotImplemented):
		"""
		Throws NoRecordError if default is not provided and no records
		Throws MultipleRecordsError if more than one record
		"""
		if default is NotImplemented:
			return self.getSingleRow()[0]
		else:
			try:
				return self.getSingleRow()[0]
			except NoRecordError:
				return default

	
	def hasRecords(self):
		"""
		checks if has records
		closes cursor
		"""
		try:
			self.next()
		except StopIteration:
			return False
		else:
			self.close()
			return True

	def getAffectedRecordCount(self):
		return self.__cursor.rowcount
	
	def close(self):
		if self.__cursor is not None:
			#rint ">>> close cursor in close"
			self.__cursor.close()
			self.__cursor = None
	
	singleRow = getSingleRecord
	getSingleRow = getSingleRecord


class DictRecordSet(RecordSet):

	def next(self):
		r = super(DictRecordSet, self).next()
		
		# repack tuple into dictionary
		d = {}
		for i, column in enumerate(self.columns):
			d[column] = r[i]

		return d


RS_BY_TYPE = {
	tuple : RecordSet,
	dict : DictRecordSet,
}


class Connection(object):


	def __init__(self, driver, *args, **kwargs):
		"""
		driver: dbapi 2.0 module
		_encoding_: encoding to convert query, parameters and resultset
		_connection_: pass dbapi 2.0 connection here if already created
		"""	
		assert hasattr(driver, 'connect'), 'first parameter must be dbapi 2.0 compattible driver'

		self.__driver = driver

		kwargs = dict(kwargs)
		self.encoding = kwargs.pop('_encoding_', None)
		self.encoding_errors = kwargs.pop('_encoding_errors_', 'strict')
		self.__decorate_error = kwargs.pop('_decorate_error_', lambda error: error)
		self.__conn = kwargs.get('_connection_') or driver.connect(*args, **kwargs)


	def __getattr__(self, name):
		return getattr(self.__conn, name)

	def execute(self, sql, parameters=None, rowType=tuple):
		"""
		Returns one-pass RecordSet
		"""
		# Convert parameters into correct style
		if parameters is not None:
			sql, parameters = getattr(self, '_convert_paramstyle_' + self.__driver.paramstyle)(sql, parameters)

		# convert sql and parameters to encoding
		if self.encoding and isinstance(sql, unicode):
			sql = sql.encode(self.encoding)
			
		if parameters is not None:
			if isinstance(parameters, dict):
				if self.encoding:
					parameters = dict((map(self._encode_parameter, item) for item in parameters.iteritems()))
			elif isinstance(parameters, (list, tuple)):
				if self.encoding:
					parameters = map(self._encode_parameter, parameters)
			else:
				raise TypeError, 'Unexpected parameters type: %s' % (parameters.__class__.__name__)
		
		c = self.__conn.cursor()
	
		assert debug.trace('sql: %s' % repr(sql))
		if isinstance(parameters, dict):
			assert debug.trace('parameters: {\n%s\n}' % '\n'.join(['\t%-30s: %s,' % (repr(k), repr(v)) for k, v in parameters.iteritems()]))
		elif isinstance(parameters, list):
			assert debug.trace('parameters: [\n%s\n]' % '\n'.join(['\t%s,' % repr(v) for v in parameters]))

		while True:
			try:
				if parameters is None:
					c.execute(sql)
				else:
					c.execute(sql, parameters)
			except self.__driver.DatabaseError, error:

				assert debug.trace('ERROR: %s: %s' % (error.__class__.__name__, error))

				error = self.__decorate_error(error)

				if error is None:
					continue # retry

				raise error

			else:
				break

		return RS_BY_TYPE[rowType](c, self.encoding, self.encoding_errors, sql, parameters)
		
	
	def _set_autocommit(self, value): self.__conn.autocommit = value
	autocommit = property(lambda self: self.__conn.autocommit, _set_autocommit)

	
	def _encode_parameter(self, p):
		return p.encode(self.encoding) if isinstance(p, unicode) else p
			

	def _convert_paramstyle_pyformat(self, sql, parameters):
		"""
		exclude not used parameters
		"""
		if isinstance(parameters, dict):
			d = {}

			if isinstance(sql, str):
				sql = unicode(sql) if self.encoding is None else sql.decode(self.encoding)

			for p in REC_PARAMETER.findall(sql):
				if p in parameters:
					d[p] = parameters[p]
				else:
					p_str = str(p) if self.encoding is None else p.encode(self.encoding)
					
					if p_str in parameters:
						d[p] = parameters[p_str]
					else:
						raise KeyError, p

			return sql, d
		else:
			return sql, parameters


	def _convert_paramstyle_format(self, sql, parameters, mark='%s'):
		if isinstance(parameters, dict):
			l = []
			while True:
				start = sql.find('%(')
				if start == -1:
					break
				end = sql.find(')s', start)
				if end == -1:
					break
				key = sql[start+2:end]
				sql = ''.join((sql[:start], mark, sql[end+2:]))
				l.append(parameters[key])
			return sql, l
		else:
			return sql.replace('%s', mark) if mark != '%s' else sql, parameters

	def _convert_paramstyle_qmark(self, sql, parameters):
		return self._convert_paramstyle_format(sql, parameters, mark='?')


	# DEPRECATED
	def query(self, sql, **parameters):
		"""
		Returns one-pass RecordSet, dict row type
		DEPRECATED
		"""
		return self.execute(sql, parameters, dict)


def str_or_repr(sql):
	try:
		return sql.encode('ascii')
	except:
		return repr(sql)

