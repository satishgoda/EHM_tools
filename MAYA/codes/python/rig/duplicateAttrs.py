'''
synopsis : 			DuplicateAttrs ( )

what does this script do ?	   finds second object's user defined attributes and adds them
                               to the first object.


how to use:

1. Run the whole code once. 

2. First, 
	select the object you want to duplicate attributes to, 
	then the object you want to duplicate attributes from,   
	optionally select the attributes you like in channel box:   
3. Run three lines below:

objs = pm.ls(sl=True)
DuplicateAttrs( dest=objs[0], source=objs[1], useSelectedAttributes=True )

Author: Ehsan HM

version: 1.0
'''
# ---------------------------------------------------------------------------------

import pymel.core as pm

def DuplicateAttrs( **kwargs ):
	source = kwargs.setdefault( 'source' )
	dest = kwargs.setdefault( 'dest' )

	if not (source and dest):
		objs = pm.ls(sl=True)
		if len( objs )!=2 :
			pm.error( 'select destination and source objects.')
		source = objs[1]
		dest = objs[0]
		
	attrList = pm.listAttr(dest, ud=True)
	destUDattrList = pm.listAttr(source, ud=True)
	if not destUDattrList:
		pm.warning( 'No attribute to duplicate. Skipped!' )
		return None
	
	# if any attribute is selected in channelBox, duplicate those attributes only
	selectedAttrs = pm.channelBox( "mainChannelBox", q=True, selectedMainAttributes=True )    
	if selectedAttrs :
		destUDattrList=selectedAttrs
	
	# if no attribute is selected duplicate all attributes
	for currentAttr in  destUDattrList :
		if currentAttr in attrList:
			pm.warning('Attribute "%s" already exists. Skipped!' % (currentAttr) )

		else:
			# get attr setting
			attrType = pm.addAttr( source.attr(currentAttr), q=True, attributeType=True )
			default = pm.addAttr( source.attr(currentAttr), q=True,  defaultValue=True )
			min = pm.addAttr( source.attr(currentAttr), q=True,  minValue=True )
			max = pm.addAttr( source.attr(currentAttr), q=True,  maxValue=True )
			nice = pm.addAttr( source.attr(currentAttr), q=True, niceName=True )
			locked = pm.getAttr( source.attr(currentAttr), lock=True )
			keyable = pm.getAttr( source.attr(currentAttr), keyable=True )
			channelBox = pm.getAttr( source.attr(currentAttr), channelBox=True )
			
			if attrType == 'enum':
				enumNames = pm.addAttr( source.attr(currentAttr), q=True, enumName=True )
				opt = { 'longName':currentAttr, 'attributeType':attrType, 'defaultValue':default, 'niceName':nice, 'enumName':enumNames }
			else:
				opt = { 'longName':currentAttr, 'attributeType':attrType, 'defaultValue':default, 'niceName':nice }
			
			if min is not None:
				opt['minValue'] = min
			if max is not None:
				opt['maxValue'] = max

			# create new attr on destination      #  DuplicateAttrs ( )
			pm.addAttr( dest ,**opt )
			
			# make it keyable
			# *** should query original attr to see if it is keyable and set accordingly
			pm.setAttr( dest.attr(currentAttr), lock=locked )
			pm.setAttr( dest.attr(currentAttr), keyable=keyable )				
			if not keyable:
				pm.setAttr( dest.attr(currentAttr), channelBox=channelBox )



