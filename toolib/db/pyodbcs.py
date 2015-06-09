
def get_mssql_connect_string(mssqlconn):
	if 'port' not in mssqlconn:
		mssqlconn['port'] = 1433
	return u'DRIVER={SQL Server};SERVER=%(host)s;DATABASE=%(database)s;UID=%(user)s;PWD=%(password)s;PORT=%(port)s;ClientCharset=CP1251' % mssqlconn

def mssql_connect(**mssqlconn):
	import pyodbc
	return pyodbc.connect(get_mssql_connect_string(mssqlconn))
	