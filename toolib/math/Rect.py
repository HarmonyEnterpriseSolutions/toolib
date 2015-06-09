"""
Point, Size, Rect, geometry calculations
"""

class Point(object):

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def maxDimensions(self, other):
		assert isinstance(other, Point)
		return Point(max(self.x, other.x), max(self.y, other.y))

	def minDimensions(self, other):
		assert isinstance(other, Point), other
		return Point(min(self.x, other.x), min(self.y, other.y))

	def __repr__(self):
		return "Point(%s, %s)" % (self.x, self.y)

	def __iter__(self):
		return iter((self.x, self.y))

Point.ZERO = Point(0, 0)

class Size(object):

	def __init__(self, width, height):
		self.width  = width
		self.height = height

	@classmethod
	def fromTwoPoints(cls, topLeft, bottomRight):
		assert isinstance(topLeft, Point)
		assert isinstance(bottomRight, Point)
		return Size(bottomRight.x - topLeft.x + 1, bottomRight.y - topLeft.y + 1)

	def __repr__(self):
		return "Size(%s, %s)" % (self.width, self.height)

	def __iter__(self):
		return iter((self.width, self.height))

class Rect(object):
	
	def __init__(self, pos, size):
		if not isinstance(pos, Point): pos = Point(*pos)
		if not isinstance(size, Size):   size = Size(*size)

		self.pos = pos
		self.size = size

	@classmethod
	def fromTwoPoints(cls, topLeft, bottomRight):
		return cls(topLeft, Size.fromTwoPoints(topLeft, bottomRight))

	def area(self):
		return self.size.width * self.size.height

	def bottom(self):
		return self.pos.y + self.size.height - 1

	def right(self):
		return self.pos.x + self.size.width - 1

	def bottomRight(self):
		return Point(self.right(), self.bottom())

	def intersect(self, other):
		assert isinstance(other, Rect)
		return Rect.fromTwoPoints(self.pos.maxDimensions(other.pos), self.bottomRight().minDimensions(other.bottomRight()))

	def __repr__(self):
		return "Rect(%s, %s)" % (repr(self.pos), repr(self.size))

	def __iter__(self):
		return iter((self.pos, self.size))

if __name__ == '__main__':
	
	r1 = Rect((10,10), (100, 100))
	r2 = Rect((20,10), (300, 300))

	print repr(r1.intersect(r2))

	print tuple(r1.pos)
	print tuple(r1.size)

	(x,y), (w,h) = r1

	print x, y, w, h
