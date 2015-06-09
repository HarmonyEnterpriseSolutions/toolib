#################################################################
# Program: Rata
"""
Functions to generate SQL from python data types
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/03/20 19:01:33 $"
__version__ = "$Revision: "
# $Source: D:/HOME/cvs/toolib/db/sqlgen.py,v $
#
#################################################################
import types, pywintypes, time

SQLNULL						= 'NULL'	#
SQLFALSE_CONDITION			= '0=1'		#
SQLTRUE_CONDITION			= '1=1'
DEF_SQLCOND_OPERATOR		= 'AND'
DEF_SQLJOIN_TYPE			= 'LEFT JOIN'

def sqlConstant(var):		# ! used in sula
	if var is None:
		return SQLNULL
	else:
		if type(var) is types.UnicodeType:
			var = str(var)
		if type(var) is types.StringType:
			var = var.replace('\\', '\\\\').replace('"', '\\\"')
			return '"%s"' % var
		return str(var)

def sqlConditionFromPropDict(propDict, operator = DEF_SQLCOND_OPERATOR):
	'Make condition string from dict of fields : values and operator'
	if not propDict:
		return '1'		# True condition ('1=1')
	retList = []
	sep = ' %s ' %operator
	for key in propDict.iterkeys():
		val = sqlConstant(propDict[key])
		if val == SQLNULL:
			cond = '%s is %s' % (key, val)
		else:
			cond = '%s=%s' % (key, val)
		retList.append(cond)
	return sep.join(retList)


### SQL DATE ###

def sqlDateFromTuple(date):
	return "%04d-%02d-%02d" % date[:3]

def sqlDateFromNumber(date):
	return sqlDateFromTuple(time.localtime(date))

def sqlDateFromCOM(date):
	return sqlDateFromTuple(time.localtime(int(date)))

__SQLDATE_CONVERTERS = {
	types.IntType		: sqlDateFromNumber,
	types.LongType		: sqlDateFromNumber,
	types.FloatType		: sqlDateFromNumber,
	types.TupleType		: sqlDateFromTuple,
	pywintypes.TimeType : sqlDateFromCOM,
	time.struct_time	: sqlDateFromTuple,
}

def sqlDate(var):
	conv = __SQLDATE_CONVERTERS.get(type(var))
	if conv is not None:
		return conv(var)



### SQL DATE TIME###

def sqlDateTimeFromTuple(date):
	return "%04d-%02d-%02d %02d:%02d:%02d" % date[:6]

def sqlDateTimeFromNumber(date):
	return sqlDateTimeFromTuple(time.localtime(date))

def sqlDateTimeFromCOM(date):
	return sqlDateFromTuple(time.localtime(int(date)))

__SQLDATETIME_CONVERTERS = {
	types.IntType		: sqlDateTimeFromNumber,
	types.LongType		: sqlDateTimeFromNumber,
	types.FloatType		: sqlDateTimeFromNumber,
	types.TupleType		: sqlDateTimeFromTuple,
	pywintypes.TimeType : sqlDateTimeFromCOM,
	time.struct_time	: sqlDateTimeFromTuple,
}

def sqlDateTime(var):
	conv = __SQLDATETIME_CONVERTERS.get(type(var), None)
	if conv:
		return conv(var)

if __name__ == '__main__':
	print sqlDate((2001,2,3,4,5,6))
	print map(sqlConstant, [1,'2',3,None,])

