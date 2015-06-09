def translateKeys(d, trans):
	res = {}

	for key1, key2 in trans:
		try:
			res[key2] = d[key1]
		except KeyError:
			pass

	return res


if __name__ == '__main__':
	print translateKeys({1:111, 2:222}, ((1,'a'), (2,'b')))