# find inputs on source and connects them to dest instead
# for tranfering input nodes to an upper group is good
# so that your source will be zerod out
#
# If selected objects are blendshape nodes, only connects normal connections not geometry inputs and such
#
# 		from ehm_scripts.rig import transferInConnections
# 		transferInConnections.TransferInConnections()
#
#----------------------------------------------------------------------------

import pymel.core as pm
from codes.python.rig import duplicateAttrs
reload( duplicateAttrs )
DuplicateAttrs	=	duplicateAttrs.DuplicateAttrs


def TransferInConnections( **kwargs ):
	source = kwargs.setdefault( 'source' )
	dest = kwargs.setdefault( 'dest' )
	
	if not ( source and dest ):
		objs = pm.ls(sl=True)
		if len( objs )!=2 :
			pm.error( 'select destination and source objects.')
		source = objs[1]
		dest = objs[0]	
	
	# find user difined attributes from source and create them for dest
	DuplicateAttrs( **kwargs )
	

	sourceIns  = pm.listConnections( source , connections=True, destination=False, skipConversionNodes=True, plugs=True )
	
	if not sourceIns:
		pm.warning( 'No attribute to transfer. Skipped!' )
		return None
	
	for i in range( 0 , len(sourceIns) ):
		inAttr = sourceIns[i][1]
		outAttr = sourceIns[i][0]

		attrName = sourceIns[i][0].name().split('.')[1]

		inAttrName = sourceIns[i][1].name().split('.')[1]

		if inAttr != dest.attr(attrName) : # prevent things to connect to themselves

			if source.type() == 'blendShape' :
				if (inAttrName != 'outputGeometry') and (inAttrName != 'groupId') and (inAttrName != 'worldMesh[0]'):
					inAttr // outAttr
					inAttr >> dest.attr(attrName)
			else:
				inAttr // outAttr
				inAttr >> dest.attr(attrName)

		else:
			pm.warning("Can not connect attribute to itself.")
