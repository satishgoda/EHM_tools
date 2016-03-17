import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
import math

nodeName = 'cosNode'
nodeID = OpenMaya.MTypeId( 0x001427 )

# node definition
class cosNode( OpenMayaMPx.MPxNode ):
	
	input = OpenMaya.MObject()
	output = OpenMaya.MObject()
	
	def __init__( self ):
		OpenMayaMPx.MPxNode.__init__( self )
	
	def compute( self, plug, dataBlock ):
		if ( plug == cosNode.output ):
			dataHandle = dataBlock.inputValue( cosNode.input )
			
			inputFloat = dataHandle.asFloat()
			result = math.cos( inputFloat )
			
			outputHandle = dataBlock.outputValue( cosNode.output )
			outputHandle.setFloat( result )
			
			dataBlock.setClean( plug )
			
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( cosNode() )

def nodeInitializer():
	# input
	nAttr = OpenMaya.MFnNumericAttribute()
	cosNode.input = nAttr.create( 'input', 'in', OpenMaya.MFnNumericData.kFloat, 0.0 )
	nAttr.setStorable(1)
	nAttr.setWritable(1)
	
	# output
	nAttr = OpenMaya.MFnNumericAttribute()
	cosNode.output = nAttr.create( 'output', 'out', OpenMaya.MFnNumericData.kFloat, 0.0 )
	nAttr.setStorable(0)
	nAttr.setWritable(0)
	
	# add attributes
	cosNode.addAttribute( cosNode.input )
	cosNode.addAttribute( cosNode.output )
	cosNode.attributeAffects( cosNode.input, cosNode.output )
	

# init plugin
def initializePlugin( mobject):
	mplugin = OpenMayaMPx.MFnPlugin( mobject)
	try:
		mplugin.registerNode( nodeName, nodeID, nodeCreator, nodeInitializer )
	except:
		sys.stderr.write( 'failed to load node: cosNode' )
		raise

# uninit plugin
def uninitializePlugin( mobject):
	mplugin = OpenMayaMPx.MFnPlugin( mobject)
	try:
		mplugin.deregisterNode( nodeID )
	except:
		sys.stderr.write( 'failed to unload plugin cosNode' )
		raise
	
	
	