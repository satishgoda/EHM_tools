from maya import cmds
import maya.OpenMaya as om

def getDagPath( objectName ):
	"""
	return dag path of given object or list of objects
	"""
	if isinstance(objectName, list):
		oNodeList=[]
		for o in objectName:
			selectionList = om.MSelectionList()
			selectionList.add(o)
			oNode = om.MDagPath()
			selectionList.getDagPath(0, oNode)
			oNodeList.append(oNode)
		return oNodeList
	else:
		selectionList = om.MSelectionList()
		selectionList.add(objectName)
		oNode = om.MDagPath()
		selectionList.getDagPath(0, oNode)
		return oNode

def rename( objs=None, name='unNamed', pad=3, prefix="", suffix="", hierarchyMode=False ):
	objs = cmds.ls(objs)
	if not objs :
		objs = cmds.ls (sl=True)
	if not objs:
		cmds.error('ehm_tools...Rename: No object to rename!')
	if hierarchyMode :
		cmds.select (objs[0] , hierarchy = True )
		objs = cmds.ls ( sl = True , long = True )  
	renamedObjects = []	
	for i in range(len(objs)):
		newName=""
		if prefix:
			newName+= (prefix+"_")
		
		newName += name

		if pad:
			zeros = ""
			for j in range(1, pad):
				if ( i<pow(10, j) ):
					zeros += "0"
			newName += ("_"+zeros+str(i+1))
		
		if suffix:
			newName+=("_"+suffix)
		
		renamedObjects.append( cmds.rename(objs[i], newName) )
	
	return renamedObjects