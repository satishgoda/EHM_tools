# import the OpenMaya module
import maya.OpenMaya as OpenMaya

# function that returns a node object given a name
def nameToNode( name ):
 selectionList = OpenMaya.MSelectionList()
 selectionList.add( name )
 node = OpenMaya.MObject()
 selectionList.getDependNode( 0, node )
 return node

# function that returns a
def nameToDag( name ):
 selectionList = OpenMaya.MSelectionList()
 selectionList.add( name )
 dagPath = OpenMaya.MDagPath()
 selectionList.getDagPath(0, dagPath)
 return dagPath
 
# function that finds a plug given a node object and plug name
def nameToNodePlug( attrName, nodeObject ):
 depNodeFn = OpenMaya.MFnDependencyNode( nodeObject )
 attrObject = depNodeFn.attribute( attrName )
 plug = OpenMaya.MPlug( nodeObject, attrObject )
 return plug

# function that finds a paramater Nurbs curve for a given position
def getParametrCurve(cvName, pt):
	cpNode = nameToNode( cvName )
	cpDag = nameToDag( cvName )
	wPoint = OpenMaya.MPoint(pt[0],pt[1],pt[2])
	# connect the MFnNurbsCurve
	# and ask the closest point
	nurbsCurveFn = OpenMaya.MFnNurbsCurve(cpDag)
	# get and set outPosition
	outParam = OpenMaya.MScriptUtil()
	outParam.createFromDouble(0)
	outParamPtr = outParam.asDoublePtr()       
	outPosition = nurbsCurveFn.closestPoint(wPoint, True, outParamPtr ,0.001, OpenMaya.MSpace.kWorld)
	Param = OpenMaya.MScriptUtil.getDouble(outParamPtr)
	
	MinMaxValuePlug = nameToNodePlug( "minMaxValue", cpNode )
	MinMaxValue = MinMaxValuePlug.asMDataHandle().asDouble2()
	
	res=Param/MinMaxValue[1]
	return res

