#-*- coding: UTF-8

try: _
except: _ = lambda x: x

import re

CODES = {
	'+380' : (
		'39',        # Киевстар (Golden Telecom)
		'50',        # МТС                      
		'63',        # life:)                   
		'66',        # МТС                      
		'67',        # Киевстар                 
		'68',        # Киевстар (Beeline)       
		'91',        # Utel                     
		'92',        # PEOPLEnet                
		'93',        # life:)                   
		'94',        # Интертелеком             
		'95',        # МТС                      
		'96',        # Киевстар                 
		'97',        # Киевстар                 
		'98',        # Киевстар
		'99',        # МТС
		'31',        # Укртелеком VVV
		'32',
		'33',
		'34',
		'35',
		'36',
		'37',
		'38',
		'41',
		'42',
		'43',
		'44',
		'45',
		'46',
		'47',
		'48',
		'49',
		'51',
		'52',
		'53',
		'54',
		'55',
		'56',
		'57',
		'58',
		'59',
		'61',
		'62',
		'63',
		'64',
		'65',
		'69',        # Укртелеком
	),
}


REC_PHONE_REMOVE = re.compile(r'[^\+0-9]|\#.*$|\*.*$')

def clean_phone(phone, prefix='+38044'):

	# remove everything not a number and all after #, * 
	phone = REC_PHONE_REMOVE.sub('', phone)

	#if len(phone) == 12:
	#	return '+' + phone;

	if len(phone) == 11 and phone[0] == prefix[2]:
		phone = prefix[:2] + phone;

	elif len(phone) == 10:
		phone = prefix[:3] + phone;

	elif len(phone) == 9:
		phone = prefix[:4] + phone;

	elif len(phone) == 7:
		phone = prefix[:6] + phone;
	
	if len(phone) == 13:
		return phone


REC_CLEAN_PHONE = re.compile(r'^\+\d{12}$')

def validate_phone(phone):
	"""
	checks number in format +380001112233 for country
	only UA yet
	"""
	if not REC_CLEAN_PHONE.match(phone):
		raise ValueError, _('phone number is not valid')
		
	#prefix = phone[:4]
	#codes = CODES.get(prefix, ())
	#if codes:
	#	phone_code = phone[len(prefix):len(prefix)+len(codes[0])]
	#	if not phone_code in codes:
	#		raise ValueError, _('unknown phone number code %s') % (prefix + phone_code,)
	return phone


if __name__ == '__main__':

	for phone in (
		'+380677313281',
		'+380671731328',
		'+380171731328',
	):
		print phone, validate_phone(phone)
