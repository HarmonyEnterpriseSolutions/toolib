from datetime import date, datetime
import locale
try: _
except NameError: _ = lambda x: x

def checktype(v, types):
	if not isinstance(v, types):
		raise TypeError, _("Expected type %s, got %s") % (_(' or ').join(("'%s'" % t.__name__ for t in types)), "'%s'" % type(v).__name__)
	return v

def blanknull(field, value):
	if value is None:
		field.yieldText('')
	return value

def blankfalse(field, value):
	if not value:
		field.yieldText('')
	return value

def nbsp(field, value):
	if not value:
		field.yieldText('&nbsp;')
	return value

def convert_decimal(field, v, scale=2, grouping=1):
	
	text = locale.format('%%.%df' % int(scale), v, grouping)

	if isinstance(text, str):
		text = text.decode(locale.getlocale()[1] or 'ascii', 'replace').replace('?', ' ')

	return text

TEXT_FORMAT_FACTORY_CONFIG = {

	'converters' : {
		'date'       : lambda field, v, format=None: checktype(v, (datetime,date)).strftime(format or '%x').decode(locale.getpreferredencoding()),
		'time'       : lambda field, v, format=None: checktype(v, datetime).strftime(format or '%X').decode(locale.getpreferredencoding()),
		'datetime'   : lambda field, v, format=None: checktype(v, datetime).strftime(format or '%c').decode(locale.getpreferredencoding()),
		'decimal'    : convert_decimal,
		'today'      : lambda field, v: date.today(),
		'now'        : lambda field, v: datetime.now(),
		'blanknull'  : blanknull,
		'blankfalse' : blankfalse,
		'iif'        : lambda field, v, resultTrue, resultFalse=None: resultTrue if v else resultFalse,
		'nbsp'       : nbsp,
		'ifnot'      : lambda field, v, alt: v or alt,
		'join'		 : lambda field, v, joiner: joiner.join(v),
		'call'       : lambda field, v, method, *params: getattr(v, method)(*params),
		'gt'         : lambda field, v, other: v > other,
	},

}
