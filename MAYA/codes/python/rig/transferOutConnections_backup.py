'''
synopsis : 			TransferOutConnections( dest, source, useSelectedAttributes )

what does this script do ?	   finds second object's output connections and replaces them
                               with your first object.
                               useful for places you want to change your contoler but you want
                               to keep the connections.


how to use:

1. Run the whole code once. 

2. First, select the object you want to transfer attributes to
	, then the object you want to transfer attributes form
	, optionally select the attributes you like in channel box:    

3. Run three lines below:

objs = pm.ls(sl=True)
TransferOutConnections( dest=objs[0], source=objs[1], useSelectedAttributes=True)

Author: Ehsan HM
'''
# ---------------------------------------------------------------------------------


import pymel.core as pm
from codes.python.rig.duplicateAttrs import DuplicateAttrs

def TransferOutConnections( **kwargs ):
	source = kwargs.setdefault( 'source' )
	dest = kwargs.setdefault( 'dest' )
	useSelectedAttributes = kwargs.setdefault( 'useSelectedAttributes' )
	

	if not ( source and dest ):
		objs = pm.ls(sl=True)
		if len( objs )!=2 :
			pm.error( 'select destination and source objects.')
		source = objs[1]
		dest = objs[0]

	# find user difined attributes from source and create them for dest
	DuplicateAttrs( **kwargs )

	sourceOuts  = pm.listConnections( source , connections=True, source=False, skipConversionNodes=True, plugs=True )

	if useSelectedAttributes :
		selectedAttrs = pm.channelBox( "mainChannelBox", q=True, selectedMainAttributes=True )    
		if selectedAttrs :
			selectedSourceOuts = []
			for i in selectedAttrs:
				for j in sourceOuts:
					if source.attr( i ) in j:
						selectedSourceOuts.append( j )
			sourceOuts = selectedSourceOuts

		else:
			sourceOuts = None
			pm.warning( 'selected attributes are not connected. Skipped!' )

	if sourceOuts:	
		for i in range( len(sourceOuts) ):
			outAttr = sourceOuts[i][0]
			inAttr = sourceOuts[i][1]
			attrName = sourceOuts[i][0].name().split('.')[1]
		
			if attrName != 'message':
				outAttr // inAttr
		
				# connections
				dest.attr(attrName)        >>      inAttr
	else:
		pm.warning( 'No attribute to transfer. Skipped!' )