
	

class Event(object):
	
	GETTERS = [
		'GetClassName', 
		'GetEventType',
		'GetEventObject',
		'GetId',
		'GetSkipped',
		#'GetTimestamp',
		'IsCommandEvent',
	]

	def dump(cls, event):
		print "+ %s ================================" % event.GetClassName()[2:]
		for name in cls.GETTERS:
			print "%s.%s() ==> %s"% (cls.__name__, name, str(getattr(event, name)())[:50])
		print
		#print dir(event)
	dump = classmethod(dump)



class KeyEvent(Event):
	GETTERS = Event.GETTERS + [
		'HasModifiers',
		'ControlDown',
		'AltDown',
		'ShiftDown',
		#'CmdDown',
		#'MetaDown',

		'GetPosition',
		#'GetX',
		#'GetY',

		'GetKeyCode',
		'GetRawKeyCode',
		'GetRawKeyFlags',
		'GetUnicodeKey',
		'GetUniChar',
	]



class UpdateUIEvent(Event):

	GETTERS = [
		'Checked', 
		'GetChecked', 
		'GetEnabled', 
		'GetEventObject', 
		'GetEventType', 
		'GetExtraLong', 
		'GetInt', 
		'GetMode', 
		'GetSelection', 
		'GetSetChecked',
		'GetSetEnabled', 
		'GetSetText', 
		'GetSkipped', 
		'GetString', 
		'GetText', 
		'GetTimestamp', 
		'GetUpdateInterval', 
		'IsChecked', 
		'IsCommandEvent', 
		'IsSelection', 
	]


def dump(object):
	eval(object.GetClassName()[2:]).dump(object)

def dumpWindowSizes(w):
	print "------------------------------------"
	print "Sizes for", w.__class__.__name__
	print "------------------------------------"
	print 'BestSize        ', w.BestSize
	print 'VirtualSize     ', w.VirtualSize
	print 'BestVirtualSize ', w.BestVirtualSize
	print 'MaxSize         ', w.MaxSize
	print 'MinSize         ', w.MinSize
	print 'EffectiveMinSize', w.EffectiveMinSize
	print 'Size            ', w.Size
	print 'ClientSize      ', w.ClientSize
	print
