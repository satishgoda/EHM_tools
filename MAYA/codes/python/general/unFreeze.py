import pymel.core as pm

def UnFreeze( objs=None ):
	# ==========================================================================================
	# UnFreezes transforms
	# ==========================================================================================
	
	if not objs:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	if not objs:
		pm.warning('ehm_tools...UnFreeze: objs argument needs some object to operate on. No object found!' )
	
	for obj in objs:
		pm.makeIdentity( obj, apply=True, t=1, r=1, s=1 )
		piv = obj.rotatePivot.get()
		obj.translate.set( -piv )
		pm.makeIdentity( obj, apply=True, t=1, r=1, s=1 )
		obj.translate.set( piv )