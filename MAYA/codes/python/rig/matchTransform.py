import pymel.core as pm
from codes.python.general import unlockUnhideAttrs 
UnlockUnhideAttrs = unlockUnhideAttrs.UnlockUnhideAttrs

def MatchTransform( force=True, folower=None, lead=None, translate=True, rotate=True, scale=True ):
	
	# if this method is being perfomed on selected objects
	# retrieve selection after job is done
	selection = pm.ls(sl=True)
	
	if folower==None or lead==None:
		selectionMode = True 
		folower, lead = pm.ls(sl=True)
	
	if force: # in case object are parented under scaled groups or their pivot has been moved
		
		null = pm.duplicate( folower )[0]
		pm.delete( pm.listRelatives( null, ad=True ) )
		UnlockUnhideAttrs( objs=null )
		
		if translate:
			pm.delete( pm.pointConstraint( lead, null ) )
			try:
				folower.translate.set( null.translate.get() )
			except:
				pass
		if rotate:
			pm.delete( pm.orientConstraint( lead, null ) )
			try:
				folower.rotate.set( null.rotate.get() )
			except:
				pass
		if scale:
			pm.delete( pm.scaleConstraint( lead, null ) )
			try:
				folower.scale.set( null.scale.get() )
			except:
				pass
		pm.delete( null )
		pm.select( selection )

	else:
		if translate:
			trans = pm.xform( lead , q=True, translation=True, ws=True )

		if rotate:
				rotate = pm.xform( lead , q=True, rotation=True, ws=True )

		if scale:
			scale = pm.xform( lead , q=True, scale=True, relative=True )

		pm.xform( folower, t=trans, ws=True )
		pm.xform( folower, ro=rotate, ws=True )
		pm.xform( folower, s=scale )