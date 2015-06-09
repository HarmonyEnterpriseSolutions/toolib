import re

REC_PHONE = re.compile(r"[\-\+\(\)\d][\s\(\)\d\-]+[\d]")
REC_PHONE_DIGIT = re.compile(r"\+|\d")

def lstrip_phone_ua(phone):
	if phone.startswith('8'):
		return phone[1:]
	elif phone.startswith('+38'):
		return phone[3:]
	else:
		return phone
	
def clean_phone(phone):
	return ''.join(REC_PHONE_DIGIT.findall(phone))

def resolve_number(phone, phone_ok):
	return phone_ok[:-len(phone)] + phone

def resolve_numbers(phones):
	phone_ok = None

	for phone in phones:
		if phone.startswith('-'):
			if phone_ok:
				phone = resolve_number(clean_phone(phone), phone_ok)
				yield phone
			else:
				yield '-' + clean_phone(phone)
		else:
			phone_ok = phone = clean_phone(phone)
			yield phone

def parse_phones(text, strip_prefix_ua=False):
	phones = list(resolve_numbers(REC_PHONE.findall(text)))
	if strip_prefix_ua:
		return map(lstrip_phone_ua, phones)
	return phones


if __name__ == '__main__':

	for line in open('phones.txt', 'rt').readlines():

		line = line.strip()

		phones = parse_phones(line, strip_prefix_ua=True)

		if len(phones) == 1 and phones[0] == line:
			continue

		print line, phones

