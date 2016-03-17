# script name : skinToClust
#
# author : Ehsan H.M
#import pymel.core as pm
# what does this script do ?		convert skinCluster to clusters
#
# synopsis :   		                SkinToClust ()
#
# flags :			                None
#
# requirement : 	                None
#
# how to use:                       select the joints, source surface then destinaiton surface and click the shelf button
#
# How to make a shlef button:
#
#						change " M:\MAYA_REPOSITORY\ehm_scripts " to where you've copied the script in the first line below,
#						make a shelf buttun from all lines below without # and empty space after it:
#
#						import sys
#						sys.path.append( 'M:\MAYA_REPOSITORY\ehm_scripts' )
#						from ehm_scripts.rig import skinToClust
#						skinToClust.SkinToClust()
#
#============================================================================

import pymel.core as pm

def SkinToClust ( joints=None, sourceGeometry=None, finalGeometry=None  ):

	#============================================================================
	# user inputs
	if sourceGeometry==None or finalGeometry==None or joints==None:
		geoAndJnts = pm.ls(sl=True)
		sourceGeometry = geoAndJnts[ len (geoAndJnts) -2 ]
		finalGeometry = geoAndJnts[ len (geoAndJnts) -1 ]
		joints = geoAndJnts[:len (geoAndJnts) -2 ]


	#============================================================================
	# find the skinCluster node on given objects

	skinClust =   pm.ls ( pm.listHistory (sourceGeometry ) ,  type = "skinCluster" )[0]



	if skinClust == []:
		pm.error( "Source Object is not skinned." )

	#============================================================================
	# create a list per selected influence containing
	# all the vertices and their weights

	# find shape of sourceShape
	sourceShape = sourceGeometry.getShape()

	# find shape of finalShape
	finalShape = finalGeometry.getShape()

	# find the number of vertices of sourceGeometry
	numOfVtxs = pm.polyEvaluate(finalGeometry) ["vertex"]

	jnt = joints[0]

	for jnt in joints:

		# start progress window
		amount = 0
		pm.progressWindow(    title= str(jnt),
											progress=0,
											status=("  find " + str(jnt) + " weights:"),
											isInterruptable=True )


		# create a dictionary containing all the values
		#==================
		tempDic = {}
		zeroVtxs = []

		# create counter for amount for status present
		if numOfVtxs != 0:
			counter = 100.0 / numOfVtxs

		vtx = 1
		for vtx in range(numOfVtxs):

			# get values from skinCluster
			tempVal = pm.skinPercent ( skinClust  , sourceShape.vtx[vtx] ,q =True , value=True , transform = jnt )

			# if the value is not 0 then add it to dictionary
			if not (  tempVal == 0 ):
				tempDic [vtx] = tempVal

			# else create a list containing 0 valued vertices
			else:
				zeroVtxs.append ( finalGeometry.vtx[vtx]  )

			# change progress window
			# pm.progressWindow ( edit=True, progress= int (amount), status=("  find " + str(jnt) + " weights:") )

			# change amount for status present
			amount += counter

		# end progress window
		pm.progressWindow(endProgress=1)


		# create a cluster in the position of the joint
		#==================
		currentClustAndHandle =  pm.cluster( finalShape , rel=True , n = (str(jnt)+"clust") )

		currentClust  = pm.ls( currentClustAndHandle[0] )[0]
		currentClustHandle = pm.ls( currentClustAndHandle[1] )[0]


		# change membership of cluster
		#==================

		# start progress window
		amount = 0
		pm.progressWindow(    title= str(jnt),
											progress=0,
											status=("  change " + str(jnt) + " membership:"),
											isInterruptable=True )


		# create counter for amount for status present
		if len(zeroVtxs) != 0:
			counter = 100.0 / len(zeroVtxs)

		pm.sets ( currentClust+"Set" , rm = zeroVtxs )

		# end progress window
		pm.progressWindow(endProgress=1)

		# positioning the clusters
		#==================

		# get position from current joint
		clustPos = pm.xform (jnt , q =True , ws=True , t=True )

		# set cluster origin values
		currentClustHandle.origin.set( clustPos )

		# center pivot of cluster
		pm.xform( currentClustHandle , centerPivots=True)



		# start progress window
		#====================

		# create a new progress window
		amount = 0
		pm.progressWindow(    title= str(jnt),
											progress=0,
											status=(" apply " + str(jnt) + " weights:") ,
											isInterruptable=True )

		# create counter for amount for status present
		if len(tempDic) != 0:
			counter = 100.0 / len(tempDic)

		# get the values from dictionary we've created and use them as cluster weights
		#==================
		for vtx in tempDic:

			# applying values
			pm.percent ( currentClust , finalShape.vtx[vtx] ,  v = tempDic [vtx] )

			# change progress window
			#pm.progressWindow ( edit=True, progress= int (amount), status=(" apply " + str(jnt) + " weights:") )

			# change amount for status present
			amount += counter

		# end progress window
		pm.progressWindow(endProgress=1)