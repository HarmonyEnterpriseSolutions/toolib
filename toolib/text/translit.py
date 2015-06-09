# -*- coding: cp1251 -*-
import re


# ISO 9-95
TRANSLIT = {
	u"—": "-",
	u"«": "",
	u"»": "",
	u"№": "#",
	u"А": "A",
	u"а": "a",
	u"Б": "B",
	u"б": "b",
	u"В": "V",
	u"в": "v",
	u"Г": "G",
	u"г": "g",
	u"Ѓ": "G",
	u"ѓ": "g",
	u"Д": "D",
	u"д": "d",
	u"Е": "E",
	u"е": "e",
	u"Ё": "YO",
	u"ё": "yo",
	u"Є": "YE",
	u"є": "ye",
	u"Ж": "ZH",
	u"ж": "zh",
	u"З": "Z",
	u"з": "z",
	u"И": "I",
	u"и": "i",
	u"І": "I",
	u"і": "i",
	u"Й": "J",
	u"й": "j",
	u"К": "K",
	u"к": "k",
	u"Л": "L",
	u"л": "l",
	u"М": "M",
	u"м": "m",
	u"Н": "N",
	u"н": "n",
	u"О": "O",
	u"о": "o",
	u"П": "P",
	u"п": "p",
	u"Р": "R",
	u"р": "r",                            
	u"С": "S",
	u"с": "s",
	u"Т": "T",
	u"т": "t",
	u"У": "U",
	u"у": "u",
	u"Ф": "F",
	u"ф": "f",
	u"Х": "H",
	u"х": "h",                         
	u"Ц": "C",
	u"ц": "c",
	u"Ч": "CH",
	u"ч": "ch",
	u"Ш": "SH",
	u"ш": "sh",
	u"Щ": "SHH",
	u"щ": "shh",
	u"Ъ": "'",
	u"ъ": "",                      
	u"Ы": "Y",
	u"ы": "y",
	u"Э": "E",
	u"э": "e",
	u"Ю": "YU",
	u"ю": "yu",
	u"Я": "YA",
	u"я": "ya",
	u"Ь": "",
	u"ь": "",
}

REC_SLUG = re.compile('(?i)[A-Z0-9]+')	

def translit(s):
	return ''.join([TRANSLIT.get(i, i) for i in s])


def make_slug(s, lowercase=True):
	s = translit(s)
	if lowercase:
		s = s.lower()
	return '-'.join(REC_SLUG.findall(s))


if __name__ == '__main__':
	print make_slug(u'Через штані джміль куса мене', lowercase=False)

