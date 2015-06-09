# -*- coding: Cp1251 -*-

import re
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from toolib.net.UrlResource import UrlResource
from email.Header import Header
from toolib.utils import strings

try: _
except: _ = lambda x: x

class EmailFormatException(Exception):
	_('EmailFormatException')
	pass

# charset koi8-r, -u has no № character
# charset utf-8 can't be read by mailer
# windows-1251 is unusable in python 2.7 due to bug in emain.mime.charset 
# (it converts to codec name cp1251 which is not recognized by mailers)
DEFAULT_CHARSET = 'utf-8'
REC_SPACE = re.compile(r'\s*')


class EmailMessage(object):

	def __init__(self,
		from_,           # address
		to,              # list of adresses
		subject = None,
		text    = None,
		charset = None,

		replyto = None,  # address
		sender  = None,  # address
		cc      = None,  # list of adresses
		bcc     = None,  # list of adresses
	):
		"""
		"""
		#rint from_
		#rint to
		#rint subject
		#rint text   
		#rint charset
		#rint sender 
		#rint cc     
		#rint bcc    

		self._charset = charset or DEFAULT_CHARSET
		
		self._message = MIMEMultipart()
		self._message.set_charset(self._charset)
    
		self._message['Subject'] = Header((subject or u"").encode(self._charset), self._charset)
    
        # FROM
		self._message['From'] = EmailAddressChecker(_("From")).check(from_)

        # TO
		if not to:
			raise EmailFormatException(_('To is empty'))
		to = map(EmailAddressChecker(_("To")).check, to)
		self._message['To'] = ','.join(to)
		self._to = tuple(to)
		
		#REPLY-TO
		if replyto:
			self._message['Reply-To'] = EmailAddressChecker(_("Reply-To")).check(replyto)

		#SENDER
		if sender:
			self._message['Sender'] = EmailAddressChecker(_("Sender")).check(sender)
		
		#CC
		self.setCc(cc or ())

		#BCC
		self.setBcc(bcc or ())
		
		if text:
			self.attach(text, 'text/plain')

	def setCc(self, cc):
		cc = map(EmailAddressChecker(_("Cc")).check, cc)
		if cc:
			self._message['Cc'] = ','.join(cc)
		elif 'Cc' in self._message:
			del self._message['Cc']
		self._cc = tuple(cc)

	def setBcc(self, bcc):
		bcc = map(EmailAddressChecker(_("Bcc")).check, bcc)
		if bcc:
			self._message['Bcc'] = ','.join(bcc)
		elif 'Bcc' in self._message:
			del self._message['Bcc']
		self._bcc = tuple(bcc)

	def getSender(self):
		return self._message['From']

	def getRecipients(self):
		return self._to + self._cc + self._bcc


	@classmethod
	def fromXml(cls, document, text_from_html=False):
		from toolib.text.xml.XmlElement import getChildElement, getChildText, getAttribute
		if isinstance(document, str):
			from xml.dom.minidom import parse
			from cStringIO import StringIO
			document = parse(StringIO(document))

		email  = getChildElement(document, u'email')

		cc  = getChildElement(email, u'cc',  optional=True)
		bcc = getChildElement(email, u'bcc', optional=True)

		email_message = EmailMessage(
			getChildText(getChildElement(email, u'from')),
			getChildText(getChildElement(email, u'to'), '').split(','),
			subject = getChildText(getChildElement(email, u'subject',  optional=True)),
			text    = getChildText(getChildElement(email, u'text',     optional=True), None),
			charset = getAttribute(email, u'charset'),
			replyto = getChildText(getChildElement(email, u'reply-to', optional=True), None),
			sender  = getChildText(getChildElement(email, u'sender',   optional=True), None),
			cc      = getChildText(cc) .split(',') if cc  else None,
			bcc     = getChildText(bcc).split(',') if bcc else None,
		)

		attachments = getChildElement(email, u'attachments')
		if attachments:
			for attachment in email.getElementsByTagName(u'attachment'):
				
				content = None

				inline = getChildElement(attachment, u"inline", optional=True)
				if inline:
					content = getChildText(inline, joinCData=True, ignoreText=True)

				urlResource = getChildElement(attachment, u"url-resource", optional=True)
				if urlResource:
					url = getChildText(urlResource, joinCData=True, ignoreText=True)

					url = ''.join(strings.splitExRe(url, REC_SPACE))

					# TODO: make urlquote function in template, remove this workaround
					url = url.replace(' ', '%20')

					content = str(UrlResource(url))
				
				if content:
					mimetype = getAttribute(attachment, "mimetype")
					filename = getAttribute(attachment, "filename", None)


					if text_from_html and mimetype == 'text/html':
						from toolib.text.html.unhtml import unhtml_readable

						submessage = MIMEMultipart(_subtype='alternative')

						attach_data(submessage, unhtml_readable(content), 'text/plain', os.path.splitext(filename)[0] + '.txt' if filename else None, email_message._charset)
						attach_data(submessage, content, mimetype, filename, email_message._charset)

						email_message.attachMessage(submessage)
					else:
						email_message.attach(content, mimetype, filename)

		return email_message


	def attachMessage(self, message, filename=None):
		attachMessage(self._message, message, filename)

	def attach(self, data, mimetype, filename=None):
		"""
		mimetypes:
			application
			audio
			image
			text
		"""
		assert mimetype
		attach_data(self._message, data, mimetype, filename, self._charset)

	def __str__(self):
		return self._message.as_string()

	def send(self, smtp):
		smtp.sendmail(self.getSender(), self.getRecipients(), str(self))
		


def attachMessage(message, attachment, filename):
	if filename:
		attachment.add_header('Content-Disposition', 'attachment', filename=filename)
	message.attach(attachment)


def attach_data(message, data, mimetype, filename=None, charset=None):
	"""
	mimetypes:
		application
		audio
		image
		text
	"""
	assert mimetype

	if isinstance(data, unicode):
		if charset:
			data = data.encode(charset)
		else:
			data = str(data)
		
	try:
		mimeType, mimeSubType = mimetype.split('/')
	except ValueError:
		raise EmailFormatException("Invalid attachment MIME type: %s" % mimetype)

	if mimeType == 'text':
		attachment = MIMEText(data, _subtype=mimeSubType, _charset=charset)
	else:
		MIMEClass = getattr(getattr(__import__("email.mime." + mimeType).mime, mimeType), 'MIME' + mimeType.capitalize())
		attachment = MIMEClass(data, _subtype=mimeSubType)

	attachMessage(message, attachment, filename)

RE_EMAIL = '''(?i)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'''
REC_EMAIL = re.compile(RE_EMAIL + '$')
REC_FIND_EMAIL = re.compile(RE_EMAIL)

def isEmailAddress(text):
	"""
	http://tools.ietf.org/html/rfc2822#section-3.4.1
	"""
	if isinstance(text, basestring):
		return bool(REC_EMAIL.match(text))
	else:
		return False

REC_ADDRESS = re.compile('''([^\<]+)\<([^\>]+)\>''')

class EmailAddressChecker(object):

	def __init__(self, description):
		self._description = description

	def check(self, text):
		text = (text or '').strip()

		m = REC_ADDRESS.match(text)
		if m:
			name, text = map(unicode.strip, m.groups())
		else:
			name = None
	
		if not text:
			raise EmailFormatException(_('%s E-Mail is empty') % (self._description,))
		
		if not isEmailAddress(text):
			raise EmailFormatException(_('%s E-Mail is not valid: %s') % (self._description, text))

		text = text.encode('ascii')
		
		if name:
			try:
				name = name.encode('ascii')
			except:
				name = str(Header(name.encode(DEFAULT_CHARSET), DEFAULT_CHARSET))
			return "%s <%s>" % (name, text)
		else:
			return text

def parseEmails(text):
	return REC_FIND_EMAIL.findall(text)


##	message = StringIO.StringIO()
##	writer = MimeWriter.MimeWriter(message)
##
##	writer.addheader('MIME-Version', '1.0')
##	writer.addheader('Subject', )
##
##	writer.addheader('From', 'nogus@mail.ru')
##	writer.addheader('To', 'oleg.noga@gmail.com')
##
##	writer.startmultipartbody('mixed')
##
##	# start off with a text/plain part
##	part = writer.nextpart()
##	body = part.startbody('text/plain')
##	body.write('This is a picture of a kitten, enjoy :)')
##
##	# now add an image part
##	part = writer.nextpart()
##	part.addheader('Content-Transfer-Encoding', 'base64')
##	body = part.startbody('image/jpeg')
##	base64.encode(open('MatrixHamster.jpg', 'rb'), body)
##
##	# finish off
##	writer.lastpart()
##
##	# send the mail
##	smtp = smtplib.SMTP('10.17.13.1')
##	smtp.sendmail('nogus@mail.ru', 'oleg.noga@gmail.com', message.getvalue())
##	smtp.quit()



if __name__ == '__main__':
	xml = open('message.xml', 'rb').read()
	open('message.eml', 'wt').write(str(EmailMessage.fromXml(xml, text_from_html=True)))


