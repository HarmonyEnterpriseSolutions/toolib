# -*- coding: Cp1251 -*-
import sys
import locale
import decimal
import datetime
import random
from toolib.text.report.config import TEXT_FORMAT_FACTORY_CONFIG
from toolib.text.report.GroupingTableTextReport import GroupingTableTextReport
from toolib.text.report.TextFormatFactory import TextFormatFactory

def getColumns():
	return [
		'_msg_to',
		'_org_contact_name',
		'_delay_date',
		'_doc_num',
		'_doc_date',
		'_doc_sum',
		'_currency_name'
	]

def getData(N, M):
	return [
		{
			'_msg_to' : 'valeriy@petrovich.test',
			'_org_contact_name' : 'Валерий Петрович',#['Валерий Петрович', 'Анна Ивановна'][i/(N/2)],
			'_delay_date' : datetime.date.today() + datetime.timedelta(i / M),
			'_doc_num' : i + 1,
			'_doc_date' :  datetime.date.today() + datetime.timedelta(i),
			'_doc_sum' : decimal.Decimal(str(round(random.random() * 10000000) / 100)),
			'_currency_name' : ('штук', 'тонн', 'метров')[int(random.random() * 3)]
		}
		for i in xrange(N)
	]

def printData(data, columns):
	for row in data:
		print "\t".join([str(row[i]) for i in columns])


def test(file='template.txt'):
	data = getData(20, 4)
	printData(data, getColumns())
	print
	print
	report = GroupingTableTextReport(open(file, 'rt').read(), TextFormatFactory(**TEXT_FORMAT_FACTORY_CONFIG))
	print report.format(data)


if __name__ == '__main__':
	
	from toolib import startup
	startup.startup()

	locale.setlocale(locale.LC_ALL, '')

	test(*sys.argv[1:])
