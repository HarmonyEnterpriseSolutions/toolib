
import exceptions
import types
import operator

def descrToIndexDict(descr):
	"""
	Gets query result descriptor and convert it
	to a dictionary <'fieldName : indexInDescription'>.
	Can be used to walk through data rows in recordset.
	"""
	retDict = {}
	for i in range(len(descr)) :
		retDict[descr[i][0]] = i
	return retDict

def convertValueToSQL(value) :
	if value is None :
		return 'NULL'
	elif type(value) in [types.StringType, types.UnicodeType] :
		value = str(value)
		#This is was patched by Fedas
		#Replace needed to save "'" in original string
		return "'%s'" % value.replace("\\","\\\\").replace("'","\\'")
	elif operator.isNumberType(value) :
		return "%s" % value
	else :
		raise exceptions.ValueError('Unknown type in convertToSQL <%s:%s>' % (type(value), value))

def printCursorRes(descr, data):
	"""
	Prints query result to console in form of table.
	"""
	print
	print formatCursorRes(descr, data)
	print "Result %d rows" % len(data)

def formatCursorRes(descr, data) :
	"""
	Prints query result to console in form of table.
	"""
	rows = len(data)
	formatNum = '|%' + str(len(str(rows))) + 's|'
	fldStr = formatNum %'#'
	fldStr1 = '+' + '-'*(len(fldStr)-2) + '+'
	for descriptor in descr :
		format = '%' + str(descriptor[2] + 1) + 's |'
		fldStr += format % str(descriptor[0][:descriptor[2] + 1])
		fldStr1 += str('-'*(descriptor[2] + 2)) + '+'
	dataList = []
	dataList.append('%s' % fldStr1)
	dataList.append('%s' % fldStr)
	dataList.append('%s' % fldStr1)
	#print '-' * len(fldStr)  + '|'
	for index in range(rows) :
		row = data[index]
		rowList = [formatNum %(index+1),]
		for i in range(len(row)) :
			format = '%' + str(descr[i][2] + 1) + 's |'
#			if row[i]==None:
#				rowList.append(format % 'None')
#			else:
			rowList.append(format % row[i])
		dataList.append("".join(rowList))
	dataList.append('%s' % fldStr1)
	return '\n'.join(dataList)




