import pymel.core as pm
def AttrExists( node , attr):

	if (attr and node):
		if not pm.objExists(node): return 0
		if attr in pm.listAttr(node,shortNames=True): return 1
		if attr in pm.listAttr(node): return 1
		return 0    
