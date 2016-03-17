import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
import math

nodeName = 'sinNode'
nodeID = OpenMaya.MTypeId( 0x0011E185 )

# node definition
class sinNode( OpenMayaMPx.MPxNode ):
	
	input = OpenMaya.MObject()
	output = OpenMaya.MObject()
	
	def __init__( self ):
		OpenMayaMPx.MPxNode.__init__( self )
	
	def compute( self, plug, dataBlock ):
		if ( plug == sinNode.output ):
			dataHandle = dataBlock.inputValue( sinNode.input )
			
			inputFloat = dataHandle.asFloat()
			result = math.sin( inputFloat )
			
			outputHandle = dataBlock.outputValue( sinNode.output )
			outputHandle.setFloat( result )
			
			dataBlock.setClean( plug )
			
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( sinNode() )

def nodeInitializer():
	# input
	nAttr = OpenMaya.MFnNumericAttribute()
	sinNode.input = nAttr.create( 'input', 'in', OpenMaya.MFnNumericData.kFloat, 0.0 )
	nAttr.setStorable(1)
	nAttr.setWritable(1)
	
	# output
	nAttr = OpenMaya.MFnNumericAttribute()
	sinNode.output = nAttr.create( 'output', 'out', OpenMaya.MFnNumericData.kFloat, 0.0 )
	nAttr.setStorable(0)
	nAttr.setWritable(0)
	
	# add attributes
	sinNode.addAttribute( sinNode.input )
	sinNode.addAttribute( sinNode.output )
	sinNode.attributeAffects( sinNode.input, sinNode.output )
	

# init plugin
def initializePlugin( mobject):
	mplugin = OpenMayaMPx.MFnPlugin( mobject)
	try:
		mplugin.registerNode( nodeName, nodeID, nodeCreator, nodeInitializer )
	except:
		sys.stderr.write( 'failed to load node: sinNode' )
		raise

# uninit plugin
def uninitializePlugin( mobject):
	mplugin = OpenMayaMPx.MFnPlugin( mobject)
	try:
		mplugin.deregisterNode( nodeID )
	except:
		sys.stderr.write( 'failed to unload plugin sinNode' )
		raise
	
	
	