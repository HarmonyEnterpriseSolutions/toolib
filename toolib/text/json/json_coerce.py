import decimal
import datetime


def json_coerce_list(l):
	return [json_coerce(i) for i in l]


def json_coerce_decimal(v):
	return str(v)


def json_coerce_dict(d):
	return dict(((json_coerce(k), json_coerce(v)) for k, v in d.iteritems()))


COERCERS = {
	list              : json_coerce_list,
	tuple             : json_coerce_list,
	dict              : json_coerce_dict,
	decimal.Decimal   : json_coerce_decimal,
	datetime.datetime : lambda value: value.isoformat(),
	datetime.date     : lambda value: value.isoformat(),
	datetime.time     : lambda value: value.isoformat(),
}


try:
	import _decimal
except:
	pass
else:
	COERCERS[_decimal.Decimal] = COERCERS[decimal.Decimal]


def json_coerce(object):
	f = COERCERS.get(type(object))
	if f:
		return f(object)
	else:
		#rint ">>> not found", type(object)
		if hasattr(object, '__iter__'):
			#rint ">>> converted to list", repr(object)
			return json_coerce_list(object)
		else:
			return object

