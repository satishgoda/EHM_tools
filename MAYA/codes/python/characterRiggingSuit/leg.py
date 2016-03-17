'''
synopsis :                         ehm_leg (self , legSize , mainCtrl , numberOfJnts  , side , mode)
                           

what does this script do ?		 rigs spine


flags :                            mainCtrl, (string)           =>      scale attribute of character's main control

                                    numberOfJnts, (int)       =>      number of spine joints

how to use :           select two locators representing hip and Leg
                        and run this ie : 
mainCtrl = pm.PyNode('main_ctrl')
Leg = ehm_leg(legSize=100 , mainCtrl=mainCtrl)
Leg.startLeg( "L" )
Leg.finishLeg(side='L' , FKIKMode=True , legNumOfJnts=6 , switchSides=False , bendy=False)
Leg.finishLeg(side='R' , FKIKMode=True , legNumOfJnts=6 , switchSides=True , bendy=False)
Leg.bendyLimb()


requirement :          Renamer, ctrlForThis, ZeroGrp, stretchySpline


============================================================================
'''


import pymel.core as pm
import math

import codes.python.general.searchReplaceNames as searchReplaceNames
reload( searchReplaceNames )
SearchReplaceNames = searchReplaceNames.SearchReplaceNames

import codes.python.general.lockHideAttr as lockHideAttr
reload( lockHideAttr )
LockHideAttr = lockHideAttr.LockHideAttr

import codes.python.general.dispOver as dispOver
reload( dispOver )
DispOver = dispOver.DispOver

import codes.python.general.renamer as renamer
reload( renamer )
Renamer = renamer.Renamer

import codes.python.curves.circle8Crv as circle8Crv
reload( circle8Crv )
Circle8Crv = circle8Crv.Circle8Crv

import codes.python.curves.softSpiralCrv as softSpiralCrv
reload( softSpiralCrv )
SoftSpiralCrv = softSpiralCrv.SoftSpiralCrv

import codes.python.curves.footCrv as footCrv
reload( footCrv )
FootCrv = footCrv.FootCrv

import codes.python.rig.zeroGrp as zeroGrp
reload( zeroGrp )
ZeroGrp = zeroGrp.ZeroGrp

import codes.python.rig.makeSplineStretchy as makeSplineStretchy
reload( makeSplineStretchy )
MakeSplineStretchy = makeSplineStretchy.MakeSplineStretchy

import codes.python.rig.jntToCrv as jntToCrv
reload( jntToCrv )
JntToCrv = jntToCrv.JntToCrv

import codes.python.curves.cubeCrv as cubeCrv
reload( cubeCrv )
CubeCrv = cubeCrv.CubeCrv

import codes.python.rig.distGlobalScale as distGlobalScale
reload( distGlobalScale )
DistGlobalScale = distGlobalScale.DistGlobalScale



# start of the ehm_Leg class

class Leg ():
	#========================================================================================================
	#========================================================================================================

	def __init__ (self , legSize , mainCtrl  ) :

		self.legSize            =     legSize
		self.mainCtrl           =     mainCtrl


		self.legSize /= 20


	#========================================================================================================
	# make initial joints for starting the rig
	#========================================================================================================

	def startLeg ( self , side ):
		print 'ehm_leg........................startLeg'
		self.side               =     side

		if self.side == "R" :
			pm.select ( clear = True )
			self.upLegInitJnt =     pm.joint ( p = ( -2     ,  self.legSize*7 , 0)                     , name = "leg_upLegInitJnt" )
			self.kneeInitJnt =      pm.joint ( p = ( -2     ,  self.legSize*4 , 0)                     , name = "leg_kneeInitJnt" )
			self.ankleInitJnt =      pm.joint ( p = ( -2     ,  self.legSize*1 , 0)                     , name = "leg_ankleInitJnt" )
			self.heelInitJnt =   pm.joint ( p = ( -2     , 0 , self.legSize*-1 )                    , name = "leg_heelInitJnt" )
			self.toeInitJnt =   pm.joint ( p = ( -2     , 0 , self.legSize* 2 )                     , name = "leg_toeInitJnt" )
			self.toeEndInitJnt =   pm.joint ( p = ( -2     , 0, self.legSize*4 )                      , name = "leg_toeEndInitJnt" )
			pm.pickWalk ( d = "up")
			self.outPivInitJnt =   pm.joint ( p = (  -(2 - self.legSize)  , 0, self.legSize*2 )                       , name = "leg_outPivInitJnt" )
			pm.pickWalk ( d = "up")
			self.inPivInitJnt =   pm.joint ( p = ( -(2 + self.legSize)  , 0 , self.legSize*2)        , name = "leg_inPivInitJnt" )
			pm.select ( clear=True )

		else :
			pm.select ( clear = True )
			self.upLegInitJnt =     pm.joint ( p = ( 2     ,  self.legSize*7 , 0)                     , name = "leg_upLegInitJnt" )
			self.kneeInitJnt =      pm.joint ( p = ( 2     ,  self.legSize*4 , 0)                     , name = "leg_kneeInitJnt" )
			self.ankleInitJnt =      pm.joint ( p = ( 2     ,  self.legSize*1 , 0)                     , name = "leg_ankleInitJnt" )
			self.heelInitJnt =   pm.joint ( p = ( 2     , 0 , self.legSize*-1 )                    , name = "leg_heelInitJnt" )
			self.toeInitJnt =   pm.joint ( p = ( 2     , 0 , self.legSize* 2 )                     , name = "leg_toeInitJnt" )
			self.toeEndInitJnt =   pm.joint ( p = ( 2     , 0, self.legSize*4 )                      , name = "leg_toeEndInitJnt" )
			pm.pickWalk ( d = "up")
			self.outPivInitJnt =   pm.joint ( p = (  2 - self.legSize  , 0, self.legSize*2 )                       , name = "leg_outPivInitJnt" )
			pm.pickWalk ( d = "up")
			self.inPivInitJnt =   pm.joint ( p = (  2 + self.legSize  , 0 , self.legSize*2)        , name = "leg_inPivInitJnt" )
			pm.select ( clear=True )

			
		return self.upLegInitJnt


	#========================================================================================================
	# finish def, will take the arguments and calls proper methods such as FKIK, FK or IK
	#========================================================================================================

	def finishLeg  ( self , side , FKIKMode , legNumOfJnts , switchSides , bendy):
		print 'ehm_leg........................finishLeg'
		self.side              =    side
		self.FKIKMode          =    FKIKMode
		self.legNumOfJnts      =    legNumOfJnts
		self.switchSides       =    switchSides
		self.bendy             =    bendy
		self.skinJnts = []

		#============================================================================
		# getting info from selected objects


		self.upLegPos =  pm.xform  ( self.upLegInitJnt , q = True  , ws = True ,  translation = True  )
		self.kneePos  = pm.xform  ( self.kneeInitJnt , q = True  , ws = True ,  translation = True  )
		self.anklePos  = pm.xform  ( self.ankleInitJnt , q = True  , ws = True ,  translation = True  )
		self.heelPos  = pm.xform  ( self.heelInitJnt , q = True  , ws = True ,  translation = True  )
		self.toePos =  pm.xform  ( self.toeInitJnt , q = True  , ws = True ,  translation = True  )
		self.toeEndPos  = pm.xform  ( self.toeEndInitJnt , q = True  , ws = True ,  translation = True  )
		self.outPivPos  = pm.xform  ( self.outPivInitJnt , q = True  , ws = True ,  translation = True  )
		self.inPivPos  = pm.xform  ( self.inPivInitJnt , q = True  , ws = True ,  translation = True  )        


		#============================================================================        
		# if switchSides is on then, reverse the x position of joints
		if self.switchSides :
			self.upLegPos[0]           =   self.upLegPos[0]         * -1
			self.kneePos[0]            =   self.kneePos[0]          * -1  
			self.anklePos[0]           =   self.anklePos[0]         * -1
			self.heelPos[0]            =   self.heelPos[0]          * -1
			self.toePos[0]             =   self.toePos[0]           * -1
			self.toeEndPos[0]          =   self.toeEndPos[0]        * -1
			self.outPivPos[0]          =   self.outPivPos[0]        * -1
			self.inPivPos[0]           =   self.inPivPos[0]         * -1

		#============================================================================
		# calculating the distance between leg and ankle, gets used for many things, like position of bendy joints and so
			
		self.dist =  math.sqrt (  pow ( (self.kneePos[0] - self.upLegPos[0] ) , 2 ) +  pow ( (self.kneePos[1] - self.upLegPos[1]) , 2 ) +  pow ((self.kneePos[2] - self.upLegPos[2] ) , 2 )  )


		#============================================================================
		# create leg joints

		pm.select ( cl = True )
		self.upLegJnt =pm.joint ( p = ( self.upLegPos[0] , self.upLegPos[1] ,self.upLegPos[2] ) , name = ( self.side + "_upLeg_jnt" ) )

		pm.select ( cl = True )
		self.kneeJnt = pm.joint ( p = ( self.kneePos[0] , self.kneePos[1] ,self.kneePos[2] ) , name = ( self.side + "_knee_jnt" ) )

		pm.select ( cl = True )
		self.ankleJnt = pm.joint ( p = ( self.anklePos[0] , self.anklePos[1] ,self.anklePos[2] ) , name = ( self.side + "_ankle_jnt" ) )

		pm.select ( cl = True )
		self.toeJnt = pm.joint ( p = ( self.toePos[0]  , self.toePos[1] ,self.toePos[2] ) , name = ( self.side + "_toe_jnt" ) )

		pm.select ( cl = True )
		self.toeEndJnt = pm.joint ( p = ( self.toeEndPos[0]  , self.toeEndPos[1] ,self.toeEndPos[2] ) , name = ( self.side + "_toe_end_jnt" ) )

		#============================================================================
		# parent, set the orientation and preferred angle for leg joints 

		pm.parent ( self.kneeJnt , self.upLegJnt )
		pm.parent ( self.ankleJnt , self.kneeJnt )
		pm.parent ( self.toeJnt , self.ankleJnt )
		pm.parent ( self.toeEndJnt , self.toeJnt )


		pm.joint ( self.upLegJnt ,  e  = True , zso = True , oj = "xzy" , sao = "zup" , ch = True )


		#======= 
		# if knee has rotations, we have to orient the joints differently

		kneeOri =  pm.getAttr ( self.kneeJnt.jointOrient )

		tempLocPos=[]


		if kneeOri[0] != 0 or kneeOri[1] != 0 or kneeOri[2] != 0 :
			
			tempLocPos.append(  ( ( self.upLegPos[0] + self.anklePos[0] ) / 2.0 )  )
			tempLocPos.append(  ( ( self.upLegPos[1] + self.anklePos[1] ) / 2.0 )  )
			tempLocPos.append(  ( ( self.upLegPos[2] + self.anklePos[2] ) / 2.0 )  )
			
			tempAim = pm.spaceLocator ( p = (0,0,0) )
			tempAim.translate.set (tempLocPos)
			
			pm.delete (  pm.aimConstraint ( self.kneeJnt , tempAim  , worldUpObject = tempAim , offset = (0 ,0 ,0) ,weight =1 ,aimVector =(1 ,0 ,0) ,upVector =(0 ,1 ,0) ,worldUpType ="vector" , worldUpVector = (0 ,1,0) )  ) 
			
			pm.move ( tempAim , 5*self.legSize , x =True ,  relative=True, objectSpace=True, worldSpaceDistance=True )
			
			pm.parent (self.kneeJnt , w=True)
			pm.parent (self.ankleJnt , w=True)
			pm.parent (self.toeJnt , w=True)
			pm.parent (self.toeEndJnt , w=True)
			
			pm.delete (  pm.aimConstraint (self.kneeJnt , self.upLegJnt , worldUpObject = tempAim , offset = (0 ,0 ,0) ,weight =1 ,aimVector =(1 ,0 ,0) ,upVector =(0 ,0 ,1) ,worldUpType ="object" ,  )    )

			pm.delete (  pm.aimConstraint (self.ankleJnt , self.kneeJnt , worldUpObject = tempAim , offset = (0 ,0 ,0) ,weight =1 ,aimVector =(1 ,0 ,0) ,upVector =(0 ,0 ,1) ,worldUpType ="object" ,  )   )

			pm.delete (  pm.aimConstraint (self.toeJnt , self.ankleJnt , worldUpObject = tempAim , offset = (0 ,0 ,0) ,weight =1 ,aimVector =(1 ,0 ,0) ,upVector =(0 ,0 ,1) ,worldUpType ="object" ,  )  )
			
			pm.delete (  pm.aimConstraint (self.toeEndJnt , self.toeJnt , worldUpObject = tempAim , offset = (0 ,0 ,0) ,weight =1 ,aimVector =(1 ,0 ,0) ,upVector =(0 ,0 ,1) ,worldUpType ="object" ,  )  )

			pm.parent (self.kneeJnt , self.upLegJnt)
			pm.parent (self.ankleJnt , self.kneeJnt)
			pm.parent (self.toeJnt , self.ankleJnt)
			pm.parent (self.toeEndJnt , self.toeJnt)           

			pm.makeIdentity (self.upLegJnt , apply = True , t = 1 , r = 1 , s = 1 , n = 0)


			pm.delete ( tempAim )

			self.toeEndJnt.jointOrient.set( 0,0,0 )
			
			############## pm.setAttr ( self.kneeJnt.attr ("preferredAngleY") , 90) ???????????????


		#============================================================================
		# FKIK, FK or IK ?

		if self.FKIKMode == "FK" :
			self.fkLimb()

		elif self.FKIKMode == "IK" :
			self.ikLimb()

		else :
			self.fkikLimb()


		#============================================================================
		# bendy if needed

		if bendy :
			print 'ehm_leg----------------------Rigging Bendy'
			self.bendyLimb()


		#================================================================================
		# clean outliner by parenting. Also, hiding unnecessary nodes and attributes. 

		legZero = pm.group(em=True , name= self.side + "_leg_zero" )
		legZero.translate.set ( self.upLegPos )

		self.FKIKMode         
		self.legNumOfJnts     
		self.switchSides     
		self.bendy        

		#=============================
		# find and rename skin joints

		if self.bendy :

			tempSkinJnts = pm.ls ( self.ankleJnt )
			
			for jnt in tempSkinJnts :
				self.skinJnts.append ( jnt  )
				
			pm.select (tempSkinJnts )
				
			if self.FKIKMode == "FK" :
				SearchReplaceNames  ( searchString="_ctrl", replaceString="_skinCtrl", objs=tempSkinJnts  )
				
			else:
				SearchReplaceNames  ( searchString="_jnt", replaceString="_skinJnt", objs=tempSkinJnts  )



		else:
			
			tempSkinJnts = pm.ls ( self.upLegJnt , self.kneeJnt , self.ankleJnt )
			
			for jnt in tempSkinJnts :
				self.skinJnts.append ( jnt  )
			
			pm.select (tempSkinJnts )
			
			if self.FKIKMode == "FK" :
				SearchReplaceNames  ( "_ctrl", "_skinCtrl", tempSkinJnts )

			else:
				SearchReplaceNames  ( "_jnt", "_skinJnt", tempSkinJnts  ) 




		#===================================================
		# clean FK mode

		if self.FKIKMode == "FK" or self.FKIKMode == "FKIK":

			
			pm.parent ( self.FKJnts[0] , legZero )
			
			# lock and hide extra attributes
			for FKJnt in self.FKJnts :
				LockHideAttr( objs=FKJnt, attrs="t")
				LockHideAttr( objs=FKJnt, attrs="s")
				LockHideAttr( objs=FKJnt, attrs="v")
				LockHideAttr( objs=FKJnt, attrs="radius")
			#=============================
			# override color of FKJnts' shapes also change display to bounding box for making it invisible
			DispOver( self.FKJnts[0] , "on")
			pm.setAttr ( (self.FKJnts[0].attr ("overrideLevelOfDetail" )), 1 )
			for FKJnt in self.FKJnts :
				shapes = (pm.listRelatives (FKJnt , c=True , type= "shape" ))
				if shapes != [] :
					if  self.side == "L" :
						DispOver( shapes[0] , "col" , 13)
					else :
						DispOver( shapes[0] , "col" , 6)  




		#===================================================
		# clean IK mode 
			   

		if self.FKIKMode == "IK" or self.FKIKMode == "FKIK":
			
			pm.parent ( self.IKJnts[0] , legZero )
			pm.setAttr (self.IKJnts[0].attr("v") , False ,lock=True )
			
			# distance nodes
			pm.parent ( self.IKLegDistT , legZero )            
			IKStuff = pm.group (self.IKLegDistT , name = self.side + "_IK_stuff")
			pm.parent ( self.IKupLegDistT , IKStuff )
			pm.parent ( self.IKKneeDistT , IKStuff )
			pm.parent ( self.IKlegDistLocs[0] , IKStuff )
			pm.setAttr (IKStuff.attr("v") , False ,lock=True )

			# dist locs
			pm.setAttr (self.IKlegDistLocs[1].attr("v") , False ,lock=True )
			LockHideAttr( objs=self.IKKneeDistLocs[0] , attrs="vv")
			
			# ankle IK ctrl
			pm.parent ( self.ankleIKCtrlZero  , self.mainCtrl )
			LockHideAttr( objs=self.ankleIKCtrl , attrs="s")

			
			# knee IK ctrl
			pm.parent ( self.kneeIKCtrlZO[0]  , self.mainCtrl )
			LockHideAttr( objs=self.kneeIKCtrl , attrs="r")
			LockHideAttr( objs=self.kneeIKCtrl , attrs="s")

			
			# override color of IK control shapes

			if  self.side == "L" :
				DispOver( self.ankleIKCtrl , "col" , 13)
				DispOver( self.kneeIKCtrl , "col" , 13)

			else :
				DispOver( self.ankleIKCtrl , "col" , 6)
				DispOver( self.kneeIKCtrl , "col" , 6)
			
			
			#parent PV guide curve start joint
			pm.parent ( self.PVGuideStartJnt , self.kneeJnt )
			self.PVGuideStartJnt.translate.set(0,0,0)

			pm.setAttr ( self.PVGuideCrv.attr("tx") , lock=False)
			pm.setAttr ( self.PVGuideCrv.attr("ty") , lock=False)
			pm.setAttr ( self.PVGuideCrv.attr("tz") , lock=False) 
					   
			pm.parent ( self.PVGuideCrv , legZero  )
			
			self.PVGuideCrv.translate.set(0,0,0)


		#===================================================
		# clean FKIK mode

		if self.FKIKMode == "FKIK":
			
			pm.parent ( self.upLegJnt , legZero )
			pm.setAttr (self.upLegJnt.attr("v") , False ,lock=True )
			# finger ctrl cleanup
			pm.parent (self.toeCtrlZO[0] , self.ankleJnt  )
			

			if self.side =="L" :
				self.toeCtrlZO[0].translate.set ( 0 , (self.legSize * 1 ) ,0)
				self.toeCtrlZO[0].scale.set (-1,1,1)
			else:
				self.toeCtrlZO[0].translate.set ( 0 , (self.legSize * -1 ) ,0)
							  

			
			pm.makeIdentity (self.toeCtrlZO[0], apply =True , r=True)
			pm.parent (self.toeCtrlZO[0] , legZero )
			pm.parentConstraint ( self.ankleJnt , self.toeCtrlZO[0] , maintainOffset=True )
			LockHideAttr( objs=self.toesCtrl , attrs="t")
			LockHideAttr( objs=self.toesCtrl , attrs="r")
			LockHideAttr( objs=self.toesCtrl , attrs="s")
			LockHideAttr( objs=self.toesCtrl , attrs="v")
			

			
			# connect finger IKFK to FK visibility
			pm.setAttr ( self.FKJnts[0].attr("v") , lock= False   )
			self.FKIK_vis_bln = pm.createNode ("reverse", n = self.side + "_FKIK_vis_rev")
			self.toesCtrl.FKIK        >>     self.FKIK_vis_bln.inputX 
			self.FKIK_vis_bln.outputX       >>     self.FKJnts[0].visibility 
			pm.setAttr ( self.FKJnts[0].attr("v") , lock= True   ) 
			
		 
			# connect finger IKFK to IK visibility

			self.toesCtrl.FKIK        >>     self.kneeIKCtrl.visibility
			self.toesCtrl.FKIK        >>     self.ankleIKCtrl.visibility
			self.toesCtrl.FKIK        >>     self.PVGuideCrv.visibility             
			LockHideAttr( objs=self.ankleIKCtrl , attrs="v")
			LockHideAttr( objs=self.kneeIKCtrl , attrs="v")

		#===================================================
		# bendy mode


		if self.bendy :
			pm.parent ( self.segMainJnts[0] , legZero )
			# seg ik stuff
			pm.parent ( self.upLeg_seg_ik_stuff[0] , legZero )
			segStuff = pm.group ( self.upLeg_seg_ik_stuff[0] , name = self.side + "_seg_stuff")
			pm.parent ( self.upLeg_seg_ik_stuff[2] , segStuff )
			pm.parent ( self.knee_seg_ik_stuff[0] , segStuff )
			pm.parent ( self.knee_seg_ik_stuff[2] , segStuff )
			pm.setAttr (segStuff.attr("v") , False ,lock=True )
			
			# mid ctrl
			pm.parent ( self.midCtrlParent , legZero )
			
			# override color of fingers control

			if  self.side == "L" :
				DispOver( self.midCtrl , "col" , 9)

			else :
				DispOver( self.midCtrl , "col" , 30)   
				
			# set advanced twist on upLeg seg ik
			pm.connectAttr ( legZero + ".worldMatrix[0]" , self.upLeg_seg_ikh + ".dWorldUpMatrix" , f = True )
			
			#parent PV guide curve start joint to mid if bendy
			if self.FKIKMode != "FK" :
				pm.parent ( self.PVGuideStartJnt , self.midCtrl )
				self.PVGuideStartJnt.translate.set(0,0,0)
				self.PVGuideCrv.translate.set(0,0,0)


		# put everything under main ctrl               
		pm.parent ( legZero  , self.mainCtrl )


		# create selection set for skin joints
		pm.sets ( self.skinJnts  , n = self.side + "_leg_skinJoints_set")



	#========================================================================================================
	# FK rig
	#========================================================================================================

	def fkLimb( self , *args ):
		print 'ehm_leg........................fkLimb'
		#===============================================================================
		# duplicate main leg joints and rename FK joints

		self.FKJnts = pm.duplicate (self.upLegJnt )
		pm.select (self.FKJnts[0])
		self.FKJnts = SearchReplaceNames ( "jnt", "FK_ctrl", self.FKJnts[0] )




		#=============================================
		# add length attribute and connect it to scale 

		for jnt in range ( len (self.FKJnts) -3 ):
			pm.addAttr (  self.FKJnts[jnt] , ln = "length"  , at = "double"  , min = 0 , dv = 1 , k = True  )
			pm.connectAttr ( self.FKJnts[jnt]+".length", self.FKJnts[jnt]+".scaleX" )




		#=============================
		# creating curves on FK joints except for the ankle end joint

		pm.select (self.FKJnts[0] , self.FKJnts[1], self.FKJnts[2] , self.FKJnts[3] )

		JntToCrv (self.legSize)


		#=============================
		# if just fk leg is needed then delete leg joints and us fk joints as leg joints
		# this way we won't have extra result joint, just fk joints will remain in the scene
		if self.FKIKMode == "FK" :
			pm.delete (self.upLegJnt)
			self.upLegJnt = self.FKJnts[0]
			self.kneeJnt = self.FKJnts[1]
			self.ankleJnt = self.FKJnts[2]
			self.toeJnt = self.FKJnts[3]
			self.toeEndJnt = self.FKJnts[4]





	#========================================================================================================
	# IK rig
	#========================================================================================================

	def ikLimb( self, *args ):
		print 'ehm_leg........................ikLimb'

		#===============================================================================
		# duplicate main leg joints and rename IK joints
		
		self.IKJnts = pm.duplicate (self.upLegJnt )
		pm.select (self.IKJnts[0])
		self.IKJnts = SearchReplaceNames ( "jnt", "IK_jnt", self.IKJnts[0] )



		#===============================================================================
		# create ik handles

		self.legIKStuff  = pm.ikHandle(  sj = self.IKJnts[0], ee = self.IKJnts[2], solver = "ikRPsolver"  )
		pm.rename (self.legIKStuff[0] ,   (self.side + "_leg_ikh") )



		#===============================================================================
		# distance nodes for stretching purpose
		self.IKLegDist = pm.distanceDimension ( sp = self.upLegPos , ep = self.anklePos )
		self.IKupLegDist = pm.distanceDimension ( sp = self.upLegPos , ep = self.kneePos )
		self.IKKneeDist = pm.distanceDimension ( sp = self.kneePos , ep = self.anklePos )

		self.IKLegDistT = pm.listRelatives ( self.IKLegDist , p=True)[0]
		self.IKupLegDistT = pm.listRelatives ( self.IKupLegDist , p=True)[0]
		self.IKKneeDistT = pm.listRelatives ( self.IKKneeDist , p=True)[0]


		#===============================================================================
		# find the leg locs from distance shape node

		self.IKlegDistLocs = pm.listConnections (self.IKLegDist , plugs=False)
		self.IKKneeDistLocs = pm.listConnections (self.IKKneeDist , plugs=False)

		pm.rename (self.IKlegDistLocs[0] , self.side + "_upLeg_dist_loc" )
		pm.rename (self.IKlegDistLocs[1] , self.side + "_ankle_dist_loc" )
		pm.rename (self.IKKneeDistLocs[0] , self.side + "_knee_dist_loc" )




		#===============================================================================
		# parent ikHandle to ankle loc
		pm.parent ( self.legIKStuff[0] , self.IKKneeDistLocs[1] )
		





		#===============================================================================
		# make ik joints stretchy

		defaultIKLegLen = pm.getAttr ( self.IKupLegDist.distance ) + pm.getAttr ( self.IKKneeDist.distance )

		self.IKLeg_stretch_mdn = pm.createNode ("multiplyDivide" , n = self.side + "_IKLeg_stretch_mdn" )

		pm.setAttr ( self.IKLeg_stretch_mdn.input2X, defaultIKLegLen )

		self.IKLegDist.distance >> self.IKLeg_stretch_mdn.input1X

		pm.setAttr ( self.IKLeg_stretch_mdn.operation, 2 )

		self.IKLeg_stretch_cnd = pm.createNode ("condition" , n = self.side + "_IKLeg_stretch_cnd")

		self.IKLegDist.distance >> self.IKLeg_stretch_cnd.firstTerm
		pm.setAttr ( self.IKLeg_stretch_cnd.secondTerm , defaultIKLegLen )
		pm.setAttr ( self.IKLeg_stretch_cnd.operation , 2 )
		self.IKLeg_stretch_mdn.outputX >> self.IKLeg_stretch_cnd.colorIfTrueR




		#================================================================================
		# Knee Lock

		pm.addAttr ( self.IKKneeDistLocs[0] ,dv = 0 ,min=0 ,max=10 , keyable =  True , ln = "kneeLock" , at = "double")

		defaultIKupLegLen = pm.getAttr ( self.IKupLegDist.distance )
		self.IKupLeg_kneeLock_mdn = pm.createNode ("multiplyDivide" , n = self.side + "_IKupLeg_kneeLock_mdn" )
		pm.setAttr ( self.IKupLeg_kneeLock_mdn.input2X, defaultIKupLegLen )
		self.IKupLegDist.distance >> self.IKupLeg_kneeLock_mdn.input1X
		pm.setAttr ( self.IKupLeg_kneeLock_mdn.operation, 2 )


		defaultIKKneeLen = pm.getAttr ( self.IKKneeDist.distance )
		self.IKKnee_kneeLock_mdn = pm.createNode ("multiplyDivide" , n = self.side + "_IKKnee_kneeLock_mdn" )
		pm.setAttr ( self.IKKnee_kneeLock_mdn.input2X, defaultIKKneeLen )
		self.IKKneeDist.distance >> self.IKKnee_kneeLock_mdn.input1X
		pm.setAttr ( self.IKKnee_kneeLock_mdn.operation, 2 )


		#================================================================================
		# make kneeLock more animation friendly by dividing it by 10

		self.IKLeg_kneeLockAnimFriend_mdn = pm.createNode ("multiplyDivide" , n = self.side + "_IKLeg_kneeLockAnimFriend_mdn" )
		pm.setAttr ( self.IKLeg_kneeLockAnimFriend_mdn.input2X, 10 )
		pm.setAttr ( self.IKLeg_kneeLockAnimFriend_mdn.operation, 2 )
		self.IKKneeDistLocs[0].attr ( "kneeLock" )    >>      self.IKLeg_kneeLockAnimFriend_mdn.input1X


		#================================================================================
		# conncet result of stretch and knee lock to joint with a blend switch on the knee locator
		self.upLeg_stretchKneeLock_bta     =                   pm.createNode ("blendTwoAttr" , n = self.side + "_upLeg_stretchKneeLock_bta" )
		self.IKLeg_kneeLockAnimFriend_mdn.outputX       >>      self.upLeg_stretchKneeLock_bta.attributesBlender
		self.IKLeg_stretch_cnd.outColorR                >>      self.upLeg_stretchKneeLock_bta.input[0]
		self.IKupLeg_kneeLock_mdn.outputX              >>      self.upLeg_stretchKneeLock_bta.input[1]


		self.knee_stretchKneeLock_bta     =                   pm.createNode ("blendTwoAttr" , n = self.side + "_knee_stretchKneeLock_bta" )
		self.IKLeg_kneeLockAnimFriend_mdn.outputX       >>      self.knee_stretchKneeLock_bta.attributesBlender
		self.IKLeg_stretch_cnd.outColorR                >>      self.knee_stretchKneeLock_bta.input[0]
		self.IKKnee_kneeLock_mdn.outputX              >>      self.knee_stretchKneeLock_bta.input[1]

		self.upLeg_stretchKneeLock_bta.output          >>      self.IKJnts[0].scaleX  
		self.knee_stretchKneeLock_bta.output          >>      self.IKJnts[1].scaleX  


					
		#================================================================================
		# force leg distance dimentions to be scalable by mainCtrl



		DistGlobalScale (mainCtrl=self.mainCtrl , dist=self.IKLegDist)
		DistGlobalScale (mainCtrl=self.mainCtrl , dist=self.IKupLegDist)
		DistGlobalScale (mainCtrl=self.mainCtrl , dist=self.IKKneeDist)



		# create IK ankle control curve with transforms of the ankle joint       
		self.ankleIKCtrl = CubeCrv( self.legSize*1.5 , self.side + "_ankle_IK_ctrl" )

		pm.select ( self.ankleIKCtrl )
		self.ankleIKCtrlZero = ZeroGrp()[0]

		pm.parent ( self.ankleIKCtrlZero , self.IKJnts[2] )

		self.ankleIKCtrlZero.translate.set( 0,0,0 )
		# self.ankleIKCtrlZero.rotate.set( 0,0,0 )

		pm.parent ( self.ankleIKCtrlZero , w=True )


		pm.parent ( self.IKlegDistLocs[1]  , self.ankleIKCtrl )


		#============================================================================
		# add attributes to leg_ctrl

		pm.addAttr (  self.ankleIKCtrl , ln = "stretch_off_on"  , at = "double"  , min = 0 , max = 1 , dv = 1 , k = True  ) 

		pm.addAttr (  self.ankleIKCtrl , ln = "roll"  , at = "double"  , min = -10 , max = 10 , dv = 0 , k = True  )

		pm.addAttr (  self.ankleIKCtrl , ln = "toe"  , at = "double"  , min = -10 , max = 10 , dv = 0 , k = True  )

		pm.addAttr (  self.ankleIKCtrl , ln = "side_to_side"  , at = "double"  , min = -10 , max = 10 , dv = 0 , k = True  )


		#============================================================================
		# create foot ik handles

		self.toeIKStuff      = pm.ikHandle(  sj = self.IKJnts[2], ee = self.IKJnts[3], solver = "ikSCsolver"  )
		pm.rename(self.toeIKStuff[0], self.side + "_toe_ikh")
		self.toeEndIKStuff   = pm.ikHandle(  sj = self.IKJnts[3], ee = self.IKJnts[4], solver = "ikSCsolver"  )
		pm.rename(self.toeEndIKStuff[0], "_toe_end_ikh")


		#============================================================================
		# foot ik groups and set driven keys


		self.heelUpSdk =  pm.group ( self.toeIKStuff[0] , self.IKlegDistLocs[1] , n = self.side + "_heel_up_sdk"  )
		pm.xform ( os= True , piv = self.toePos )

		self.toeSdk =  pm.group( self.toeEndIKStuff[0] , n = self.side + "_toe_sdk"  )
		pm.xform ( os= True , piv = self.toePos )



		self.tipSdk = pm.group ( self.heelUpSdk , self.toeSdk  , n = self.side + "_tip_sdk"  )
		pm.xform ( os= True , piv = ( self.toeEndPos[0] , 0 , self.toeEndPos[2] )   )

		self.heelSdk =  pm.group ( self.tipSdk , n = self.side + "_heel_sdk"  )
		pm.xform ( os= True , piv = ( self.heelPos[0] , 0 , self.heelPos[2] )   ) 



		self.inFootSdk =  pm.group ( self.heelSdk, n = self.side + "_in_foot_sdk"  )
		pm.xform ( os= True , piv = ( self.inPivPos[0] , 0 , self.inPivPos[2] )   )

		self.outFootSdk =  pm.group ( self.inFootSdk , n = self.side + "_out_foot_sdk"  )
		pm.xform ( os= True , piv = ( self.outPivPos[0] , 0 , self.outPivPos[2] )   )



		pm.parent ( self.outFootSdk , self.ankleIKCtrl )


		#============================================================================
		# foot set driven keys

		# toe set driven keys
		pm.setDrivenKeyframe (   self.toeSdk.rotateX , currentDriver =  self.ankleIKCtrl.toe , dv = 0 , v = 0   )
		pm.setDrivenKeyframe (   self.toeSdk.rotateX , currentDriver =  self.ankleIKCtrl.toe , dv = 10 , v = -45   )
		pm.setDrivenKeyframe (   self.toeSdk.rotateX , currentDriver =  self.ankleIKCtrl.toe , dv = -10 , v = 70   )


		# roll set driven keys
		pm.setDrivenKeyframe (   self.heelSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = 0 , v = 0   )
		pm.setDrivenKeyframe (   self.tipSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = 0 , v = 0   )
		pm.setDrivenKeyframe (   self.heelUpSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = 0 , v = 0   )

		pm.setDrivenKeyframe (   self.heelSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = 10 , v = -30   )

		pm.setDrivenKeyframe (   self.tipSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = -10 , v = 45   )
		pm.setDrivenKeyframe (   self.heelUpSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = -10 , v = 0   )

		pm.setDrivenKeyframe (   self.tipSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = -5 , v = 0   )
		pm.setDrivenKeyframe (   self.heelUpSdk.rotateX , currentDriver = self.ankleIKCtrl.roll , dv = -5 , v = 30   )


		#================================================================================
		# create IK knee control curve

			
		self.kneeIKCtrl = SoftSpiralCrv( self.legSize , self.side + "_knee_IK_ctrl" )

		if self.side == "R" :
			self.kneeIKCtrl.scale.scaleY.set (-1)
			pm.makeIdentity (self.kneeIKCtrl , apply = True , t = 1 , r = 1 , s = 1 , n = 0)

		pm.select ( self.kneeIKCtrl )
		self.kneeIKCtrlZO = ZeroGrp()

		pm.parent ( self.kneeIKCtrlZO[0] , self.IKJnts[1] )

		self.kneeIKCtrlZO[0].translate.set( 0,0,0 )
		#self.kneeIKCtrlZO[0].rotate.set( 0,0,0 )

		pm.parent ( self.kneeIKCtrlZO[0] , w=True )

		pm.parent ( self.IKKneeDistLocs[0]  , self.kneeIKCtrl )


		# direction of the knee ctrl is defined here. ????????????????????????????????
		self.kneeIKCtrlZO[1].translate.set (0,0, self.legSize*3)

		pm.poleVectorConstraint( self.IKKneeDistLocs[0] , self.legIKStuff[0] )

		#===========
		# pv guide curve

		self.PVGuideCrv = pm.curve ( d = 1 ,
					
					p = ( (self.kneePos) , (0,0,0 ) ) ,

					k = (1,2) , name = self.side + "_PV_guide_crv" )

		self.PVGuideStartJnt =pm.joint ( p = (self.kneePos) , name = ( self.side + "_PV_guide_start_jnt" ) )
		pm.select (cl=True)
		self.PVGuideEndJnt =pm.joint ( p = (0,0,0) , name = ( self.side + "_PV_guide_end_jnt" ) )

		pm.skinCluster( self.PVGuideCrv ,  self.PVGuideStartJnt , self.PVGuideEndJnt , toSelectedBones = True )

		pm.parent (self.PVGuideEndJnt , self.kneeIKCtrl)
		self.PVGuideEndJnt.translate.set(0,0,0)

		pm.setAttr ( self.PVGuideCrv.overrideEnabled , True)
		pm.setAttr ( self.PVGuideCrv.overrideDisplayType , True)

		pm.setAttr ( self.PVGuideCrv.inheritsTransform , False)

		LockHideAttr ( objs=self.PVGuideStartJnt , attrs="vv")
		LockHideAttr ( objs=self.PVGuideEndJnt , attrs="vv")



		#================================================================================
		# if just ik leg is needed then delete leg joints and us ik joints as leg joints
		# this way we won't have extra result joint, just ik joints will remain in the scene

		if self.FKIKMode == "IK" :
			pm.delete (self.upLegJnt)
			self.upLegJnt = self.IKJnts[0]
			self.kneeJnt = self.IKJnts[1]
			self.ankleJnt = self.IKJnts[2]
			self.toeJnt = self.IKJnts[3]  

 

	#========================================================================================================
	# FKIK rig
	#========================================================================================================

	def fkikLimb( self  ):
		print 'ehm_leg........................fkikLimb'
		self.toesCtrl =  FootCrv( self.legSize*1.2 , self.side + "_toes_ctrl")

		pm.select (self.toesCtrl)

		self.toeCtrlZO = ZeroGrp()

		pm.addAttr (  self.toesCtrl , ln = "FKIK"  , at = "double"  , min = 0 , max = 1 , dv = 0 , k = True  )


		self.ikLimb()

		self.fkLimb()



		#================================================================================
		# connect fk and ik to fkik result joints

		self.FKIKupLeg_RotResult_bln = pm.createNode ("blendColors", n = self.side + "_FKIKupLeg_RotResult_bln")
		self.FKIKupLeg_SclResult_bln = pm.createNode ("blendColors", n = self.side + "_FKIKupLeg_SclResult_bln")

		self.FKJnts[0].rotate     >>     self.FKIKupLeg_RotResult_bln.color2
		self.IKJnts[0].rotate     >>     self.FKIKupLeg_RotResult_bln.color1 
			   
		self.FKJnts[0].scale      >>     self.FKIKupLeg_SclResult_bln.color2
		self.IKJnts[0].scale      >>     self.FKIKupLeg_SclResult_bln.color1        

		self.toesCtrl.FKIK      >>     self.FKIKupLeg_RotResult_bln.blender
		self.toesCtrl.FKIK      >>     self.FKIKupLeg_SclResult_bln.blender

		self.FKIKupLeg_RotResult_bln.output       >>     self.upLegJnt.rotate
		self.FKIKupLeg_SclResult_bln.output       >>     self.upLegJnt.scale





		self.FKIKKnee_RotResult_bln = pm.createNode ("blendColors", n = self.side + "_FKIKKnee_RotResult_bln")
		self.FKIKKnee_SclResult_bln = pm.createNode ("blendColors", n = self.side + "_FKIKKnee_SclResult_bln")

		self.FKJnts[1].rotate     >>     self.FKIKKnee_RotResult_bln.color2
		self.IKJnts[1].rotate     >>     self.FKIKKnee_RotResult_bln.color1
			 
		self.FKJnts[1].scale      >>     self.FKIKKnee_SclResult_bln.color2
		self.IKJnts[1].scale      >>     self.FKIKKnee_SclResult_bln.color1

		self.toesCtrl.FKIK      >>     self.FKIKKnee_RotResult_bln.blender
		self.toesCtrl.FKIK      >>     self.FKIKKnee_SclResult_bln.blender

		self.FKIKKnee_RotResult_bln.output       >>     self.kneeJnt.rotate
		self.FKIKKnee_SclResult_bln.output       >>     self.kneeJnt.scale




		self.FKIKAnkle_RotResult_bln = pm.createNode ("blendColors", n = self.side + "_FKIKAnkle_RotResult_bln")

		self.FKJnts[2].rotate     >>     self.FKIKAnkle_RotResult_bln.color2
		self.IKJnts[2].rotate     >>     self.FKIKAnkle_RotResult_bln.color1

		self.toesCtrl.FKIK      >>     self.FKIKAnkle_RotResult_bln.blender

		self.FKIKAnkle_RotResult_bln.output       >>     self.ankleJnt.rotate




		self.FKIKToe_RotResult_bln = pm.createNode ("blendColors", n = self.side + "_FKIKToe_RotResult_bln")

		self.FKJnts[3].rotate     >>     self.FKIKToe_RotResult_bln.color2
		self.IKJnts[3].rotate     >>     self.FKIKToe_RotResult_bln.color1

		self.toesCtrl.FKIK      >>     self.FKIKToe_RotResult_bln.blender

		self.FKIKToe_RotResult_bln.output       >>     self.toeJnt.rotate




		# override color of fingers control
		if  self.side == "L" :
			DispOver( self.toesCtrl , "col" , 13)
		else :
			DispOver( self.toesCtrl , "col" , 6)




	#========================================================================================================
	# bendy rig
	#========================================================================================================


	def bendyLimb( self , *args ):
		print 'ehm_leg........................bendyLimb'       
		
		#============================================================================
		# duplicate main leg joints and rename bendy joints
		
		self.segMainJnts = pm.duplicate (self.upLegJnt )

		# delete not joint nodes under the hierarchy if any
		extraShapes = pm.listRelatives (self.segMainJnts[0], ad=True )

		for extraShape in extraShapes :
			if not pm.objectType(extraShape) == "joint":
				pm.delete(extraShape)

		self.segMainJnt = pm.ls (self.segMainJnts[0] )[0]
		self.segMainJnts = pm.listRelatives (self.segMainJnts[0], ad=True )
		self.segMainJnts.append(self.segMainJnt)
		self.segMainJnts.reverse()


		#============================================================================
		# create locators for positioning and orienting "curvy_midCtrl"

		# upLeg_rev_loc
		upLeg_rev_loc =  pm.spaceLocator ( p = (0,0,0) )

		pm.parent ( upLeg_rev_loc , self.upLegJnt )
		pm.rename ( upLeg_rev_loc , self.side + "_upLeg_rev_loc" )

		upLeg_rev_loc.translate.translateX.set  ( self.dist + self.dist/20 ) 
		upLeg_rev_loc.translate.translateY.set  ( 0 )
		upLeg_rev_loc.translate.translateZ.set  ( (self.dist/200) )

		upLeg_rev_loc.rotate.set (0,0,0)


		
		#============================================================================
		# find the position of self.kneeJnt to create empty group for this loc
		# we can compensate the length of leg parts by scaling this group

		upLeg_rev_loc_grp = pm.group ( n = upLeg_rev_loc.name() + "_grp" )
		pm.xform ( upLeg_rev_loc_grp , ws=True , piv = self.kneePos)

		# we need to make this locator scalable. if not, we won't be able to scale upLeg or knee seperately
		upLeg_rev_loc_mdn = pm.createNode ("multiplyDivide" , n = upLeg_rev_loc.name() + "_mdn" )
		upLeg_rev_loc_mdn.operation.set ( 2 )
		upLeg_rev_loc_mdn.input1X.set ( 1 )

		self.upLegJnt.scaleX >>  upLeg_rev_loc_mdn.input2X

		upLeg_rev_loc_mdn.outputX >> upLeg_rev_loc_grp.scaleX

		
		#============================================================================
		# knee_rev_loc

		knee_rev_loc =  pm.spaceLocator ( p = (0,0,0) )
		pm.parent ( knee_rev_loc , self.kneeJnt )
		pm.rename ( knee_rev_loc , self.side + "_knee_rev_loc" )

		knee_rev_loc.translate.translateX.set (self.dist/-20)
		knee_rev_loc.translate.translateY.set ( 0 )
		knee_rev_loc.translate.translateZ.set (self.dist/200)

		knee_rev_loc.rotate.set (0,0,0) 


		pm.select(knee_rev_loc)
		knee_rev_loc_grp = pm.group ( n = knee_rev_loc.name() + "_grp" )
		pm.xform ( knee_rev_loc_grp , ws=True , piv = self.kneePos )
				  

		# we need to make this locator scalable. if not, we won't be able to scale upLeg or knee seperately

		knee_rev_loc_mdn = pm.createNode ("multiplyDivide" , n = knee_rev_loc.name() + "_mdn")
		knee_rev_loc_mdn.operation.set ( 2 )
		knee_rev_loc_mdn.input1X.set ( 1 )
		self.kneeJnt.scaleX          >>         knee_rev_loc_mdn.input2X
		knee_rev_loc_mdn.outputX     >>         knee_rev_loc_grp.scaleX



		# L_knee_aim_loc 
		#================
		knee_aim_loc =  pm.spaceLocator ( p = (0,0,0) )
		pm.parent (  knee_aim_loc , self.kneeJnt )
		pm.rename ( knee_aim_loc , self.side + "_knee_aim_loc" )

		pm.pointConstraint( upLeg_rev_loc , knee_rev_loc , knee_aim_loc )

		# creating the curvy_midCtrl_Parent for mid_joint position ( main purpose of this part )
		self.midCtrlParent = pm.group ( em = True )
		pm.pointConstraint(  self.kneeJnt , self.midCtrlParent )
		pm.aimConstraint ( knee_aim_loc, self.midCtrlParent , aimVector = (0,0,-1) , upVector = (-1,0,0) , worldUpType = "object" , worldUpObject = self.upLegJnt )
		pm.rename ( self.midCtrlParent , self.side + "_curvy_midCtrl_Parent")



		#============================================================================
		# finding the position for segMainJnts and creating them

		self.midJntPosition = 0.0


		midJnt = self.segMainJnts[0]


		# create upLeg seg joints
		for  i in ( range (self.legNumOfJnts-1) ) :
			
			midJntPosition = (self.kneeJnt.translate.translateX.get() / self.legNumOfJnts )
				
			midJnt = pm.insertJoint ( midJnt )
				
			pm.joint  (  midJnt , e = True , relative = True , component = True ,   position = ( midJntPosition  , 0 , 0 )  )

		#=============        
		# create knee seg joints 
		# create an extra joint on knee in segmenty so that we could create two ikSplines for the whole leg

		midJnt = self.segMainJnts[1]

		midJntParent = midJnt.duplicate()
		pm.delete ( pm.listRelatives ( midJntParent , allDescendents = True) )
		pm.parent ( midJnt , midJntParent)

		for  i in ( range (self.legNumOfJnts-1) ) :
			
			midJntPosition = (self.ankleJnt.translate.translateX.get() / self.legNumOfJnts )
				
			midJnt = pm.insertJoint ( midJnt )
				
			pm.joint  (  midJnt , e = True , relative = True , component = True ,   position = ( midJntPosition  , 0 , 0 )  )


		segJnts = pm.listRelatives ( self.segMainJnts[0] , allDescendents = True)
		segJnts.append ( self.segMainJnts[0] )
		segJnts.reverse()

		
		pm.select (segJnts)
		
		
		segJnts = Renamer ( objs=segJnts, name=self.side+"_leg_seg_###_jnt" , hierarchyMode=False).newJnts

		
		# select skin joint
		tempSkinJnts = pm.ls ( segJnts [ 0 : self.legNumOfJnts ] , segJnts [  self.legNumOfJnts+1 : self.legNumOfJnts*2+1 ] ) 

		# add skin jnt to skinJnts list
		for jnt in tempSkinJnts :
			self.skinJnts.append ( jnt )
		
		# rename them
		pm.select ( tempSkinJnts )
		SearchReplaceNames (  "_jnt", "_skinJnt", tempSkinJnts )



		#============================================================================
		# creating ik splines for segmenty joints
		pm.select ( segJnts[0] )
		pm.select ( segJnts[self.legNumOfJnts] , add = True )
		self.upLeg_seg_ik_stuff = pm.ikHandle ( sol = "ikSplineSolver" , parentCurve = False , ns = 2 )
		self.upLeg_seg_ikh = pm.rename ( self.upLeg_seg_ik_stuff[0] , self.side + "_upLeg_seg_ikh" )
		upLeg_seg_eff = pm.rename ( self.upLeg_seg_ik_stuff[1] , self.side + "_upLeg_seg_eff" )
		upLeg_seg_crv = pm.rename ( self.upLeg_seg_ik_stuff[2] , self.side + "_upLeg_seg_crv" )
		pm.select ( segJnts[self.legNumOfJnts+1] )
		pm.select ( segJnts[self.legNumOfJnts*2+1] , add = True )
		self.knee_seg_ik_stuff = pm.ikHandle ( sol = "ikSplineSolver" , parentCurve = False , ns = 2 )
		knee_seg_ikh = pm.rename ( self.knee_seg_ik_stuff[0] , self.side + "_knee_seg_ikh" )
		knee_seg_eff = pm.rename ( self.knee_seg_ik_stuff[1] , self.side + "_knee_seg_eff" )
		knee_seg_crv = pm.rename ( self.knee_seg_ik_stuff[2] , self.side + "_knee_seg_crv" )


		#============================================================================
		# creating curvy_midCtrl_jnt

		curvy_midCtrl_jnt = pm.joint ( p = ( self.kneePos[0] , self.kneePos[1] ,self.kneePos[2] ) , name = ( self.side + "_curvy_midCtrl_jnt" ) )

		# creating ctrl curve for curvy_midCtrl_jnt

		self.midCtrl = Circle8Crv ( self.legSize*1.2 , self.side+"_leg_toon_ctrl")
		pm.parent (self.midCtrl , self.midCtrlParent )
				
		self.midCtrl.rotate.set (0,0,0)
		self.midCtrl.translate.set (0,0,0) 

		pm.parent (curvy_midCtrl_jnt , self.midCtrl )
		curvy_midCtrl_jnt.jointOrient.set (0,0,0) 

		LockHideAttr ( objs=curvy_midCtrl_jnt , attrs="vv")

		LockHideAttr ( objs=self.midCtrl , attrs="sy")
		LockHideAttr ( objs=self.midCtrl , attrs="sz")
		LockHideAttr ( objs=self.midCtrl , attrs="v")

		
		#============================================================================
		# skinning the seg_crvs



		#==========
		# before skinning we should make sure that leg is completely staright.
		# we temporarly parent segmenty ikCurve to joint

		pm.parent ( knee_seg_crv , self.kneeJnt )

		if self.FKIKMode != "IK" :
			# tempKneeOri = pm.getAttr ( self.kneeJnt.jointOrient )
			tempKneeOri = self.kneeJnt.jointOrient.get()
			self.kneeJnt.jointOrient.set(0,0,0) 
		 
		else : # find position for putting the ik so that leg gets straight
			tempAnkleIKLoc = pm.spaceLocator ( p = (0,0,0) )
			pm.parent (tempAnkleIKLoc , self.upLegJnt  )
			tempAnkleIKLoc.rotate.set(0,0,0)
			legLen =   ( self.kneeJnt.translate.translateX.get() + self.ankleJnt.translate.translateX.get() )
			tempAnkleIKLoc.translate.set( legLen ,0,0)
			tempAnkleIKPos = pm.xform ( tempAnkleIKLoc , q=True , ws=True ,  translation = True )
			pm.parent (self.IKlegDistLocs[1], w=True)
			# straighten the leg for skinning
			self.IKlegDistLocs[1].translate.set( tempAnkleIKPos )



		#==========
		upLeg_seg_crv_skinCluster = ( pm.skinCluster( upLeg_seg_crv ,  self.upLegJnt , curvy_midCtrl_jnt , toSelectedBones = True ) )

		knee_seg_crv_skinCluster = ( pm.skinCluster( knee_seg_crv ,  curvy_midCtrl_jnt , self.kneeJnt , toSelectedBones = True ) )


		#==========
		pm.setAttr ( upLeg_seg_crv.tx ,  lock=False )
		pm.setAttr ( upLeg_seg_crv.ty ,  lock=False )
		pm.setAttr ( upLeg_seg_crv.tz ,  lock=False )

		pm.setAttr ( upLeg_seg_crv.rx ,  lock=False )
		pm.setAttr ( upLeg_seg_crv.ry ,  lock=False )
		pm.setAttr ( upLeg_seg_crv.rz ,  lock=False )
				
		pm.setAttr ( knee_seg_crv.tx ,  lock=False )
		pm.setAttr ( knee_seg_crv.ty ,  lock=False )
		pm.setAttr ( knee_seg_crv.tz ,  lock=False )

		pm.setAttr ( knee_seg_crv.rx ,  lock=False )
		pm.setAttr ( knee_seg_crv.ry ,  lock=False )
		pm.setAttr ( knee_seg_crv.rz ,  lock=False )


		pm.parent ( knee_seg_crv , w =True )

		pm.setAttr ( upLeg_seg_crv.tx ,  lock=True )
		pm.setAttr ( upLeg_seg_crv.ty ,  lock=True )
		pm.setAttr ( upLeg_seg_crv.tz ,  lock=True )

		pm.setAttr ( upLeg_seg_crv.rx ,  lock=True )
		pm.setAttr ( upLeg_seg_crv.ry ,  lock=True )
		pm.setAttr ( upLeg_seg_crv.rz ,  lock=True )
				
		pm.setAttr ( knee_seg_crv.tx ,  lock=True )
		pm.setAttr ( knee_seg_crv.ty ,  lock=True )
		pm.setAttr ( knee_seg_crv.tz ,  lock=True )

		pm.setAttr ( knee_seg_crv.rx ,  lock=True )
		pm.setAttr ( knee_seg_crv.ry ,  lock=True )
		pm.setAttr ( knee_seg_crv.rz ,  lock=True )


		if self.FKIKMode != "IK" :
			self.kneeJnt.jointOrient.set ( tempKneeOri )


		else:
			# now that we have skinned segmenty curves, we can put the leg to it's default pose
			pm.parent  ( self.IKlegDistLocs[1] , self.ankleIKCtrl  )
			self.IKlegDistLocs[1].translate.set( 0,0,0 )




		# setting the weights
		pm.skinPercent ( upLeg_seg_crv_skinCluster , (upLeg_seg_crv + ".cv[3:4]") , transformValue = ( curvy_midCtrl_jnt, 1)  )
		pm.skinPercent ( knee_seg_crv_skinCluster , (knee_seg_crv + ".cv[0:1]") , transformValue = ( curvy_midCtrl_jnt, 1)  )

		pm.skinPercent ( upLeg_seg_crv_skinCluster , (upLeg_seg_crv + ".cv[2]") , transformValue = ( curvy_midCtrl_jnt, 0.5)  )
		pm.skinPercent ( knee_seg_crv_skinCluster , (knee_seg_crv + ".cv[2]") , transformValue = ( curvy_midCtrl_jnt, 0.5)  )

		pm.skinPercent ( upLeg_seg_crv_skinCluster , (upLeg_seg_crv + ".cv[1]") , transformValue = ( curvy_midCtrl_jnt, 0.1)  )
		pm.skinPercent ( knee_seg_crv_skinCluster , (knee_seg_crv + ".cv[3]") , transformValue = ( curvy_midCtrl_jnt, 0.1)  )



		#============================================================================
		# making the joints stratchable 
			
		MakeSplineStretchy ( ikCrv=upLeg_seg_crv , stretchSwitch=True , volume=False , thicknessPlace="end")
		upLeg_seg_crv.inheritsTransform.set ( 0 ) 

		MakeSplineStretchy ( ikCrv=knee_seg_crv , stretchSwitch=True , volume=False ,thicknessPlace="start")
		knee_seg_crv.inheritsTransform.set ( 0 )


		#============================================================================
		# setting the twist parameters for the segmenty joints

		self.upLeg_seg_ikh.dTwistControlEnable.set ( 1 )
		self.upLeg_seg_ikh.dWorldUpType.set ( 4 )
		self.upLeg_seg_ikh.dWorldUpVectorX.set ( 1 )
		self.upLeg_seg_ikh.dWorldUpVectorY.set ( 0 )
		pm.connectAttr ( self.kneeJnt + ".worldMatrix[0]" , self.upLeg_seg_ikh + ".dWorldUpMatrixEnd" , f = True )

		knee_seg_ikh.dTwistControlEnable.set ( 1 )
		knee_seg_ikh.dWorldUpType.set ( 4 )
		pm.connectAttr ( self.kneeJnt + ".worldMatrix[0]" , knee_seg_ikh + ".dWorldUpMatrix" , f = True )
		pm.connectAttr ( self.ankleJnt + ".worldMatrix[0]" , knee_seg_ikh + ".dWorldUpMatrixEnd" , f = True )