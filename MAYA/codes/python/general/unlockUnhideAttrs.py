import pymel.core as pm
# ==========================================================================================
# unlock and unhide Attributes def
# ==========================================================================================
def UnlockUnhideAttrs( objs = None ) :

	if objs==None:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	for obj in objs:
		pm.setAttr (obj.tx , lock = False , keyable = True )
		pm.setAttr (obj.ty , lock = False , keyable = True )
		pm.setAttr (obj.tz , lock = False , keyable = True )
		pm.setAttr (obj.rx , lock = False , keyable = True )
		pm.setAttr (obj.ry , lock = False , keyable = True )
		pm.setAttr (obj.rz , lock = False , keyable = True )
		pm.setAttr (obj.sx , lock = False , keyable = True )
		pm.setAttr (obj.sy , lock = False , keyable = True )
		pm.setAttr (obj.sz , lock = False , keyable = True )
		pm.setAttr (obj.v , lock = False , keyable = True )

