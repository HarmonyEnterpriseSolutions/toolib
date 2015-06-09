import mimetypes, mimetools

def encode(fields, files, subtype='form-data', boundary=None, crlf='\n'):
	"""
	fields is a sequence of (name, value) elements for regular form fields.
	files is a sequence of (name, filename, value) elements for data to be uploaded as files
	Return (content_type, body) ready for httplib.HTTP instance
	"""
	boundary = boundary or mimetools.choose_boundary()
	l = []
	for (key, value) in fields:
		l.append('--' + boundary)
		l.append('Content-Disposition: %s; name="%s"' % (subtype, str(key)))
		l.append('')
		l.append(str(value))
	for (key, filename, value) in files:
		l.append('--' + boundary)
		l.append('Content-Disposition: %s; name="%s"; filename="%s"' % (subtype, str(key), str(filename)))
		l.append('Content-Type: %s' % mimetypes.guess_type(filename)[0] or 'application/octet-stream')
		l.append('')
		l.append(str(value))
	l.append('--' + boundary + '--')
	l.append('')

	for i, v in enumerate(l):
		assert isinstance(v, str), v

	body = crlf.join(l)

	headers = {
		'Content-Type'   : 'multipart/%s; boundary=%s' % (subtype, boundary),
		'Content-Length' : len(body),
	}

	return headers, body

"""
#problem that is is encoding content-type header
#cannot use with urllib2
from MimeWriter import MimeWriter
from cStringIO import StringIO
def encode_multipart_formdata2(fields, files):

	out = StringIO()

	w = MimeWriter(out)

	w.startmultipartbody('form-data')

	for key, value in fields:
		sw = w.nextpart()
		sw.addheader('Content-Disposition', 'form-data; name="%s"' % (key,))
		f = sw.startbody('application/octet-stream')
		f.write(value)

	for key, filename, value in files:
		sw = w.nextpart()
		sw.addheader('Content-Disposition', 'form-data; name="%s"; filename="%s"' % (key, filename))
		f = sw.startbody(mimetypes.guess_type(filename)[0] or 'application/octet-stream')
		f.write(value)

	w.lastpart()

	return out.getvalue()
"""

