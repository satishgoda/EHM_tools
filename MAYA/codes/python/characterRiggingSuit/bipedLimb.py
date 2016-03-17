'''
# what does this script do ?		 rigs the arm

'''
#============================================================================

import pymel.core as pm
import pymel.core.datatypes as dt

from codes.python.rig import jntToCube
JntToCube 			=	jntToCube.JntToCube

from codes.python.rig import findPosBetween
FindPosBetween		=	findPosBetween.FindPosBetween

from codes.python.rig import findPVposition
reload( findPVposition )
FindPVposition		=	findPVposition.FindPVposition

from codes.python.general import mirrorObjLikeJnt
reload( mirrorObjLikeJnt )
MirrorObjLikeJnt = mirrorObjLikeJnt.MirrorObjLikeJnt

from codes.python.rig import rigFK
RigFK 				=	rigFK.RigFK

from codes.python.rig import rigIK
reload( rigIK )
RigIK 				=	rigIK.RigIK

from codes.python.rig import rigFKIK
reload( rigFKIK )
RigFKIK 			=	rigFKIK.RigFKIK

from codes.python.rig import rigBendyLimb
reload( rigBendyLimb )
RigBendyLimb		=	rigBendyLimb.RigBendyLimb

from codes.python.rig import oriJnt
reload( oriJnt )
OriJnt		=	oriJnt.OriJnt

from codes.python.general import lockHideAttr
LockHideAttr 		=	lockHideAttr.LockHideAttr

from codes.python.general import dist
Dist		=	dist.Dist

from codes.python.rig.projectedAim    			import     ProjectedAim

from functools import partial

class BipedLimb():
	
	def __init__(self, *args, **kwargs):
		self.UI()
	
	def UI(self):
		width = 570
		height = 280
		# create window
		if pm.window( 'ehm_BipedLimb_UI', exists=True ):
			pm.deleteUI( 'ehm_BipedLimb_UI' )
		pm.window( 'ehm_BipedLimb_UI', title='Rig Biped Limbs', w=width, h=height, mxb=False, mnb=False, sizeable=True )
		
		# main layout
		baseForm = pm.formLayout()
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'left', 6) )
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'right', 6) )
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'top', 6) )
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'bottom', 38) )
		# pm.scrollLayout( horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
		formLayout = pm.formLayout(w=width, h=height)
		
		
		# spine size
		self.BipedLimbSizeT = pm.text( label="Limb Size: ")	
		self.BipedLimbSizeF = pm.floatSliderGrp(adjustableColumn=4,min=0, max=20, fieldMaxValue=10000, value=5, field=True )

		
		# character mode radio buttons
		self.limbModeText = pm.text(label='Limb Mode: ', align='right')
		self.limbModeRC = pm.radioCollection()
		self.armRB = pm.radioButton(label="Arm", select=True )
		self.legRB = pm.radioButton(label="Leg")

		
		# number of joints
		self.numOfJntsText = pm.text( label='Number of joints: ', align='right')		
		self.numOfJntsIS = pm.intSliderGrp( field=True, value=6, maxValue=20, fieldMaxValue=1000 )		
		
		
		# extras check boxes
		self.extrasText = pm.text( label='Extras: ', align='right' )		
		self.bendyCB = pm.checkBox( label="Bendy", value=True )
		
		
		# buttons
		self.initButton = pm.button( label='Place joints',  h=30,  c=partial( self.bipedLimb_init, 10, 'arm', 'L' ), parent=baseForm  )
		self.packButton = pm.button( label='Finish Rig', h=30,  c=partial( self.bipedLimb_pack, 1.0, 'FKIK', True, 6, True, 'arm' ), parent=baseForm    )		
		self.closeButton = pm.button( label='Close', h=30,  c= self.closeUI , parent=baseForm    )		

		
		# place spine size
		pm.formLayout( formLayout, edit=True, attachPosition=(self.BipedLimbSizeT,'right', 0, 28 ) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.BipedLimbSizeT,'top', 17 ) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.BipedLimbSizeF,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.BipedLimbSizeF,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.BipedLimbSizeF,'top', 15 ) )	
		
		# place character mode
		pm.formLayout( formLayout, edit=True, attachPosition=(self.limbModeText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.limbModeText,'top', 17, self.BipedLimbSizeT) )
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.armRB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.armRB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.armRB,'top', 15, self.BipedLimbSizeT) )		

		pm.formLayout( formLayout, edit=True, attachPosition=(self.legRB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.legRB,'right', 15, 100 ) )
		
		pm.formLayout( formLayout, edit=True, attachControl=(self.legRB,'top', 35, self.BipedLimbSizeT) )	
		
		
		# place number of joints
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfJntsText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfJntsText,'top', 17, self.legRB) )
	
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfJntsIS,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfJntsIS,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfJntsIS,'top', 12, self.legRB ) )	

				
		
		# place check boxes
		pm.formLayout( formLayout, edit=True, attachPosition=(self.extrasText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.extrasText,'top', 17, self.numOfJntsIS) )
	
		pm.formLayout( formLayout, edit=True, attachPosition=(self.bendyCB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.bendyCB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.bendyCB,'top', 15, self.numOfJntsIS ) )	
		

		# place buttons		
		pm.formLayout( baseForm, edit=True, attachPosition=(self.initButton,'left', 3, 0) )
		pm.formLayout( baseForm, edit=True, attachPosition=(self.initButton,'right', 1, 33) )
		pm.formLayout( baseForm, edit=True, attachForm=(self.initButton,'bottom', 3) )	

		pm.formLayout( baseForm, edit=True, attachPosition=(self.packButton,'left', 1, 33) )
		pm.formLayout( baseForm, edit=True, attachPosition=(self.packButton,'right', 3, 66) )
		pm.formLayout( baseForm, edit=True, attachForm=(self.packButton,'bottom', 3) )	

		pm.formLayout( baseForm, edit=True, attachPosition=(self.closeButton,'left', 1, 66) )
		pm.formLayout( baseForm, edit=True, attachPosition=(self.closeButton,'right', 3, 100) )
		pm.formLayout( baseForm, edit=True, attachForm=(self.closeButton,'bottom', 3) )	

		# show window
		pm.showWindow( 'ehm_BipedLimb_UI' )

	
	def closeUI( self, *args ):
		pm.deleteUI( 'ehm_BipedLimb_UI' )								


		
	def worldPos( self, obj, *args ):
		try:
			return pm.xform( obj,q=True,t=True,ws=True )
		except:
			raise Exception( 'ehm_tools...bipedLimb.worldPos: could not query world position of object %s'%obj )



	def PVbyToeJnt( self, upJnt, midJnt, toeJnt, *args ):
		# guesses best pole vector position using upleg, knee and toe joints
		A = dt.Vector( pm.xform(upJnt, q=True, t=True, ws=True) ) # upleg joint
		B = dt.Vector( pm.xform(midJnt, q=True, t=True, ws=True) ) # knee joint
		C = dt.Vector( pm.xform(toeJnt, q=True, t=True, ws=True) ) # toe end joint
		return ( (A - B).normal() * (A - C).length() / 2 ) + C

		

	#========================================================================================================
	# make initial joints for starting the rig
	#========================================================================================================

	def bipedLimb_init( self, BipedLimbSize=10, mode='arm', side='L', *args  ):

		self.BipedLimbInitJnts = []
		
		try:# if in UI mode, get number of joints from UI
			BipedLimbSize = pm.floatSliderGrp( self.BipedLimbSizeF, q=True, value=True)
			selectedMode = pm.radioCollection( self.limbModeRC, q=True, select=True)
			mode = pm.radioButton( selectedMode, q=True, label=True ).lower()
		
		except:
			pass
		
		if mode == 'arm':
			pm.select( clear = True )
			self.BipedLimbInitJnts.append( pm.joint ( p = ( BipedLimbSize * 3 / 14.0     , BipedLimbSize*13 / 14.0 , 0) , name = "%s_uparm_initJnt"%side ) )
			
			self.BipedLimbInitJnts.append( pm.joint ( p = ( BipedLimbSize * 7 / 14.0      , BipedLimbSize*13 / 14.0 , 0) , name = "%s_elbow_initJnt"%side ) )
			pm.joint( self.BipedLimbInitJnts[0], e=True, zso=True, oj='xyz', sao='yup')
			
			self.BipedLimbInitJnts.append( pm.joint ( p = ( BipedLimbSize * 11 / 14.0     , BipedLimbSize*13 / 14.0 , 0) , name = "%s_hand_initJnt"%side ) )
			pm.joint( self.BipedLimbInitJnts[1], e=True, zso=True, oj='xyz', sao='yup')
			
			self.BipedLimbInitJnts.append( pm.joint ( p = ( BipedLimbSize * 12 / 14.0     , BipedLimbSize*13 / 14.0 , 0) , name = "%s_handEnd_initJnt"%side ) )
			pm.joint( self.BipedLimbInitJnts[2], e=True, zso=True, oj='xyz', sao='yup')
			
			pm.select ( clear=True )


		elif mode == 'leg':
			pm.select( clear = True )

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*2/7.0, BipedLimbSize*7/7.0, 0), name = "L_initUplegJnt") )

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*2/7.0, BipedLimbSize*4/7.0, 0), name = "L_initKneeJnt") )
			pm.joint( self.BipedLimbInitJnts[0], e=True, zso=True, oj='xzy', sao='xup' )

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*2/7.0, BipedLimbSize*1/7.0, 0), name = "L_initAnkleJnt") )
			pm.joint( self.BipedLimbInitJnts[1], e=True, zso=True, oj='xzy', sao='xup')

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*2/7.0,0,BipedLimbSize*-1/7.0), name = "L_initHeelJnt") )
			pm.joint( self.BipedLimbInitJnts[2], e=True, zso=True, oj='xzy', sao='xup')

			pm.pickWalk( d='up' )

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize* 2/7.0, BipedLimbSize*0.5/7.0, BipedLimbSize*1/7.0), name = "L_initBallJnt") )
			pm.joint( self.BipedLimbInitJnts[3], e=True, zso=True, oj='xzy', sao='xup')

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*2/7.0,0,BipedLimbSize*2/7.0), name = "L_initToeEndJnt") )
			pm.joint( self.BipedLimbInitJnts[4], e=True, zso=True, oj='xzy', sao='xup')

			pm.pickWalk( d='up' )

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*2.5/7.0,0,BipedLimbSize*1/7.0), name = "L_initOutFootJnt") )
			pm.joint( self.BipedLimbInitJnts[4], e=True, zso=True, oj='xzy', sao='xup')

			pm.pickWalk( d='up' )

			self.BipedLimbInitJnts.append( pm.joint(p=(BipedLimbSize*1.5/7.0,0,BipedLimbSize*1/7.0), name = "L_initInFootJnt") )
			pm.joint( self.BipedLimbInitJnts[4], e=True, zso=True, oj='xzy', sao='xup')

			pm.select ( clear=True )


			
	#========================================================================================================
	# pack the arm rig
	#========================================================================================================

	def bipedLimb_pack( self, ctrlSize=1.0, FKIKMode='FKIK', mirror=True, numOfSegs=6, bendy=True, mode='arm', *args ):

		try:# if in UI mode, get number of joints from UI
			ctrlSize = pm.floatSliderGrp( self.spineSizeF, q=True, value=True)
			selectedMode = pm.radioCollection( self.characterModeRC, q=True, select=True)
			mode = pm.radioButton( selectedMode, q=True, label=True ).lower()
			numOfSegs = pm.intSliderGrp( self.numOfJntsIS, q=True, value=True)
			bendy = pm.checkBox( self.bendyCB, q=True, value=True )		
		except:
			pass
		
		bipedLimbJnts = []
		FKIKstuff = []
		OSbipedLimbJnts = []	
		OSFKIKstuff = []	
		
		#============================================================================
		# find some info for naming and control sizes

		side = self.BipedLimbInitJnts[0].name()[0]
		limbLen = Dist( self.BipedLimbInitJnts[0] , self.BipedLimbInitJnts[1] )
		
		otherSide = 'R'
		if side == 'R':
			otherSide = 'L'	
		
		
		#============================================================================
		# getting info from selected objects
		if mode == 'arm':
			firstInitJnt 	= 	self.BipedLimbInitJnts[0]
			secondInitJnt 	= 	self.BipedLimbInitJnts[1]
			thirdInitJnt 	=	self.BipedLimbInitJnts[2]
			forthInitJnt 	= 	self.BipedLimbInitJnts[3]

			armPos 		= 	self.worldPos( firstInitJnt )
			elbowPos  	= 	self.worldPos( secondInitJnt )
			handPos  	= 	self.worldPos( thirdInitJnt )
			handEndPos  = 	self.worldPos( forthInitJnt )

		elif mode == 'leg':
			firstInitJnt 		= 	self.BipedLimbInitJnts[0]
			secondInitJnt 		= 	self.BipedLimbInitJnts[1]
			thirdInitJnt 		=	self.BipedLimbInitJnts[2]
			heelInitJnt 	    = 	self.BipedLimbInitJnts[3]
			forthInitJnt 	    = 	self.BipedLimbInitJnts[4]
			toeEndInitJnt 	    = 	self.BipedLimbInitJnts[5]
			outsideInitJnt 	    = 	self.BipedLimbInitJnts[6]
			insideInitJnt 	    = 	self.BipedLimbInitJnts[7]
			
			upLegPos 			= 	self.worldPos( firstInitJnt )
			kneePos      		= 	self.worldPos( secondInitJnt )
			anklePos      		= 	self.worldPos( thirdInitJnt )
			ballPos         	= 	self.worldPos( forthInitJnt )
			toeEndPos      	 	= 	self.worldPos( toeEndInitJnt )
			heelPos        	 	= 	self.worldPos( heelInitJnt )
			outsidePos      	= 	self.worldPos( outsideInitJnt )
			insidePos       	= 	self.worldPos( insideInitJnt )

			


		#============================================================================
		# create arm or leg joints
		if mode == 'arm':
			pm.select ( cl = True )
			upLimbJnt =pm.joint ( p = armPos  , name = ( side + "_upArm_jnt" ) )

			midLimbJnt = pm.joint ( p = elbowPos , name = ( side + "_elbow_jnt" ) )
			pm.joint( upLimbJnt, e=True, zso=True, oj='xyz', sao='yup')

			butLimbJnt = pm.joint ( p = handPos , name = ( side + "_hand_jnt" ) )
			pm.joint( midLimbJnt,  e=True, zso=True, oj='xyz', sao='yup')

			handEndJnt = pm.joint ( p = handEndPos , name = ( side + "_hand_end_jnt" ) )
			pm.joint( butLimbJnt,  e=True, zso=True, oj='xyz', sao='yup')

			bipedLimbJnts = [ upLimbJnt, midLimbJnt, butLimbJnt, handEndJnt ]

		elif mode == 'leg':
			pm.select ( cl = True )
			upLimbJnt =pm.joint ( p = upLegPos  , name = ( side + "_upLeg_jnt" ) )

			midLimbJnt = pm.joint ( p = kneePos , name = ( side + "_knee_jnt" ) )
			pm.joint( upLimbJnt, e=True, zso=True, oj='xzy', sao='xup')

			butLimbJnt = pm.joint ( p = anklePos , name = ( side + "_ankle_jnt" ) )
			pm.joint( midLimbJnt,  e=True, zso=True, oj='xzy', sao='xup')

			ballJnt = pm.joint ( p = ballPos , name = ( side + "_ball_jnt" ) )
			pm.joint( butLimbJnt,  e=True, zso=True, oj='xzy', sao='xup')
			
			toeEndJnt = pm.joint ( p = toeEndPos , name = ( side + "_toeEnd_jnt" ) )
			pm.joint( ballJnt,  e=True, zso=True, oj='xzy', sao='xup')
			
			pm.select(clear=True)
			heelJnt = pm.joint ( p = heelPos , name = ( side + "_heel_jnt" ) )

			pm.select(clear=True)
			outsideJnt = pm.joint ( p = outsidePos , name = ( side + "_outside_jnt" ) )

			pm.select(clear=True)
			insideJnt = pm.joint ( p = insidePos , name = ( side + "_inside_jnt" ) )
			
			bipedLimbJnts = [ upLimbJnt, midLimbJnt, butLimbJnt, ballJnt, toeEndJnt, heelJnt,outsideJnt,insideJnt ]


				
		#============================================================================
		# find the pole vector position
		# orient joints and set preferred angle
		
		# find pole vector position
		PVposition = FindPVposition( objs= (upLimbJnt, midLimbJnt, butLimbJnt) )

		if mode == 'arm': # arm mode .................................................
			
			if PVposition: # arm is bent!
				# create and position aim locator
				aimLoc = pm.spaceLocator()
				PVposition = FindPVposition( objs= (upLimbJnt, midLimbJnt, butLimbJnt) )
				aimLoc.translate.set( PVposition )
			
			else: # arm is not bent!
				# create and position aim locator
				aimLoc = pm.spaceLocator()
				pm.parent( aimLoc, midLimbJnt )
				pm.makeIdentity( aimLoc, t=True, r=True, s=True )
				aimLoc.translateZ.set( -limbLen*1.5 )
				pm.parent( aimLoc, w=True)
				aimLoc.rotate.set( 0,0,0 )

			# rotate the aim to match the rotation of the arm
			pm.delete( pm.aimConstraint( midLimbJnt, aimLoc, worldUpType="object", aimVector=(1,0,0), upVector=(0,1,0), worldUpObject= butLimbJnt  ) )

			# orient joints according to aim locator
			for jnt in ( upLimbJnt, midLimbJnt, butLimbJnt ):
				OriJnt( jnt=jnt, upAim=aimLoc , aimAxis='-z' )
				
			# set preferred angle
			midLimbJnt.preferredAngleY.set( -90 )
			
			poleVectorTransform = None
			footRotate = None
			

			

		elif mode == 'leg': # leg mode .................................................
			
			if PVposition: # leg is bent!
				# create and position aim locator
				aimLoc = pm.spaceLocator()
				PVposition = FindPVposition( objs= (upLimbJnt, midLimbJnt, butLimbJnt) )
				aimLoc.translate.set( PVposition )
				
			else: # leg is not bent!
				PVposition = self.PVbyToeJnt( upLimbJnt, midLimbJnt, toeEndJnt )
				# create and position aim locator
				aimLoc = pm.spaceLocator()
				aimLoc.translate.set( PVposition ) # position aim in front of the foot
				
			# rotate the aim to match the rotation of the arm
			pm.delete( pm.aimConstraint( midLimbJnt, aimLoc, worldUpType="object", aimVector=(1,0,0), upVector=(0,1,0), worldUpObject= butLimbJnt  ) )

			# orient joints according to aim locator
			for jnt in bipedLimbJnts[:-4]:
				OriJnt( jnt=jnt, upAim=aimLoc , aimAxis='-y' )

			# set preferred angle
			midLimbJnt.preferredAngleZ.set( 90 )
			
			# find foot Y rotation to pass to rigIK and rigFKIK
			footRotateY = ProjectedAim( objs=( butLimbJnt , toeEndJnt ) )
			footRotate = ( 0, footRotateY, 0 )					

		# pole vector transformations to be passed to rigIK and rigFKIK
		PVposition = pm.xform( aimLoc, q=True, ws=True, t=True )
		PVrotation = pm.xform( aimLoc, q=True, ws=True, ro=True )
		poleVectorTransform = ( PVposition, PVrotation )
		
		

		#============================================================================
		# If mirror is ON
		if mirror == True:
			# mirror joints
			OSjnts =  pm.mirrorJoint( upLimbJnt, mirrorYZ=True , mirrorBehavior=True, searchReplace=( "L", "R" ) )
			if mode=='leg':
				OSjnts.append( pm.mirrorJoint( heelJnt, mirrorYZ=True , mirrorBehavior=True, searchReplace=( "L", "R" ) ) )
				OSjnts.append( pm.mirrorJoint( outsideJnt, mirrorYZ=True , mirrorBehavior=True, searchReplace=( "L", "R" ) ) )
				OSjnts.append( pm.mirrorJoint( insideJnt, mirrorYZ=True , mirrorBehavior=True, searchReplace=( "L", "R" ) ) )
			OSbipedLimbJnts = pm.ls( OSjnts )

			# transforms of mirrored pole vector
			OSaimLoc = MirrorObjLikeJnt( aimLoc )[0]
			OSPVposition = pm.xform( OSaimLoc, q=True, ws=True, t=True )
			OSPVrotation = pm.xform( OSaimLoc, q=True, ws=True, ro=True )
			OSpoleVectorTransform = ( OSPVposition, OSPVrotation )
			
			# transforms of mirrored hand or foot control
			footNull = pm.group(em=True)
			if mode=='leg':
				footNull.translate.set( anklePos )
				footNull.rotate.set( footRotate )
			elif mode=='arm':
				footNull.translate.set( handPos )
			
			OShandTransforms = MirrorObjLikeJnt( objs=footNull, returnValue=True )
			OSfootRotate = OShandTransforms[0][1]
			pm.delete( footNull )


		#============================================================================
		# create IK, FK rigs and blend them
		
		
		# FK mode =============
		if FKIKMode == 'FK':
			RigFK( jnts = OSbipedLimbJnts, side = side )
			# other side
			if mirror:
				RigFK( jnts = OSbipedLimbJnts, side=otherSide )

			

		# IK mode =============
		elif FKIKMode == 'IK':
			armRigStuff = RigIK( 		  jnts=bipedLimbJnts
										, mode=mode
										, side = side
										, poleVectorTransform=poleVectorTransform
										, footRotate=footRotate
										, rigHandOrFoot=True
										, ctrlSize = ctrlSize )
			
			
			# other side
			if mirror:
				OSarmRigStuff = RigIK( 		  jnts=OSbipedLimbJnts 
											, mode=mode
											, side=otherSide
											, poleVectorTransform=OSpoleVectorTransform
											, mirrorMode=True
											, footRotate=OSfootRotate
											, rigHandOrFoot=True
											, ctrlSize = ctrlSize )
				

		# FKIK mode =============
		elif FKIKMode == 'FKIK':
			# for i in ( bipedLimbJnts, mode, side, poleVectorTransform, footRotate ):
				# print i
			# return None			
			FKIKstuff = RigFKIK( 		  jnts=bipedLimbJnts
										, mode=mode
										, side=side
										, poleVectorTransform=poleVectorTransform
										, footRotate=footRotate
										, rigHandOrFoot=True
										, ctrlSize = ctrlSize )
			
			# other side
			if mirror:
				OSFKIKstuff = RigFKIK( 		  jnts=OSbipedLimbJnts
											, mode=mode
											, side=otherSide
											, poleVectorTransform=OSpoleVectorTransform
											, mirrorMode=True
											, footRotate=(0,0,0)
											, rigHandOrFoot=True )
				
				'''
				OSFKIKstuff = RigFKIK( 		  jnts=OSbipedLimbJnts
											, mode=mode
											, side=otherSide
											, poleVectorTransform=OSpoleVectorTransform
											, mirrorMode=True
											, footRotate=OSfootRotate
											, rigHandOrFoot=True )
				'''
		
		
		#============================================================================
		# rig bendy limbs
		bendies = RigBendyLimb( jnts=bipedLimbJnts[:3]
								, bendyCtrl=FKIKstuff[3]
								, numOfSegs= numOfSegs
								, side=side )
		if mirror:
			OSbendies = RigBendyLimb( jnts=OSbipedLimbJnts[:3]
									, bendyCtrl=OSFKIKstuff[3]
									, numOfSegs= numOfSegs
									, isMirroredJoint=True
									, side=otherSide )
		
		# clean up
		pm.delete( self.BipedLimbInitJnts, aimLoc )
		bendies[-1].setParent( FKIKstuff[-1] )
		if mirror:
			pm.delete( OSaimLoc )
			OSbendies[-1].setParent( OSFKIKstuff[-1] )
