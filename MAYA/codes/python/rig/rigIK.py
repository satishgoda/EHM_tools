import pymel.core as pm

from codes.python.general.dist                   import     Dist
from codes.python.general     import     getAllChildren
GetAllChildren = getAllChildren.GetAllChildren 

from codes.python.general.reverseShape           import     ReverseShape
from codes.python.general.lockHideAttr           import     LockHideAttr
from codes.python.general.colorize               import     Colorize
from codes.python.curves.circle3ArrowCrv         import     Circle3ArrowCrv
from codes.python.curves.cubeCrv                 import     CubeCrv
from codes.python.curves.softSpiralCrv           import     SoftSpiralCrv
from codes.python.curves.sharpSpiralCrv          import     SharpSpiralCrv



from codes.python.rig.matchTransform             import     MatchTransform
from codes.python.rig.zeroGrp                    import     ZeroGrp
from codes.python.rig.transferOutConnections     import     TransferOutConnections
from codes.python.rig.guideCrv    				import     GuideCrv

from codes.python.rig             				import     makeIkStretchy
MakeIkStretchy = makeIkStretchy.MakeIkStretchy

from codes.python.rig                        import		findPVposition
FindPVposition = findPVposition.FindPVposition

from codes.python.rig                        import		projectedAim
ProjectedAim = projectedAim.ProjectedAim


from codes.python.general 					import		mirrorObjLikeJnt
MirrorObjLikeJnt = mirrorObjLikeJnt.MirrorObjLikeJnt

#============================================================================
# def for rigging the hand  
def RigHand( startJnt, endJnt, father ):
	side = startJnt.name()[0]
	handIKStuff = pm.ikHandle(  sj = startJnt, ee = endJnt, solver = "ikSCsolver"  )
	handIK = pm.rename ( handIKStuff[0] , ( side + "_sc_ikh") )
	pm.parent( handIK, father )
	father.scale >> startJnt.scale		
	LockHideAttr( objs = handIKStuff, attrs='vv' )


# auto pole vector
# this script takes two objects and create a single joint chain
# with a SC ik handle applied to it.
# you can use this to create auto pole vector for quadrupeds.

def autoPoleVector( baseJnt=None, endJnt=None, side='L' ):

	baseJntPos = pm.xform( baseJnt, q=True, t=True, ws=True )
	endJntPos = pm.xform( endJnt, q=True, t=True, ws=True )

	pm.select(clear=True)
	poleVectorJnt_one = pm.joint( p=baseJntPos )
	poleVectorJnt_two = pm.joint( p=endJntPos )
	poleVectorIKstuff = pm.ikHandle(  sj = poleVectorJnt_one, ee = poleVectorJnt_two, solver = "ikSCsolver"  )

	pv = pm.spaceLocator()
	pv.setParent( poleVectorJnt_two )
	pv.translate.set( 0,0,0 )
	pvZeros = ZeroGrp( pv )

	pm.pointConstraint( poleVectorIKstuff[0], pvZeros[0] )

	if side=='L':
		pv.translateX.set( 1 )
	elif side=='R':
		pv.translateX.set( -1 )


	pvZeros[0].setParent( poleVectorJnt_two )

	return ( pv, poleVectorIKstuff, (poleVectorJnt_one, poleVectorJnt_two) ) 






# RigIK function

def RigIK( jnts=None, side='L', ctrlSize=1.0, mode='arm', characterMode='biped',mirrorMode=False,poleVectorTransform=None,footRotate=None,rigHandOrFoot=False ):
	# find color of the ctrls
	color = 'y'
	if side == 'L':
		color = 'r'
	elif side == 'R':
		color = 'b'

	# biped mode
	# -----------------------------------------------------------
	if characterMode=='biped': 
	
		# biped inputs check 
		if not jnts:
			jnts = pm.ls(sl=True)
			if not len(jnts) == 4  :
				pm.error( 'ehm_tools...rigIK: (biped mode) select uparm, elbow, hand and hend end joints.' )

		# check mode - arm or leg
		if mode=='arm':
			limbName = 'hand'
			secondLimb = 'elbow'
		elif mode=='leg':
			limbName = 'foot'	
			secondLimb = 'knee'
		else:
			pm.error('ehm_tools...rigIK: mode argument must be either "arm" or "leg"!')

		# start rigging biped
		uparmJnt	=	jnts[0]
		elbowJnt	=	jnts[1]
		handJnt		=	jnts[2]
		handEndJnt	=	jnts[3]

		# find control size
		if mode=='arm':
			ctrlSize = Dist( uparmJnt, elbowJnt )* 0.4 * ctrlSize
		elif mode=='leg':
			ctrlSize = Dist( uparmJnt, elbowJnt )* 0.3 * ctrlSize
	


		# find arm limbs position
		uparmPos = pm.xform(uparmJnt,q=True,t=True,ws=True)
		elbowPos = pm.xform(elbowJnt,q=True,t=True,ws=True)
		handPos  = pm.xform(handJnt ,q=True,t=True,ws=True)



		# create ik handle
		armIKStuff  = pm.ikHandle(  sj = uparmJnt, ee = handJnt, solver = "ikRPsolver"  )
		armIK = pm.rename ( armIKStuff[0] ,   ( side + "_arm_ikh" ) )
		

		# make Ik Stretchy
		locs, dists = MakeIkStretchy( ikh=armIK , elbowLock=True )



		#========================================================================================================
		# create and position the IK elbow control curve
		
		if mode=='arm':
			elbowIKCtrl = SoftSpiralCrv ( ctrlSize , '%s_%s_IK_ctrl'%(side,secondLimb) )	
			# rotate elbowIKCtrl to be seen from side view
			elbowIKCtrl.rotateZ.set(90)
			elbowIKCtrl.scaleZ.set(-1)
			if mirrorMode:
				ReverseShape( objs=elbowIKCtrl, axis='y')
				ReverseShape( objs=elbowIKCtrl, axis='z')

		elif mode=='leg':
			elbowIKCtrl = SharpSpiralCrv ( ctrlSize , '%s_%s_IK_ctrl'%(side,secondLimb) )
			# rotate elbowIKCtrl to be seen from side view
			elbowIKCtrl.rotate.set(90,90,-90)		
			if mirrorMode:
				ReverseShape( objs=elbowIKCtrl, axis='y')
				ReverseShape( objs=elbowIKCtrl, axis='z')		

		pm.makeIdentity( elbowIKCtrl, apply=True )

		
		# give it color
		Colorize( shapes=elbowIKCtrl.getShape(), color=color )


		tmpAim = pm.group( em=True )
		if poleVectorTransform: # pole vector position is given
			elbowIKCtrl.translate.set( poleVectorTransform[0] )
			elbowIKCtrl.rotate.set( poleVectorTransform[1] )

		
		else: # pole vector position is NOT given, we'll guess it
			aimPos = FindPVposition( objs = (uparmJnt,elbowJnt,handJnt) )
					
			if aimPos: # if pole vector position was found by FindPVposition def, we're done :)
				pm.xform( elbowIKCtrl, ws=True, t = aimPos )
				
			else: # limb is straight
				pm.delete( pm.pointConstraint( elbowJnt , elbowIKCtrl ) ) # position the elbowIKCtrl

			if mode=='arm': # find elbow pole vector position and rotation
				tmpAim.translate.set( elbowPos[0], elbowPos[1], elbowPos[2]-ctrlSize ) # position it slightly behind elbow joint
				pm.delete( pm.aimConstraint( 
										tmpAim
										, elbowIKCtrl 
										, upVector = (0,1,0)
										, aimVector = (0,0,-1)
										) ) # rotate elbowIKCtrl to point to tmpAim 

			if mode=='leg': # find knee pole vector position
				tmpAim.translate.set( elbowPos[0], elbowPos[1], elbowPos[2]+ctrlSize ) # position it slightly behind elbow joint
				pm.delete( pm.aimConstraint( 
										tmpAim
										, elbowIKCtrl 
										, upVector = (0,1,0)
										, aimVector = (0,0,1)
										) ) 


		# elbow IK control is in place now, parent elbow loc to it and offset it from arm a bit
		elbowIKCtrlZeros = ZeroGrp(elbowIKCtrl)
		pm.parent( locs[1], elbowIKCtrl )
		locs[1].translate.set(0,0,0)
		locs[1].rotate.set(0,0,0)		

		'''
		if mode=='arm':			
			elbowIKCtrl.translateZ.set( -ctrlSize*2.0 )
		if mode=='leg':
			elbowIKCtrl.translateZ.set( ctrlSize*2.0 )
		'''


		# use elbow control curve instead of locator as the pole vector
		TransferOutConnections( source=locs[1], dest=elbowIKCtrl )

		LockHideAttr( objs=elbowIKCtrl, attrs='r') 
		LockHideAttr( objs=elbowIKCtrl, attrs='s')

		# create pole vector
		pm.poleVectorConstraint( locs[1], armIK )


		
		#========================================================================================================
		# rig hand or foot and position them in the correct place
		
		if mode=='arm': # position the hand control
			handIKCtrl = Circle3ArrowCrv ( ctrlSize , '%s_%s_IK_ctrl'%(side,limbName) )
			MatchTransform( force=True, folower=handIKCtrl, lead=handJnt )
			if rigHandOrFoot:
				RigHand( handJnt, handEndJnt, handIKCtrl )
				locs[2].setParent( handIKCtrl )

			
		elif mode=='leg': # position the foot control
			handIKCtrl = CubeCrv ( ctrlSize , '%s_%s_IK_ctrl'%(side,limbName) )	
			handIKCtrl.translate.set( pm.xform(handJnt, q=True, ws=True, t=True) )
			handIKCtrl.rotate.set( footRotate )
			
			
			if rigHandOrFoot: # rig foot
			
				ankleJnt = jnts[2]
				ballJnt = jnts[3]
				toeEndJnt = jnts[4]
				ballPos = pm.xform( jnts[3], q=True, t=True, ws=True )
				toeEndPos = pm.xform( jnts[4], q=True, t=True, ws=True )
				heelPos = pm.xform( jnts[5], q=True, t=True, ws=True )
				outsidePos = pm.xform( jnts[6], q=True, t=True, ws=True )
				insidePos = pm.xform( jnts[7], q=True, t=True, ws=True )	
				
				# create foot ik handles
				ankleBallIKStuff  = pm.ikHandle(  sj = ankleJnt, ee = ballJnt, solver = "ikSCsolver"  )
				ankleBallIK = pm.rename ( ankleBallIKStuff[0] ,   ( side + "_ankleBall_ikh" ) )
				ballToeEndIKStuff  = pm.ikHandle(  sj = ballJnt, ee = toeEndJnt, solver = "ikSCsolver"  )
				ballToeIK = pm.rename ( ballToeEndIKStuff[0] ,   ( side + "_ballToeEnd_ikh" ) )
				
				# add attributes to foot controler
				pm.addAttr(handIKCtrl, ln="roll", at='double', min=-10, max=10, dv=0, keyable=True )
				pm.addAttr(handIKCtrl, ln="sideToSide", at='double', min=-10, max=10, dv=0, keyable=True )
				pm.addAttr(handIKCtrl, ln="toes", at='double', min=-10, max=10, dv=0, keyable=True )


				# toe group
				toeGrp = pm.group( ballToeIK, name='%s_toe_IK_grp'%side )
				pm.xform( toeGrp, os=True, piv=( ballPos ) )

				# heelUp group
				heelUpGrp = pm.group( ankleBallIK,  locs[2], name='%s_heelUp_IK_grp'%side  )
				pm.xform( heelUpGrp, os=True, piv=( ballPos ) )

				
				# pivOnToe group
				outsideGrp = pm.group( toeGrp,  heelUpGrp, name='%s_outside_IK_grp'%side  )
				pm.xform( outsideGrp, os=True, piv=( outsidePos ) )

				# pivOnHeel group
				insideGrp = pm.group( outsideGrp, name='%s_inside_IK_grp'%side  )
				pm.xform( insideGrp, os=True, piv=( insidePos ) )

				# pivOutSide group
				toeTipGrp = pm.group( insideGrp, name='%s_toeTip_IK_grp'%side  )
				pm.xform( toeTipGrp, os=True, piv=( toeEndPos ) )

				# pivInSide group
				heelGrp = pm.group( toeTipGrp, name='%s_heel_IK_grp'%side  )
				pm.xform( heelGrp, os=True, piv=( heelPos ) )
				footGrp = pm.group( heelGrp, name='%s_foot_IK_grp'%side)
				footGrp.setParent( handIKCtrl )
				
				# toe set driven keys
				pm.setDrivenKeyframe( toeGrp.rotateX, currentDriver=handIKCtrl.toes, itt='linear', ott='linear', driverValue=10 ,value=-90  )
				pm.setDrivenKeyframe( toeGrp.rotateX, currentDriver=handIKCtrl.toes, itt='linear', ott='linear', driverValue=-10 ,value=90  )

				# roll set driven keys
				pm.setDrivenKeyframe( heelUpGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=0 ,value=0  )
				pm.setDrivenKeyframe( heelUpGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=-5 ,value=45  )
				pm.setDrivenKeyframe( heelUpGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=10 ,value=0  )

				pm.setDrivenKeyframe( toeTipGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=-5 ,value=0  )
				pm.setDrivenKeyframe( toeTipGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=-10 ,value=60  )

				pm.setDrivenKeyframe( heelGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=10 ,value=-45  )
				pm.setDrivenKeyframe( heelGrp.rotateX, currentDriver=handIKCtrl.roll, itt='linear', ott='linear', driverValue=0 ,value=0  )

				# sideToSide set driven keys
				value = 45
				if mirrorMode:
					value = -45
				pm.setDrivenKeyframe( outsideGrp.rotateZ, currentDriver=handIKCtrl.sideToSide, itt='linear', ott='linear', driverValue=0 ,value=0  )
				pm.setDrivenKeyframe( outsideGrp.rotateZ, currentDriver=handIKCtrl.sideToSide, itt='linear', ott='linear', driverValue=10 ,value=-value  )

				pm.setDrivenKeyframe( insideGrp.rotateZ, currentDriver=handIKCtrl.sideToSide, itt='linear', ott='linear', driverValue=0 ,value=0  )
				pm.setDrivenKeyframe( insideGrp.rotateZ, currentDriver=handIKCtrl.sideToSide, itt='linear', ott='linear', driverValue=-10 ,value=value  )
								
				# delete joint that determine foot's different pivots
				pm.delete( jnts[-3:] )
				
				# hide extras
				LockHideAttr( objs=(ankleBallIKStuff,ballToeEndIKStuff) , attrs='vv' )

		
		handIKCtrlZeros = ZeroGrp( handIKCtrl)
		handIKCtrlZero = handIKCtrlZeros[0]
		TransferOutConnections( source = locs[2], dest= handIKCtrl )

		# colorize hand control
		Colorize( shapes=handIKCtrl.getShape(), color=color )

		# check if joints are mirrored, if so, we must reverse the hand control vertices
		if mirrorMode:
			ReverseShape( axis = 'x', objs = handIKCtrl )

	
		# hide extra stuff
		LockHideAttr( objs=locs, attrs='vv' )
		LockHideAttr( objs=dists, attrs='vv' )

		ikGrp = pm.group(  jnts[0], dists, locs[0], name= '%s_ik_arm'%side )
		pm.xform( ikGrp,  os=True, piv=(0,0,0) )

		#  create guide curves for pole vector
		elbowGuide = GuideCrv( elbowIKCtrl,elbowJnt )
		elbowIKCtrl.v >> elbowGuide.getShape().v
		elbowGuide.setParent( ikGrp )
		
		
		# clean up
		pm.delete( tmpAim )
		
		# return
		return ( handIKCtrl, elbowIKCtrl, jnts, locs, dists, handIKCtrlZeros, elbowIKCtrlZeros, ikGrp )


	# quadruped mode
	# -----------------------------------------------------------			
	if characterMode=='quadruped':
		
		# quadruped inputs check
		if not jnts:
			jnts = pm.ls(sl=True)
			if not len(jnts) == 7  :
				pm.error( 'ehm_tools...rigIK: (quadruped mode) jnts arguments needs 7 joints.' )	

		# check mode - arm or leg	
		if mode=='arm':
			pm.error('ehm_tools...rigIK: quadruped arm is not defined yet!')
		elif mode=='leg':
			firstLimbName	= 'pelvis'	
			secondLimbName	= 'hip'	
			thirdLimbName	= 'stifle'	
			forthLimbName	= 'hock'
			fifthLimbName	= 'ankle'
			sixthLimbName	= 'hoof'
			seventhLimbName	= 'hoofEnd'
		else:
			pm.error('ehm_tools...rigIK: mode argument must be either "arm" or "leg"!')


		# start rigging the quadruped
		pelvisJnt	=	jnts[0]
		hipJnt		=	jnts[1]
		stifleJnt	=	jnts[2]		
		hockJnt		=	jnts[3]		
		ankleJnt	=	jnts[4]		
		hoofJnt		=	jnts[5]		
		hoofEndJnt	=	jnts[6]		

		# find arm limbs position
		pelvisPos 	= pm.xform( pelvisJnt	,q=True,t=True,ws=True )
		hipPos 		= pm.xform( hipJnt		,q=True,t=True,ws=True )
		stiflePos  	= pm.xform( stifleJnt 	,q=True,t=True,ws=True )
		hockPos  	= pm.xform( hockJnt 	,q=True,t=True,ws=True )
		anklePos  	= pm.xform( ankleJnt 	,q=True,t=True,ws=True )
		hoofPos  	= pm.xform( hoofJnt 	,q=True,t=True,ws=True )
		hoofEndPos  = pm.xform( hoofEndJnt 	,q=True,t=True,ws=True )


		# find control size
		ctrlSize = Dist( hipJnt, hockJnt )* 0.2 * ctrlSize
		
		# set preferred angle
		if mode=='arm' :
			pm.error('ehm_tools...rigIK: quadruped arm is not defined yet!')
		else:
			stifleJnt.preferredAngleZ.set( 10 )
			hockJnt.preferredAngleZ.set( -10 )

		
		# create ik handle for main joint chain
		IKstuff = pm.ikHandle(  sj = hipJnt, ee = hockJnt, solver = "ikRPsolver"  )
		ankleIKstuff = pm.ikHandle(  sj = hockJnt, ee = ankleJnt, solver = "ikSCsolver"  )


		# create 3 extra joint chains for making some auto movements on the leg:

		# chain 1. upper leg, lower leg, foot
		#    - this chain is used for automatic upper leg bending when foot control is moved
		pm.select(clear=True)
		autoUpLegJnt_tmp = pm.duplicate( hipJnt )[0]
		autoJnts_tmp =  GetAllChildren( objs=autoUpLegJnt_tmp, childType='joint')

		autoUpLegJnt   =  pm.rename( autoJnts_tmp[0], '%s_autoUpLegJnt'%side )
		autoLowLegJnt  =  pm.rename( autoJnts_tmp[1], '%s_autoLowLegJnt'%side )
		autoKneeJnt    =  pm.rename( autoJnts_tmp[2], '%s_autoKneeJnt'%side )
		autoKneeEndJnt =  pm.rename( autoJnts_tmp[3], '%s_autoKneeEndJnt'%side )
		
		autoIKstuff = pm.ikHandle(  sj = autoUpLegJnt, ee = autoKneeEndJnt, solver = "ikRPsolver"  )




		# chain 2 and 3:
		#    - these chains are needed for automatic pole vector

		PV = autoPoleVector( baseJnt=hipJnt, endJnt=hockJnt, side=side )
		autoPV = autoPoleVector( baseJnt=autoUpLegJnt, endJnt=autoKneeEndJnt, side='L' )



		# create automatic pole vector and set the twist parameter
		pm.poleVectorConstraint( PV[0], IKstuff[0] )
		pm.poleVectorConstraint( autoPV[0], autoIKstuff[0] )



		if side=='L':
			IKstuff[0].twist.set( 90 )
			autoIKstuff[0].twist.set( 90 )
		elif side=='R':
			IKstuff[0].twist.set( -90 )
			autoIKstuff[0].twist.set( -90 )



		# parent all ikhandles to auto kneeEnd joint.
		# now we're controling 3 joint chain ik handle with one joint
		# which itself is being controled by foot control.
		IKstuffGrp = pm.group( ankleIKstuff[0], IKstuff[0], PV[1][0] )
		pm.xform( os=True, piv=( pm.xform(ankleJnt,q=True,t=True,ws=True) ) )
		IKstuffGrp.setParent( autoKneeEndJnt )		

		autoIKstuffZeros = ZeroGrp( autoIKstuff[0] )
		autoPV[1][0].setParent( autoIKstuffZeros[1] )



		# make Ik Stretchy
		locs, dists = MakeIkStretchy( ikh=autoIKstuff[0] , elbowLock=False )



		# Finally, parent main upLeg joint to autoUpLegJnt. The purpose of whole auto joint chain
		pm.parent( locs[0], autoUpLegJnt )
		ZeroGrp()

		pm.parentConstraint( autoUpLegJnt, hipJnt, mo=True )



		# create IK hand control
		if mode=='arm':
			pm.error('ehm_tools...rigIK: quadruped arm is not defined yet!')
		else:
			IKCtrl = CubeCrv ( size=ctrlSize , name= '%s_%s_IK_ctrl'%(side,ankleJnt) )	
	

		# position the hand control
		pm.addAttr( IKCtrl, ln="upLeg_rotation", at='double', keyable=True )



		# find color of the ctrls
		color = 'y'
		if side == 'L':
			color = 'r'
		elif side == 'R':
			color = 'b'

		Colorize( shapes=IKCtrl.getShape(), color=color )


		# position the hand control
		if mode=='arm':
			pm.error('ehm_tools...rigIK: quadruped arm is not defined yet!')
		else:
			pm.delete( pm.pointConstraint( ankleJnt , IKCtrl ) )
			IKCtrl.rotateY.set( ProjectedAim( objs=(hipJnt,stifleJnt), fullCircle=False ))


		IKCtrlZeros = ZeroGrp( IKCtrl )

		#IKCtrlZero = IKCtrlZeros[0]
		pm.pointConstraint( IKCtrl, PV[1][0] )
		pm.parent ( autoIKstuff[0], locs[2]  , IKCtrl )
		TransferOutConnections( source = locs[2], dest= IKCtrl )

		
		# check if joints are mirrored, if so, we must reverse the hand control vertices
		#x = kneeEndJnt.translateX.get()
		#y = kneeEndJnt.translateY.get()
		#z = kneeEndJnt.translateZ.get()
		#if x < 0:
		#	ReverseShape( axis = 'x', objs = IKCtrl )
		#elif y < 0:
		#	ReverseShape( axis = 'y', objs = IKCtrl )
		#elif z < 0:
		#	ReverseShape( axis = 'z', objs = IKCtrl )

	
		# hide extra stuff
		LockHideAttr( objs=locs, attrs='vv' )
		LockHideAttr( objs=dists, attrs='vv' )
		LockHideAttr( objs=PV[0], attrs='vv' )
		LockHideAttr( objs=PV[1], attrs='vv' )
		LockHideAttr( objs=autoIKstuff, attrs='vv' )
		LockHideAttr( objs=autoUpLegJnt, attrs='vv' )
		LockHideAttr( objs=PV[2][0], attrs='vv' )

		# cleaup outliner
		ikGrp = pm.group( hipJnt, autoUpLegJnt, PV[2][0], dists, locs[1],PV[1][0], IKCtrlZeros[0], name= '%s_ik_leg'%side )
		pm.xform( ikGrp,  os=True, piv=(0,0,0) )


		# return
		# return ( IKCtrl, jnts, locs, dists, IKCtrlZeros, ikGrp )


		