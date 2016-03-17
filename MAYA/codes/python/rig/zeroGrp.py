import pymel.core as pm
# ---------------------------------------------------------------------------------
'''
synopsis : zeroGrp ()

what does this do ?
       It creates empty groups on top of selected objects and transfer the transform
       values to this group. use this instead of -----FREEZE TRANSFORM------ for your objects.

how to use :  

objs = pm.ls( sl=True )[0]

ZeroGrp( objs=objs )

note : 	  doesn't work on clusters

return :    newly created  zero groups and ofs groups
'''
# ---------------------------------------------------------------------------------

def ZeroGrp( objs=None ) :

	if not objs:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	zeroGrps = [] # zero grps for return 
	ofsGrps = [] # ofs grps for return
		
	for obj in objs:
		
		if '|' in obj.name():
			name = obj.name().split('|')[-1]
		else:
			name = obj.name()
		
		zeroGrp = pm.group ( em = True ,  name  = ( name + "_zero"  ) )
		pm.xform (os = True , piv =  (0,0,0) )
		pm.select (obj , add = True )
		parentJnt = obj.getParent()
	
		if not parentJnt:
			pm.parent()
			zeroGrp.translate.set(0,0,0)
			zeroGrp.rotate.set(0,0,0)
			zeroGrp.scale.set(1,1,1)
			pm.parent (w = True)
			pm.parent( obj ,   zeroGrp  )
			ofsGrp = pm.group ( name = ( name + "_ofs") )
			pm.xform ( os = True , piv = (0,0,0) )
			
		elif parentJnt:
			pm.parent()
			zeroGrp.translate.set(0,0,0)
			zeroGrp.rotate.set(0,0,0)
			zeroGrp.scale.set(1,1,1)
			pm.select (parentJnt , add = True )
			pm.parent()
			pm.parent( obj , zeroGrp  )
			ofsGrp = pm.group ( name = ( name + "_ofs") )
			pm.xform ( os = True , piv = (0,0,0) )

		zeroGrps.append ( zeroGrp )
		ofsGrps.append ( ofsGrp )
		

	pm.select( zeroGrps )
	
	if len(objs) == 1:
		return ( zeroGrps[0], ofsGrps[0] )
	else:
		return ( zeroGrps, ofsGrps )

