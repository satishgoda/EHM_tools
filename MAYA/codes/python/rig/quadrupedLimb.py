'''
# what does this script do ?		 rigs the arm

from codes.python.everyone_can_rig import quadrupedLimb
quadrupedLimb.QuadrupedLimb_init( mode='leg' )
quadrupedLimb.QuadrupedLimb_pack( mode='leg' )

quadrupedLimb.QuadrupedLimb_init()
quadrupedLimb.QuadrupedLimb_pack()


QuadrupedLimb_init( mode='leg' )
QuadrupedLimb_pack( mode='leg' )

QuadrupedLimb_init( mode='arm' )
QuadrupedLimb_pack( mode='arm' )

'''

#============================================================================

import pymel.core as pm

import codes.python.rig as RIG
import codes.python.general as GNL
import codes.python.curves as CRV

LockHideAttr 		=	GNL.lockHideAttr.LockHideAttr
JntToCube 			=	RIG.jntToCube.JntToCube
FindPosBetween		=	RIG.findPosBetween.FindPosBetween
MirrorObjLikeJnt	=	GNL.mirrorObjLikeJnt.MirrorObjLikeJnt
ReverseShape		=	GNL.reverseShape.ReverseShape
RigFK 				=	RIG.rigFK.RigFK
RigIK 				=	RIG.rigIK.RigIK
RigFKIK 			=	RIG.rigFKIK.RigFKIK
RigBendyLimb		=	RIG.rigBendyLimb.RigBendyLimb


def WorldPos( obj ):
	try:
		return pm.xform( obj,q=True,t=True,ws=True )
	except:
		raise Exception( 'ehm_tools...quadrupedLimb.WorldPos: could not query world position of object %s'%obj )



#========================================================================================================
# make initial joints for starting the rig
#========================================================================================================

def QuadrupedLimb_init( **kwargs ):
	QuadrupedLimbSize = kwargs.setdefault( 'QuadrupedLimbSize', 1.0 )
	mode = kwargs.setdefault( 'mode', 'arm' )
	side = kwargs.setdefault( 'side', 'L' )
	
	global QuadrupedLimbInitJnts
	QuadrupedLimbInitJnts = []
	
	if mode == 'arm':
		pm.select( clear = True )
		QuadrupedLimbInitJnts.append( pm.joint ( p = ( QuadrupedLimbSize * 3      , QuadrupedLimbSize*13 , 0) , name = "%s_uparm_initJnt"%side ) )
		
		QuadrupedLimbInitJnts.append( pm.joint ( p = ( QuadrupedLimbSize * 7      , QuadrupedLimbSize*13 , 0) , name = "%s_elbow_initJnt"%side ) )
		pm.joint( QuadrupedLimbInitJnts[0], e=True, zso=True, oj='xyz', sao='yup')
		
		QuadrupedLimbInitJnts.append( pm.joint ( p = ( QuadrupedLimbSize * 11     , QuadrupedLimbSize*13 , 0) , name = "%s_hand_initJnt"%side ) )
		pm.joint( QuadrupedLimbInitJnts[1], e=True, zso=True, oj='xyz', sao='yup')
		
		QuadrupedLimbInitJnts.append( pm.joint ( p = ( QuadrupedLimbSize * 12     , QuadrupedLimbSize*13 , 0) , name = "%s_handEnd_initJnt"%side ) )
		pm.joint( QuadrupedLimbInitJnts[2], e=True, zso=True, oj='xyz', sao='yup')
		
		pm.select ( clear=True )


	elif mode == 'leg':
		pm.select( clear = True )
		QuadrupedLimbInitJnts.append( pm.joint(p=(2,7,0), name = "L_initupLimbJnt") )

		QuadrupedLimbInitJnts.append( pm.joint(p=(2,4,0), name = "L_initmidLimbJnt") )
		pm.joint( QuadrupedLimbInitJnts[0], e=True, zso=True, oj='xzy', sao='xup' )

		QuadrupedLimbInitJnts.append( pm.joint(p=(2,1,0), name = "L_initbutLimbJnt") )
		pm.joint( QuadrupedLimbInitJnts[1], e=True, zso=True, oj='xzy', sao='xup')

		QuadrupedLimbInitJnts.append( pm.joint(p=(2,0,-1), name = "L_initHeelJnt") )
		pm.joint( QuadrupedLimbInitJnts[2], e=True, zso=True, oj='xzy', sao='xup')

		QuadrupedLimbInitJnts.append( pm.joint(p=(2,0,1), name = "L_initendLimbJnt") )
		pm.joint( QuadrupedLimbInitJnts[3], e=True, zso=True, oj='xzy', sao='xup')

		QuadrupedLimbInitJnts.append( pm.joint(p=(2,0,2), name = "L_initToeEndJnt") )
		pm.joint( QuadrupedLimbInitJnts[4], e=True, zso=True, oj='xzy', sao='xup')

		pm.select ( clear=True )


		
#========================================================================================================
# pack the arm rig
#========================================================================================================

def QuadrupedLimb_pack( **kwargs ):
	FKIKMode = kwargs.setdefault( 'FKIKMode', 'FKIK' )
	mirror = kwargs.setdefault( 'mirror', True )
	numOfSegs = kwargs.setdefault( 'numOfSegs',10 )
	bendy = kwargs.setdefault( 'bendy', True  )
	mode = kwargs.setdefault( 'mode', 'arm' )

	quadrupedLimbJnts = []
	FKIKstuff = []
	OSquadrupedLimbJnts = []	
	OSFKIKstuff = []	
	
	#============================================================================
	# find some info for naming and control sizes

	side = QuadrupedLimbInitJnts[0].name()[0]
	limbLen = GNL.dist.Dist( QuadrupedLimbInitJnts[0] , QuadrupedLimbInitJnts[1] )
	
	otherSide = 'R'
	if side == 'R':
		otherSide = 'L'	
	
	
	#============================================================================
	# def for rigging the hand  
	def RigHand( butLimbJnt, endLimbJnt, father ):
		side = butLimbJnt.name()[0]
		handIKStuff = pm.ikHandle(  sj = butLimbJnt, ee = endLimbJnt, solver = "ikSCsolver"  )
		handIK = pm.rename ( handIKStuff[0] , ( side + "_hand_ikh") )
		pm.parent( handIK, father )
		father.scale >> butLimbJnt.scale		
		LockHideAttr( objs = handIKStuff, attr='vv' )

		
	#============================================================================
	# def for rigging single chain joints
	def RigSingleChain( startJnt, endJnt, father ):
		side = startJnt.name()[0]
		IKStuff = pm.ikHandle(  sj = startJnt, ee = endJnt, solver = "ikSCsolver"  )
		IK = pm.rename ( IKStuff[0] , ( side + "_sc_ikh") )
		pm.parent( IK, father )
		father.scale >> startJnt.scale		
		GNL.lockHideAttr.LockHideAttr( objs = IKStuff, attr='vv' )
				


	#============================================================================
	# getting info from selected objects
	if mode == 'arm':
		firstInitJnt 	= 	QuadrupedLimbInitJnts[0]
		secondInitJnt 	= 	QuadrupedLimbInitJnts[1]
		thirdInitJnt 	=	QuadrupedLimbInitJnts[2]
		forthInitJnt 	= 	QuadrupedLimbInitJnts[3]

		armPos 		= 	WorldPos( firstInitJnt )
		elbowPos  	= 	WorldPos( secondInitJnt )
		handPos  	= 	WorldPos( thirdInitJnt )
		handEndPos  = 	WorldPos( forthInitJnt )

	elif mode == 'leg':
		firstInitJnt 	= 	QuadrupedLimbInitJnts[0]
		secondInitJnt 	= 	QuadrupedLimbInitJnts[1]
		thirdInitJnt 	=	QuadrupedLimbInitJnts[2]
		heelInitJnt 	    = 	QuadrupedLimbInitJnts[3]
		forthInitJnt 	    = 	QuadrupedLimbInitJnts[4]
		toeEndInitJnt 	    = 	QuadrupedLimbInitJnts[5]
	
		upLegPos 		= 	WorldPos( firstInitJnt )
		kneePos      	= 	WorldPos( secondInitJnt )
		anklePos      	= 	WorldPos( thirdInitJnt )
		heelPos         = 	WorldPos( heelInitJnt )
		ballPos         = 	WorldPos( forthInitJnt )
		toeEndPos        = 	WorldPos( toeEndInitJnt )

	#============================================================================
	# create arm or leg joints
	if mode == 'arm':
		pm.select ( cl = True )
		upLimbJnt =pm.joint ( p = armPos  , name = ( side + "_upArm_jnt" ) )

		midLimbJnt = pm.joint ( p = elbowPos , name = ( side + "_elbow_jnt" ) )
		pm.joint( upLimbJnt, e=True, zso=True, oj='xyz', sao='yup')

		butLimbJnt = pm.joint ( p = handPos , name = ( side + "_hand_jnt" ) )
		pm.joint( midLimbJnt,  e=True, zso=True, oj='xyz', sao='yup')

		endLimbJnt = pm.joint ( p = handEndPos , name = ( side + "_hand_end_jnt" ) )
		pm.joint( butLimbJnt,  e=True, zso=True, oj='xyz', sao='yup')

		quadrupedLimbJnts = [ upLimbJnt, midLimbJnt, butLimbJnt, endLimbJnt ]

	elif mode == 'leg':
		pm.select ( cl = True )
		upLimbJnt =pm.joint ( p = upLegPos  , name = ( side + "_upLeg_jnt" ) )

		midLimbJnt = pm.joint ( p = kneePos , name = ( side + "_knee_jnt" ) )
		pm.joint( upLimbJnt, e=True, zso=True, oj='xzy', sao='xup')

		butLimbJnt = pm.joint ( p = anklePos , name = ( side + "_ankle_jnt" ) )
		pm.joint( midLimbJnt,  e=True, zso=True, oj='xzy', sao='xup')

		endLimbJnt = pm.joint ( p = ballPos , name = ( side + "_ball_jnt" ) )
		pm.joint( butLimbJnt,  e=True, zso=True, oj='xzy', sao='xup')
		
		toeEndJnt = pm.joint ( p = toeEndPos , name = ( side + "_toeEnd_jnt" ) )
		pm.joint( endLimbJnt,  e=True, zso=True, oj='xzy', sao='xup')
		
		quadrupedLimbJnts = [ upLimbJnt, midLimbJnt, butLimbJnt, endLimbJnt, toeEndJnt ]

	#============================================================================
	# orient joints and set preferred angle
	if midLimbJnt.jointOrientX.get() != 0: # arm is bent
		aimLoc = pm.spaceLocator()
		upArmHandMidPos = FindPosBetween( percent=50, base=upLimbJnt, tip=butLimbJnt )
		aimLoc.translate.set( upArmHandMidPos )
		pm.delete( pm.aimConstraint( midLimbJnt, aimLoc, worldUpType="object", aimVector=(1,0,0), upVector=(0,1,0), worldUpObject= butLimbJnt  ) )
		pm.move( aimLoc, ( limbLen*2.0, 0, 0 ), wd=True, os=True, relative=True )
		for jnt in ( upLimbJnt, midLimbJnt, butLimbJnt ):
			RIG.oriJnt.OriJnt( jnt=jnt, upAim=aimLoc , aimAxis='-z' )
		
		if mode == 'arm':
			midLimbJnt.preferredAngleY.set( -90 )
		elif mode == 'leg':
			midLimbJnt.preferredAngleZ.set( 90 )
	
	else:
		aimLoc = pm.spaceLocator()
		pm.parent( aimLoc, secondInitJnt )
		pm.makeIdentity( aimLoc, t=True, r=True, s=True )
		if mode == 'arm':
			midLimbJnt.preferredAngleY.set( -90 )
			aimLoc.translateZ.set( -limbLen*1.5 )
		elif mode == 'leg':
			aimLoc.translateY.set( -limbLen*1.5 )
			midLimbJnt.preferredAngleZ.set( 90 )
		pm.parent( aimLoc, w=True)
	
	aimLoc.rotate.set( 0,0,0 )
	
	#============================================================================
	# If mirror is ON
	if mirror == True:
		# mirror joints and pole vector loc
		OSjnts = pm.mirrorJoint( upLimbJnt, mirrorYZ=True , mirrorBehavior=True, searchReplace=( "L", "R" ) )
		OSjnts = pm.ls( OSjnts )
		OSupLimbJnt = OSjnts[0]
		OSmidLimbJnt = OSjnts[1]
		OSbutLimbJnt = OSjnts[2]
		OSendLimbJnt =  OSjnts[3]
		OSquadrupedLimbJnts = [ OSupLimbJnt, OSmidLimbJnt, OSbutLimbJnt, OSendLimbJnt ]
		
		
		
		OSaimLoc = pm.duplicate( aimLoc )[0]
		OSaimLoc.translateX.set( -OSaimLoc.translateX.get() )

	#============================================================================
	# create IK, FK joints
	
	
	# FK mode =============
	if FKIKMode == 'FK':
	
		RigFK( jnts = ( upLimbJnt, midLimbJnt, butLimbJnt ), side = side )
		pm.delete( aimLoc )
		
		# other side
		if mirror:
			RigFK( jnts = ( OSupLimbJnt, OSmidLimbJnt, OSbutLimbJnt ), side=otherSide )
			pm.delete( OSaimLoc )


	# IK mode =============
	elif FKIKMode == 'IK':
	
		armRigStuff = RigIK( jnts = ( upLimbJnt, midLimbJnt, butLimbJnt ), mode=mode,  aim = aimLoc , side = side  )
		RigHand( butLimbJnt, endLimbJnt, armRigStuff[0] )
		
		# other side
		if mirror:
			OSarmRigStuff = RigIK( jnts = ( OSupLimbJnt, OSmidLimbJnt, OSbutLimbJnt ), mode=mode,  aim = OSaimLoc , side=otherSide )
			RigHand( OSbutLimbJnt, OSendLimbJnt, OSarmRigStuff[0] )


	# FKIK mode =============
	elif FKIKMode == 'FKIK':
		FKIKstuff = RigFKIK( jnts = ( upLimbJnt, midLimbJnt, butLimbJnt ), mode=mode,  aim = aimLoc , side=side )
		RigHand( FKIKstuff[1][2], FKIKstuff[1][3], FKIKstuff[2][0] )

		
		# other side
		if mirror:
			OSFKIKstuff = RigFKIK( jnts = ( OSupLimbJnt, OSmidLimbJnt, OSbutLimbJnt ), mode=mode,  aim = OSaimLoc , side=otherSide )
			RigHand( OSFKIKstuff[1][2], OSFKIKstuff[1][3], OSFKIKstuff[2][0] )
			# reverse finger ctrl and elbow ctrl shapes
			# ReverseShape( OSFKIKstuff[3], 'x' )
			# ReverseShape( OSFKIKstuff[2][1], 'z' )
			# ReverseShape( OSFKIKstuff[2][1], 'x' )
	#============================================================================
	pm.delete( QuadrupedLimbInitJnts )
	
	RigBendyLimb( jnts=quadrupedLimbJnts[:3], bendyCtrl=FKIKstuff[3], numOfSegs= numOfSegs )
	if mirror:
		RigBendyLimb( jnts=OSquadrupedLimbJnts[:3], bendyCtrl=OSFKIKstuff[3], numOfSegs= numOfSegs, isMirroredJoint=True )

	
#========================================================================================================
# pack the arm rig
#========================================================================================================
def QuadrupedLimb( **kwargs ):

	QuadrupedLimb_init( **kwargs )
	QuadrupedLimb_pack( **kwargs ) 
