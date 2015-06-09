import xml.dom

class XmlConstraintException(Exception):
	def __init__(self, element, message):
		super(XmlConstraintException, self).__init__("Element '%s': %s" % (getattr(element, 'tagName', None) if element else None, message))

def getChildElement(element, tagName, optional=False):
	el = element.getElementsByTagName(tagName)
	if optional and not el:
		return
	if len(el) == 1:
		return el[0]
	else:
		raise XmlConstraintException(element, "expected child element '%s' count in %s, got %s" % (tagName, (0, 1) if optional else (1,), len(el)))
		
TEXT_NODE_TYPES = set((xml.dom.Node.TEXT_NODE, xml.dom.Node.CDATA_SECTION_NODE))

def getChildText(element, defaultValue=NotImplemented, joinText=True, joinCData=False, ignoreText=False, ignoreCData=False):
	"""
	nodeType
		xml.dom.Node.TEXT_NODE           - join text nodes, ignore cdata if ignoreOtherTextNodeTypes, ignore comments
		xml.dom.Node.CDATA_SECTION_NODE  - join cdata nodes, ignore text if ignoreOtherTextNodeTypes, ignore comments
		None                             - join text and cdata nodes, ignore comments
	"""
	#rint 'getChildText(%s, %s, %s)' % (defaultValue, nodeType, ignoreOtherTextNodeTypes)
	if element is not None:

		textNodeTypes = set()
		if not ignoreText  and joinText:  textNodeTypes.add(xml.dom.Node.TEXT_NODE)
		if not ignoreCData and joinCData: textNodeTypes.add(xml.dom.Node.CDATA_SECTION_NODE)

		# ignore comments
		ignoredNodeTypes = set((xml.dom.Node.COMMENT_NODE,))
		if ignoreText:  ignoredNodeTypes.add(xml.dom.Node.TEXT_NODE)
		if ignoreCData: ignoredNodeTypes.add(xml.dom.Node.CDATA_SECTION_NODE)

		nodes = [node for node in element.childNodes if node.nodeType not in ignoredNodeTypes]

		# check all nodes is alowed
		for node in nodes:
			if node.nodeType not in textNodeTypes:
				raise XmlConstraintException(element, "unexpected type of node %s" % (node,))

		if nodes:
			text = u''.join((node.data for node in nodes))
		else:
			text = defaultValue
	else:
		text = defaultValue

	if text is NotImplemented:
		raise XmlConstraintException(element, "required text and/or cdata subnodes not found")

	return text

def getAttribute(element, name, defaultValue=NotImplemented):
	value = element.getAttribute(name) if element.hasAttribute(name) else defaultValue
	if value is NotImplemented:
		raise XmlConstraintException(element, "required attribute '%s' not found" % (name,))
	return value		
