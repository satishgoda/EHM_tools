import pymel.core as pm
# ==========================================================================================
# Lock and Hide Attributes def
# ==========================================================================================
def LockHideAttr( **kwargs ):
	objs = kwargs.setdefault( 'objs', pm.ls( sl=True ) )
	objs = pm.ls( objs )
	attrs = kwargs.setdefault( 'attrs', 'all' )
	


	# if any attribute is selected in channelBox, lock those attributes only
	selectedAttrs = pm.channelBox( "mainChannelBox", q=True, selectedMainAttributes=True )    
	if selectedAttrs :
		attrs=selectedAttrs

	
	if not objs:
		pm.warning('ehm_tools...LockHideAttr: objs argument needs some object to operate on. No object found!' )
	
	
	for obj in objs:

		if attrs == "all" :
			pm.setAttr (obj.tx  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.ty  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.tz  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.rx  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.ry  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.rz  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.sx  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.sy  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.sz  , lock = True , keyable = False , channelBox = False)
			pm.setAttr (obj.v  , lock = True , keyable = False , channelBox = False)

		elif attrs == "t" :
			pm.setAttr ( obj.tx  ,lock=True , keyable=False , cb=False)
			pm.setAttr ( obj.ty  ,lock=True , keyable=False , cb=False)
			pm.setAttr ( obj.tz  ,lock=True , keyable=False , cb=False)

		elif attrs == "r" :
			pm.setAttr ( obj.rx  ,lock=True , keyable=False , cb=False)
			pm.setAttr ( obj.ry  ,lock=True , keyable=False , cb=False)
			pm.setAttr ( obj.rz  ,lock=True , keyable=False , cb=False)

		elif attrs == "s" :
			pm.setAttr ( obj.sx  ,lock=True , keyable=False , cb=False)
			pm.setAttr ( obj.sy  ,lock=True , keyable=False , cb=False)
			pm.setAttr ( obj.sz  ,lock=True , keyable=False , cb=False)

		elif attrs == "v" : # lock visibility
			pm.setAttr ( obj.v ,lock=True , keyable=False , cb=False)

		elif attrs == "vv" : # hide the object and lock visibility
			pm.setAttr ( obj.v , False ,lock=True , keyable=False , cb=False)

		elif isinstance(attrs,list):
			for attr in attrs:
				pm.setAttr ( obj.attr(attr) ,lock=True , keyable=False , cb=False)
		else:
			pm.setAttr ( obj.attr(attrs) ,lock=True , keyable=False , cb=False)