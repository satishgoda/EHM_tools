import pymel.core as pm

from codes.python.general import renamer
reload( renamer )
Renamer = renamer.Renamer

from codes.python.rig.makeSplineStretchy import MakeSplineStretchy

from codes.python.rig import divideJnt
DivideJnt = divideJnt.DivideJnt

from codes.python.rig.orientMirroredJnt import OrientMirroredJnt


def Segmentor ( **kwargs ):
	numOfSegs =			kwargs.setdefault( 'numOfSegs' , 5 )
	jnt = 				kwargs.setdefault( 'jnt', pm.ls( sl=True ) )
	volume = 			kwargs.setdefault( 'volume' , False )
	thicknessPlace =	kwargs.setdefault( 'thicknessPlace' , 'mid' )
	stretchSwitch = 	kwargs.setdefault( 'stretchSwitch' , False )
	isMirroredJoint = 	kwargs.setdefault( 'isMirroredJoint' , False )


	if not jnt:
		pm.error( 'ehm_tools...segmentor: jnt argument accepts a joint. select a joint!' )
	else:
		jnt = pm.ls( jnt )[0]	

	if not jnt.type() == 'joint':
		pm.error( 'ehm_tools...segmentor: jnt argument accepts a joint. "%s" was given instead!' %jnt  )

	children = jnt.getChildren()
	if not children :
		pm.error('ehm_tools...segmentor: selected joint must have a child joint.')
	else:
		child = children[0]

	segName = jnt.name()


	#============================================================================
	# duplicate main arm joints and rename bendy joints
	dupStartJnt = pm.duplicate ( jnt )[0]
	dupEndJnt = pm.duplicate ( child )[0]

	pm.delete ( pm.listRelatives ( dupStartJnt, ad=True ) )
	pm.delete ( pm.listRelatives ( dupEndJnt, ad=True ) )

	pm.parent ( dupEndJnt , dupStartJnt )


	# reverse orientation if needed
	if isMirroredJoint == True:
		OrientMirroredJnt( jnts = [ dupEndJnt , dupStartJnt ] )

	#============================================================================
	# finding the position for segMainJnts and creating them


	segJnts = DivideJnt( dupStartJnt, numOfDivisions=numOfSegs ).newJnts

	Renamer( objs=segJnts, name="%s_seg_###_jnt" %segName  , hierarchyMode=False)


	#============================================================================
	# creating ik splines for segmenty joints

	limb_seg_ik_stuff = pm.ikHandle ( sj=dupStartJnt , ee=dupEndJnt , sol = "ikSplineSolver" , parentCurve = False , ns = 2 )
	limb_seg_ikh = pm.rename (  limb_seg_ik_stuff[0] ,  "%s_limb_seg_ikh" %segName  )
	limb_seg_eff = pm.rename (  limb_seg_ik_stuff[1] ,  "%s_limb_seg_eff" %segName  )
	limb_seg_crv = pm.rename (  limb_seg_ik_stuff[2] ,  "%s_limb_seg_crv" %segName  )

	limb_seg_crv.inheritsTransform.set( False )
	
	#============================================================================
	# setting the twist parameters for the segmenty joints

	limb_seg_ikh.dTwistControlEnable.set( 1 )
	limb_seg_ikh.dWorldUpType.set( 4 )


	#============================================================================
	# clean up
	segStuffGrp = pm.group ( limb_seg_crv , limb_seg_ikh , segJnts[0] , name = "%s_seg_stuff" %segName )


	#============================================================================
	# making the joints stratchable

	MakeSplineStretchy ( thicknessPlace=thicknessPlace, stretchSwitch=stretchSwitch, volume=volume, ikCrv=limb_seg_crv )

	return ( segJnts, limb_seg_ik_stuff, segStuffGrp )