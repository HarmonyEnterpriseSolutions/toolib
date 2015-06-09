# -*- coding: cp1251 -*-
import re


# ISO 9-95
TRANSLIT = {
	u"�": "-",
	u"�": "",
	u"�": "",
	u"�": "#",
	u"�": "A",
	u"�": "a",
	u"�": "B",
	u"�": "b",
	u"�": "V",
	u"�": "v",
	u"�": "G",
	u"�": "g",
	u"�": "G",
	u"�": "g",
	u"�": "D",
	u"�": "d",
	u"�": "E",
	u"�": "e",
	u"�": "YO",
	u"�": "yo",
	u"�": "YE",
	u"�": "ye",
	u"�": "ZH",
	u"�": "zh",
	u"�": "Z",
	u"�": "z",
	u"�": "I",
	u"�": "i",
	u"�": "I",
	u"�": "i",
	u"�": "J",
	u"�": "j",
	u"�": "K",
	u"�": "k",
	u"�": "L",
	u"�": "l",
	u"�": "M",
	u"�": "m",
	u"�": "N",
	u"�": "n",
	u"�": "O",
	u"�": "o",
	u"�": "P",
	u"�": "p",
	u"�": "R",
	u"�": "r",                            
	u"�": "S",
	u"�": "s",
	u"�": "T",
	u"�": "t",
	u"�": "U",
	u"�": "u",
	u"�": "F",
	u"�": "f",
	u"�": "H",
	u"�": "h",                         
	u"�": "C",
	u"�": "c",
	u"�": "CH",
	u"�": "ch",
	u"�": "SH",
	u"�": "sh",
	u"�": "SHH",
	u"�": "shh",
	u"�": "'",
	u"�": "",                      
	u"�": "Y",
	u"�": "y",
	u"�": "E",
	u"�": "e",
	u"�": "YU",
	u"�": "yu",
	u"�": "YA",
	u"�": "ya",
	u"�": "",
	u"�": "",
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
	print make_slug(u'����� ���� ����� ���� ����', lowercase=False)

