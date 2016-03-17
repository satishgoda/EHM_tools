import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys

nodeName = 'ehm_pushDeformer'
nodeId = OpenMaya.MTypeId( 0x0011E187 )

class ehm_pushDeformer( OpenMayaMPx.MPxDeformerNode ):
	
	colliderMatrix = OpenMaya.MObject()
	
	def __init__( self ):
		OpenMayaMPx.MPxDeformerNode.__init__( self )
	
	def deform( self, dataBlock, geoItr, matrix, index ):
		
		# envelope
		envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
		envelopeHandle = dataBlock.inputValue( envelope )
		envelopeValue = envelopeHandle.asFloat()
		
		if not envelopeValue:
			return OpenMaya.MStatus.kSuccess
		

		# 0. get deformer input
		input = OpenMayaMPx.cvar.MPxDeformerNode_input
		
		# 1. Attach a handle to input Array Attribute.
		inputHandle_array = dataBlock.outputArrayValue( input )
		
		# 2. Jump to particular element
		inputHandle_array.jumpToElement( index )
				
		# 3. Attach a handle to specific data block
		inputHandle_element = inputHandle_array.outputValue()
		
		# 4. Reach to the child - inputGeom
		inputGeom = OpenMayaMPx.cvar.MPxDeformerNode_inputGeom
		inMeshHandle = inputHandle_element.child( inputGeom )
		
		# 5. get Mesh
		inMesh = inMeshHandle.asMesh()
		
		# Envelope
		envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
		envelopeHandle = dataBlock.inputValue( envelope )
		envelopeValue = envelopeHandle.asFloat()
		
		# pushValue
		pushHandle = dataBlock.inputValue( self.push )
		pushValue = pushHandle.asFloat()
		


		inmeshVertexItr = OpenMaya.MItMeshVertex( inMesh ) #  using this we have complete control over geometry.	getConnectedVertices()
		# meshFn = OpenMaya.MFnMesh( inMesh ) # using this we can get and set all point positions in one step
		
		origPoses = OpenMaya.MPointArray() # original points' positions list
		geoItr.allPositions( origPoses, OpenMaya.MSpace.kObject ) # get original point positions
		
		
		finalPoses = OpenMaya.MPointArray() # list of average positions of all neighbour vertices'  positions	
		
		# deform
		while not geoItr.isDone():
			
			currentVertIndex = inmeshVertexItr.index()
			# weight
			weight = self.weightValue( dataBlock, index, currentVertIndex )	
			
			#if weight:
			# get normal
			normal_util = OpenMaya.MScriptUtil()
			normal_util.createFromList([1.0, 1.0, 1.0], 3)
			normal = OpenMaya.MVector( normal_util.asDoublePtr() )
			vertexIndex = geoItr.index()

			
			index_util = OpenMaya.MScriptUtil()
			index_util.createFromInt(0)
			indexPtr = index_util.asIntPtr()
			
			inmeshVertexItr.setIndex( vertexIndex, indexPtr )
			inmeshVertexItr.getNormal( normal , OpenMaya.MSpace.kObject  )
			#normal_inWorldSpace =  normal #* matrix
			

			# consider ENVELOPE and WEIGHTS value in calculations in 4 steps
			pushAmount = normal * pushValue * envelopeValue * weight ;

			
			pointPosition =  inmeshVertexItr.position() # new point position in world space * matrix 
			finalPos = pointPosition + pushAmount  # new point position in local space * matrix.inverse()
		
			#else: # if weight is 0.0
			#	finalPos =  geoItr.position() #origPoses[ currentVertIndex ]
			'''
			this part was supposed to make this deformer quicker 
			but setting original position 
			of each vertex that has a weight value of 0.0
			but it has a bug and doesn't work.
			'''
			
			finalPoses.append( finalPos )
			
			
			geoItr.next()
			
		geoItr.setAllPositions( finalPoses )
		
		

def nodeCreator():
	return OpenMayaMPx.asMPxPtr( ehm_pushDeformer() )

def nodeInitializer():
	
	# add attribute function set
	nAttr = OpenMaya.MFnNumericAttribute()
	
	# input
	ehm_pushDeformer.push = nAttr.create( 'push', 'pu', OpenMaya.MFnNumericData.kFloat, 0.0 )
	nAttr.setReadable( 1 )
	nAttr.setWritable( 1 )
	nAttr.setStorable( 1 )
	nAttr.setKeyable( 1 )
	
	
	
	# add attributes
	ehm_pushDeformer.addAttribute( ehm_pushDeformer.push )
	
	
	
	# design circuitary
	outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
	ehm_pushDeformer.attributeAffects( ehm_pushDeformer.push, outputGeom )

	# make deformer paintable
	# OpenMaya.MGlobal.executeCommand( "makePaintable -attrType multiFloat -sm deformer ehm_pushDeformer weights;" )
	
	# make deformer paintable
	OpenMaya.MGlobal.executeCommand( "makePaintable -attrType multiFloat -sm deformer ehm_pushDeformer weights;" )
	
	
def initializePlugin( mObj ):
	plugin = OpenMayaMPx.MFnPlugin( mObj, 'Ehsan HM', '1.0', 'any' )
	try:
		plugin.registerNode( nodeName, nodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kDeformerNode )
	except:
		sys.stderr.write( 'Faild to load plugin: %s' % nodeName )
	
		
def uninitializePlugin( mObj ):
	plugin = OpenMayaMPx.MFnPlugin( mObj )
	try:
		plugin.deregisterNode( nodeId )
	except:
		sys.stderr.write( 'Faild to unload plugin: %s' % nodeName )