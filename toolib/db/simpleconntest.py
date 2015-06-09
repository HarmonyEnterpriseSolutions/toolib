#-*- coding: UTF8 -*-

import unittest
from simpleconn import Connection
from decimal import Decimal
import datetime

MSSQLCONN = {
	'host'     : '192.168.2.4',
	'user'     : 'dealer',
	'password' : 'dealer', 
}

PGSQLCONN = {
	'host'     : 'localhost',
	'user'     : 'postgres',
	'password' : 'postgres', 
}


class GenericTestCase(unittest.TestCase):
	
	def setUp(self):
		self.order = (
			u'текст', 
			u'целое', 
			u'децимал', 
			#u'дата', 
			#u'датавремя', 
			#u'логическое',
		)
		self.row = {
			u'текст'      : u'ЙЦУКЕНГШЩЗХЇФВАПРОЛДЖЄЯЧСМИТЬБЮйцукенгшщзхїфвапролджєячсмитьбю',
			u'целое'      : 12345,
			u'децимал'    : Decimal('12.345'),
			u'дата'       : datetime.date.today(),
			u'датавремя'  : datetime.datetime.now(),
			u'логическое' : True,
		}
		self.insert = u'INSERT INTO таблица (%s) VALUES (%s)' % (
			', '.join(self.order),
			', '.join(('%(' + i + ')s' for i in self.order)),
		)
		self.select = u'SELECT %s FROM таблица' % (
			', '.join(self.order),
		)

		self.row2 = [self.row[i] for i in self.order]
		self.insert2 = u'INSERT INTO таблица (%s) VALUES (%s)' % (
			', '.join(self.order),
			', '.join(('%s' for i in self.order)),
		)

	def tearDown(self):
		pass

	def do_test_types(self, c):
		c.execute(self.insert, dict(self.row))
		c.commit()
		c.execute(self.insert.encode(c.encoding), encode_dict(dict(self.row), c.encoding))
		c.commit()

		c.execute(self.insert2, list(self.row2))
		c.commit()
		c.execute(self.insert2.encode(c.encoding), encode_list(list(self.row2), c.encoding))
		c.commit()
		
		rows = list(c.execute(self.select))
		assert len(rows) == 4

		for row in rows:
			for (i, field) in enumerate(self.order):
				print field, row[i]
				assert self.row[field] == row[i]
				assert type(self.row[field]) is type(row[i])


def encode_dict(d, encoding):
	d2 = {}
	for k, v in d.iteritems():
		if isinstance(k, unicode): k = k.encode(encoding)
		if isinstance(v, unicode): v = v.encode(encoding)
		d2[k] = v
	return d2

def encode_list(l, encoding):
	return [v.encode(encoding) if isinstance(v, unicode) else v for v in l]

class Psycopg2TestCase(GenericTestCase):

	def setUp(self):
		
		GenericTestCase.setUp(self)

		import psycopg2
		c = Connection(psycopg2, _encoding_='UTF8', **PGSQLCONN)
		c.set_isolation_level(0)
		#c.execute('DROP DATABASE IF EXISTS temp_test')
		try:
			c.execute('CREATE DATABASE temp_test')
		except:
			pass
		c.close()

		c = Connection(psycopg2, database='temp_test', _encoding_='UTF8', **PGSQLCONN)
		c.execute(u'''
			DROP TABLE IF EXISTS таблица;
			CREATE TABLE таблица (
				ключ SERIAL PRIMARY KEY,
				текст text,
				целое integer,
				децимал decimal(5,3),
				дата date,
				датавремя timestamp without time zone,
				логическое boolean
			);
		''')

		c.commit()
		c.close()

	def tearDown(self):
		GenericTestCase.tearDown(self)
		#c = Connection(psycopg2, **PGSQLCONN)
		#c.set_isolation_level(0)
		#c.execute('DROP DATABASE IF EXISTS temp_test')
		#c.close()

	def test_types_psycopg2(self):
		import psycopg2
		self.do_test_types(Connection(psycopg2, database='temp_test', _encoding_='UTF8', **PGSQLCONN))


class PyodbcTestCase(GenericTestCase):

	def setUp(self):
		
		GenericTestCase.setUp(self)

		import pyodbc
		c = Connection(pyodbc, u'DRIVER={SQL Server};SERVER=%(host)s;DATABASE=master;UID=%(user)s;PWD=%(password)s' % MSSQLCONN, autocommit = True, _encoding_='Cp1251')
		try:
			c.execute('CREATE DATABASE temp_test')
		except:
			pass
		c.close()

		c = Connection(pyodbc, u'DRIVER={SQL Server};SERVER=%(host)s;DATABASE=temp_test;UID=%(user)s;PWD=%(password)s' % MSSQLCONN, _encoding_='Cp1251')
		try:
			c.execute(u'''DROP TABLE таблица;''')
		except:
			pass
		c.execute(u'''
			CREATE TABLE таблица (
				ключ int identity not null,
				текст text,
				целое int,
				децимал decimal(5,3),
				дата smalldatetime,
				датавремя datetime,
				логическое int
			);
		''')

		c.commit()
		c.close()

	def tearDown(self):
		GenericTestCase.tearDown(self)
		#c = Connection(pyodbc, **PGSQLCONN)
		#c.set_isolation_level(0)
		#c.execute('DROP DATABASE IF EXISTS temp_test')
		#c.close()

	def test_types_psycopg2(self):
		import pyodbc
		c = Connection(pyodbc, u'DRIVER={SQL Server};SERVER=%(host)s;DATABASE=temp_test;UID=%(user)s;PWD=%(password)s' % MSSQLCONN, _encoding_='Cp1251')
		self.do_test_types(c)


if __name__ == '__main__':
	unittest.main()