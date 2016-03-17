# GetAllChildren()
# returns object's all children as a list, if includeItself true, then
# new list includes and starts with specified object itself
# ============================================================================

import pymel.core as pm


def GetAllChildren( objs=None, childType=None, includeItself=True ):
	
	childrenLists = []
	
	childrenList = []

	if objs==None:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	
	for obj in objs:

		if not childType:
			childrenList = obj.listRelatives( ad=True )
		else:
			childrenList = obj.listRelatives( ad=True, type=childType )

		if includeItself == True:
			childrenList.append( obj )

	childrenList.reverse()

	childrenLists.append( childrenList )
	
	if len( objs ) == 1:
		return childrenList
	else:
		return childrenLists
