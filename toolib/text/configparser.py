from ConfigParser import ConfigParser
from cStringIO import StringIO


def iter_config(text):

	c = ConfigParser()
	f = StringIO()
	f.write(text)
	f.seek(0)
	try:
		c.readfp(f)
	finally:
		f.close()

	for section in c.sections():
		for o in c.options(section):
			yield (section, o), c.get(section, o, raw=True)
	

def config_from_dict(d):

	c = ConfigParser()

	items = d.items()
	items.sort()

	old_section = None
	for (section, option), value in items:
		if section != old_section:
			c.add_section(section)
			old_section = section
		c.set(section, option, value)

	f = StringIO()

	c.write(f)
	
	return f.getvalue()


def join_configs(*configs):

	d = dict()
	
	for config in reversed(configs):
		
		d.update(dict(iter_config(config)))

	return config_from_dict(d)


if __name__ == '__main__':
	print join_configs("""\
[report]
a=1
b=2
c=3

[zuzbe]
bebe=2
""", """\
[report]
a=4
b=5
d=333

[zuzbe]
bebe=7
""")
