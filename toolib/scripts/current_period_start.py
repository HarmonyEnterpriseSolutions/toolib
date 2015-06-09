import sys
from toolib.util.dates import today


def main(period='day', ms=False):
	date = today().startof(period)
	pattern = '%Y%m%d' if ms else '%Y-%m-%d' 
	print date.strftime(pattern)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('period', nargs='?', default='day', help="period: day|week|month|quarter|year, default is day")
	parser.add_argument('--ms', dest='ms', action='store_true', help="use MSSQL date format")
	main(**parser.parse_args().__dict__)
 	