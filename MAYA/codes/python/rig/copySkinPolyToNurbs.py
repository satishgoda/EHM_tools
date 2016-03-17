# script name: ehm_copySkinPolyToNurbs
#
# Author: Ehsan HM
#
# What does this do?  copies skinWeights from polygon to nurbs
#
# How to use:			select polyMesh, then nurbs surface and run this
#
# flags:
# 						source, must be polygon
# 						dest, must be Nurbs surface
# 						searchTolerance, is used to find closet nurbs CV to current poly vertex
#               		set it pretty low or result would be unpredictable.
#
# How to make a shlef button:
#
#						change " M:\MAYA_REPOSITORY\ehm_scripts " to where you've copied the script in the first line below,
#						make a shelf buttun from all lines below without # and empty space after it:
#
#						import sys
#						sys.path.append( 'M:\MAYA_REPOSITORY\ehm_scripts' )
#						import copySkinPolyToNurbs
#						copySkinPolyToNurbs.CopySkinPolyToNurbs()
#
#
# Notes:		This works best, if polymesh is created by converting the nurbs to poly
#				from modify, convert menu
#
#================================================================================

import pymel.core as pm
from codes.python.rig import findDeformers
FindDeformers = findDeformers.FindDeformers

def CopySkinPolyToNurbs( source=None , dest=None, searchTolerance=0.005 ):

	if source==None or dest==None :
		source, dest = pm.ls(sl=True)

	# find shapes and skin nodes
	sourceShape = source.getShape()
	sourceSkin = FindDeformers( sourceShape , 'skinCluster' )
	if not sourceSkin:
		pm.error("source object doesn't have a skin deformer")
	sourceSkin = sourceSkin[0]	
	
	destShape = dest.getShape()
	destSkin = FindDeformers( destShape , 'skinCluster' )
	if not destSkin:
		pm.error("target object doesn't have a skin deformer")
	destSkin = destSkin[0]
	
	# find joints affection the skin
	sourceJnts = pm.skinCluster(sourceSkin, q=True, influence=True)
	destJnts = pm.skinCluster(destSkin, q=True, influence=True)
	if sourceJnts != destJnts:
		pm.error("SkinClusters must have the same joint.")

	Us = destShape.numCVsInU()
	Vs = destShape.numCVsInV()
	numVtxs= pm.polyEvaluate( sourceShape, v=True )

	# unlock all joint
	for jnt in destJnts:
		jnt.liw.set(0)


	#===============================
	pm.select(cl=True)
	for U in range(Us):
		for V in range(Vs):
			pm.select( destShape.cv[U][V], add=True )
			pos = destShape.getCV( U, V, space='world' )

			# find vertex by position
			pm.select( source.vtx[0:numVtxs-1])
			pm.polySelectConstraint( mode=2, type=1, dist=1, distbound=(0,searchTolerance), distpoint=pos )
			vtx = pm.ls(sl=True)[0]
			pm.polySelectConstraint( dist=0 )

			# find wieghts from found vertex
			wtList = []
			rawWts = pm.skinPercent( sourceSkin, vtx, q=True, value=True  )

			# find joints affection the vertex
			jntList = []
			for i in range(len(rawWts)):
				if rawWts[i] > 0.0:
					jntList.append(sourceJnts[i])
					wtList.append(rawWts[i])

			# set weights to nurbs point
			opt = []
			for j in range(len(jntList)):
				tmp= []
				tmp.append( str(jntList[j]) )
				tmp.append( wtList[j] )
				opt.append( tmp )

			pm.skinPercent( str(destSkin), destShape.cv[U][V] , transformValue=( opt )  )