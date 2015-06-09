import re
import psycopg2
from simpleconn import Connection

REC_COLUMN_DEFAULT = re.compile("""nextval\('(\w+)'::regclass\)""")


def pg_reset_seq(conn, commit=True, lower=False, tables=None):

	# wrapp db api 2.0 connection to simpleconn
	if not isinstance(conn, Connection):
		conn = Connection(psycopg2, _connection_=conn)

	c = 0
	
	for table_name, column_name, column_default in conn.execute("SELECT table_name, column_name, column_default FROM information_schema.columns WHERE (%(tables)s IS NULL OR table_name = ANY(%(tables)s)) AND column_default LIKE 'nextval(\\'%%\\'::regclass)'", locals()):

		sequence_name, = REC_COLUMN_DEFAULT.match(column_default).groups()

		value, = conn.execute("SELECT last_value FROM %s" % sequence_name).getSingleRow()
		
		max_value, = conn.execute("SELECT COALESCE(MAX(%s), 1) FROM %s" % (column_name, table_name)).getSingleRow()

		#rint sequence_name, value, max_value

		if max_value > value or lower and max_value != value:

			print "resetting %s.%s sequence %s. last value is %s, must be %s" % (table_name, column_name, sequence_name, value, max_value)
		
			conn.execute("SELECT setval('%s', %s)" % (sequence_name, max_value))
			if commit:
				conn.commit()

			c += 1

	return c
		

if __name__ == '__main__':
	import psycopg2
	conn = Connection(psycopg2, 
		user = 'postgres',
		password = 'postgres',
		database = 'wwmtest',
	)
	pg_reset_seq(conn, lower=True, tables=['spr_wms_items'])