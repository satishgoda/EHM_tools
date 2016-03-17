import pymel.core as pm

from codes.python.general import renamer
reload(renamer)
Renamer = renamer.Renamer

from codes.python.rig import jntOnCrv
reload(jntOnCrv)
JntOnCrv = jntOnCrv.JntOnCrv

from codes.python.rig import jntToCrv
reload(jntToCrv)
JntToCrv = jntToCrv.JntToCrv

from codes.python.rig import zeroGrp
reload(zeroGrp)
ZeroGrp = zeroGrp.ZeroGrp

from codes.python.rig import makeSplineStretchy
reload(makeSplineStretchy)
MakeSplineStretchy = makeSplineStretchy.MakeSplineStretchy

from codes.python.general import lockHideAttr
reload(lockHideAttr)
LockHideAttr = lockHideAttr.LockHideAttr


import pymel.core as pm
from functools import partial

class Spine():
	
	def __init__(self, *args, **kwargs):

		self.UI()
	
	def UI(self):
		width = 570
		height = 280
		# create window
		if pm.window( 'ehm_Spine_UI', exists=True ):
			pm.deleteUI( 'ehm_Spine_UI' )
		pm.window( 'ehm_Spine_UI', title='Rig Spine', w=width, h=height, mxb=False, mnb=False, sizeable=True )
		
		# main layout
		baseForm = pm.formLayout()
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'left', 6) )
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'right', 6) )
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'top', 6) )
		pm.formLayout( baseForm, edit=True, attachForm=(frameLayout,'bottom', 38) )
		# pm.scrollLayout( horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
		formLayout = pm.formLayout(w=width, h=height)
		
	

		# name of spine
		self.limbNameT = pm.text( label="Limb Name: ")			
		self.limbNameTF = pm.textField( text="spine")
	
		# spine size
		self.spineSizeT = pm.text( label="Spine Size: ")	
		self.spineSizeF = pm.floatSliderGrp(adjustableColumn=4,min=0, max=20, fieldMaxValue=10000, value=5, field=True )

		
		# character mode radio buttons
		self.characterModeText = pm.text(label='Character Mode: ', align='right')
		self.characterModeRC = pm.radioCollection()
		self.bipedRB = pm.radioButton(label="Biped", select=True )
		self.quadrupedRB = pm.radioButton(label="Quadruped")


		# number of init joints
		self.numOfInitJntsText = pm.text( label='Number of Initial joints: ', align='right')		
		self.numOfInitJntsIS = pm.intSliderGrp( field=True, value=4, maxValue=10, fieldMaxValue=1000 )
		
		# number of FK controls
		self.numOfFKctrlText = pm.text( label='Number of FK Controls: ', align='right')		
		self.numOfFKctrlIS = pm.intSliderGrp( field=True, value=2, maxValue=10, fieldMaxValue=1000 )
		
		# number of init joints
		self.numOfJntsText = pm.text( label='Number of joints: ', align='right')		
		self.numOfJntsIS = pm.intSliderGrp( field=True, value=6, maxValue=20, fieldMaxValue=1000 )		
		
		# extras check boxes
		self.extrasText = pm.text( label='Extras: ', align='right' )		
		self.ssCB = pm.checkBox( label="Squash Stretch", value=True )	
		self.volumeCB = pm.checkBox( label="Preserve Volume", value=True )	
		self.stretchSwitchCB = pm.checkBox( label="Create Stretch Switch On Spline Curve", value=True )	
		self.midCtrlCB = pm.checkBox( label="MidCtrl", value=True )

		
		
		# buttons
		self.initButton = pm.button( label='Place joints',  h=30,  c=partial( self.spine_init, 5.0, 'spine', 'biped', 4 ), parent=baseForm  )
		self.packButton = pm.button( label='Finish Rig', h=30,  c=partial( self.spine_pack, 5.0, 'spine', 'biped', 4 , None, False, True, True, True, None, 3 ), parent=baseForm    )		
		self.closeButton = pm.button( label='Close', h=30,  c= self.closeUI , parent=baseForm    )		

		# place limb name
		pm.formLayout( formLayout, edit=True, attachPosition=(self.limbNameT,'right', 0, 28 ) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.limbNameT,'top', 17 ) )
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.limbNameTF,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.limbNameTF,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.limbNameTF,'top', 15 ) )		
		
		# place spine size
		pm.formLayout( formLayout, edit=True, attachPosition=(self.spineSizeT,'right', 0, 28 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.spineSizeT,'top', 15, self.limbNameT ) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.spineSizeF,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.spineSizeF,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.spineSizeF,'top', 12, self.limbNameT ) )	
		
		# place character mode
		pm.formLayout( formLayout, edit=True, attachPosition=(self.characterModeText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.characterModeText,'top', 17, self.spineSizeT) )
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.bipedRB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.bipedRB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.bipedRB,'top', 15, self.spineSizeT) )		

		pm.formLayout( formLayout, edit=True, attachPosition=(self.quadrupedRB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.quadrupedRB,'right', 15, 100 ) )
		
		pm.formLayout( formLayout, edit=True, attachControl=(self.quadrupedRB,'top', 35, self.spineSizeT) )	


		# place number of joints
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfInitJntsText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfInitJntsText,'top', 37, self.characterModeText) )
	
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfInitJntsIS,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfInitJntsIS,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfInitJntsIS,'top', 32, self.characterModeText ) )	
			

		# place number of joints
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfJntsText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfJntsText,'top', 17, self.numOfInitJntsText) )
	
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfJntsIS,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfJntsIS,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfJntsIS,'top', 12, self.numOfInitJntsText ) )	

		# placee number of FK controls
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfFKctrlText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfFKctrlText,'top', 17, self.numOfJntsText) )
	
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfFKctrlIS,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.numOfFKctrlIS,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.numOfFKctrlIS,'top', 12, self.numOfJntsText ) )	
		
		
		# place check boxes
		pm.formLayout( formLayout, edit=True, attachPosition=(self.extrasText,'right', 0 , 28) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.extrasText,'top', 17, self.numOfFKctrlText) )
	
		pm.formLayout( formLayout, edit=True, attachPosition=(self.ssCB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.ssCB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.ssCB,'top', 15, self.numOfFKctrlText ) )	
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.volumeCB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.volumeCB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.volumeCB,'top', 35, self.numOfFKctrlText ) )	

		pm.formLayout( formLayout, edit=True, attachPosition=(self.stretchSwitchCB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.stretchSwitchCB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.stretchSwitchCB,'top', 55, self.numOfFKctrlText ) )	

		pm.formLayout( formLayout, edit=True, attachPosition=(self.midCtrlCB,'left', 0, 30 ) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.midCtrlCB,'right', 15, 100 ) )
		pm.formLayout( formLayout, edit=True, attachControl=(self.midCtrlCB,'top', 75, self.numOfFKctrlText ) )	

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
		pm.showWindow( 'ehm_Spine_UI' )

	
	def closeUI( self, *args ):
		pm.deleteUI( 'ehm_Spine_UI' )								

	
	
	#========================================================================================================
	# make initial joints for starting the rig

	def spine_init ( self, size=5.0, limbName='spine', mode='biped', numOfJnts=4 , *args ):
		
		self.spine_initJnts=[]
		self.tmpCrv = None
		
		try:# if in UI mode, get number of joints from UI
			size = pm.floatSliderGrp( self.spineSizeF, q=True, value=True)
			limbName = pm.textField( self.limbNameTF, q=True, text=True)
			selectedMode = pm.radioCollection( self.characterModeRC, q=True, select=True)
			mode = pm.radioButton( selectedMode, q=True, label=True ).lower()
			numOfJnts = pm.intSliderGrp( self.numOfInitJntsIS, q=True, value=True)
		except:
			pass

		curveCVs=[]
		curveCVsCount=[]
		for i in range(numOfJnts):
			pm.select (clear=True)

			if mode=='biped':
				jntPos = ( 0, size+(size*1.0/(numOfJnts-1)*i), 0 )
			elif mode=='quadruped':
				jntPos = ( 0, size, (size*1.0/(numOfJnts-1)*i)-size/2.0 )
			else:
				pm.error('ehm_tools...Spine: mode arg accepts "biped" or "quadruped" only!')

			self.spine_initJnts.append(  pm.joint ( p = jntPos , name = "%s_%s_initJnt"%(limbName,i+1) )  )
			curveCVs.append( jntPos )
			curveCVsCount.append( i )

		self.tmpCrv = pm.curve( d=1, p=curveCVs , k=curveCVsCount )
		self.tmpCrv.getShape().template.set(True)
		pm.skinCluster( self.spine_initJnts,self.tmpCrv)	


	#========================================================================================================
	# use initJnts to create the final rig

	def spine_pack ( self
						, size=5.0
						, limbName='spine'
						, mode='biped'
						, numOfJnts=4 
						, mainCtrl=None
						, midCtrl=False
						, ss=True
						, stretchSwitch=True
						, volume=True
						, numOfFKctrl=None
						, numOfSpans=3 
						, *args ):
		
		try:# if in UI mode, get number of joints from UI
			size = pm.floatSliderGrp( self.spineSizeF, q=True, value=True)
			limbName = pm.textField( self.limbNameTF, q=True, text=True)
			selectedMode = pm.radioCollection( self.characterModeRC, q=True, select=True)
			mode = pm.radioButton( selectedMode, q=True, label=True ).lower()
			numOfJnts = pm.intSliderGrp( self.numOfJntsIS, q=True, value=True)
			numOfFKctrl = pm.intSliderGrp( self.numOfFKctrlIS, q=True, value=True )
			ss = pm.checkBox( self.ssCB, q=True, value=True )	
			volume = pm.checkBox( self.volumeCB, q=True, value=True )
			stretchSwitch = pm.checkBox( self.stretchSwitchCB, q=True, value=True )
			midCtrl = pm.checkBox( self.midCtrlCB, q=True, value=True )			
		except:
			pass	
		
		# create spine curve and it's joints 	
		crv = pm.duplicate( self.tmpCrv, name=('%s_crv'%limbName) )[0]
		crv.getShape().template.set(False)
		pm.rebuildCurve( crv, ch=False, s=numOfSpans )
		jnts = (JntOnCrv( numOfJnts=numOfJnts, crv=crv )).newJnts

		Renamer( objs=jnts , name="%s_###_jnt"%limbName )


		# orient spine joints 
		pm.joint( jnts[0],  e=True, oj='xzy', secondaryAxisOrient='xup', ch=True, zso=True )



		# create joints which will drive the spine curve
		if not midCtrl: # create base and end control joints
			controlJnts = (JntOnCrv( crv=crv , numOfJnts=2 )).newJnts
			startJnt  = pm.rename(controlJnts[0],'hip_ctrl' )
			endJnt    = pm.rename(controlJnts[1],'torso_ctrl' )
			pm.parent(  endJnt , world=True )

		else: # create base, end and middle control joint
			controlJnts = (JntOnCrv( crv=crv , numOfJnts=3 )).newJnts
			startJnt  = pm.rename(controlJnts[0],'hip_ctrl' )
			midJnt    = pm.rename(controlJnts[1],'mid_ctrl' )
			endJnt    = pm.rename(controlJnts[2],'torso_ctrl' )
			pm.parent( midJnt, endJnt , world=True )


		# orient control joints
		for jnt in controlJnts:
			if mode=='biped':
				jnt.jointOrient.set(90,0,90)
			elif mode=='quadruped':
				jnt.jointOrient.set(180,-90,0)	

		# remove init joints and curve
		pm.delete( self.tmpCrv, self.spine_initJnts )

		
		# create body control
		body_ctrl = (pm.curve ( d = 1 , p = [ (0, -size*.3 ,  size*.3)
											, (0, -size*.3 , -size*.3)
											, (0,  size*.3 , -size*.3)
											, (0,  size*.3 ,  size*.3)
											, (0, -size*.3 ,  size*.3) ]
							, k = [ 0 , 1 , 2 , 3 , 4 ] 
							, name = 'body_ctrl'
							) )
		body_ctrl.getShape().overrideEnabled.set(True)	
		body_ctrl.getShape().overrideColor.set(17)	
		pm.xform( body_ctrl, ws=True, t=pm.xform(startJnt, q=True, ws=True, t=True) )
		pm.xform( body_ctrl, ws=True, ro=pm.xform(startJnt, q=True, ws=True, ro=True) )
			

		# create IK controls 
		JntToCrv( jnts=controlJnts, shape='circle', size=size*0.25 )
		for jnt in controlJnts:
			jnt.overrideEnabled.set(True)
			jnt.overrideColor.set(17)	

		IKzeroGrps = ZeroGrp( objs=controlJnts )

		# create FK controls 
		if numOfFKctrl :
			fkCtrls = [] 		
			for i in range(numOfFKctrl):
				fkCtrls.append( (pm.circle( c=(0,0,0), nr=(1,0,0), r=size*0.25, name = "%s_FK_%s)ctrl"%(limbName,i) ) )[0]  )
				fkCtrls[i].getShape().overrideEnabled.set(True)	
				fkCtrls[i].getShape().overrideColor.set(18)	
				pm.xform( fkCtrls[i], ws=True, t=pm.xform(startJnt, q=True, ws=True, t=True) )
				moveAmount = size*0.07+(size/float(numOfFKctrl)*i)
				if mode=='biped':
					pm.move( fkCtrls[i], (0,moveAmount,0), r=True )
					pm.rotate( fkCtrls[i], (90,0,90)  , r=True )
				elif mode=='quadruped':
					pm.move( fkCtrls[i], (0,0,moveAmount), r=True )
					pm.rotate( fkCtrls[i], (180,-90,0), r=True )			

			pm.parent ( IKzeroGrps[0][-1] , fkCtrls[-1] )

			for i in range(numOfFKctrl-1):
				fkCtrls[i+1].setParent( fkCtrls[i] )

			fkCtrlsZeroGrps = ZeroGrp( objs=fkCtrls[0] )


		# keep mid control between first and last joints
		if midCtrl:
			startNull= pm.group(em=True,name='%s_start_null'%limbName)
			endNull= pm.group(em=True,name='%s_end_null'%limbName)
			startNull.setParent( startJnt )
			endNull.setParent( endJnt )
			pm.xform( startNull, t=(size*.3,0,0), ro=(0,0,0), os=True )
			pm.xform( endNull, t=(-size*.3,0,0), ro=(0,0,0), os=True )
			pm.pointConstraint( startNull, endNull, IKzeroGrps[0][1] )
			midOriNull= pm.group(em=True,name='%s_midOrient_null'%limbName)
			pm.pointConstraint( startJnt, midOriNull )
			pm.aimConstraint( endJnt, midOriNull, aimVector=(1,0,0), worldUpType="none")
			midOriNull.rotate >> IKzeroGrps[0][1].rotate		


		# parent FK, IK and mid cotrol to body
		if midCtrl and numOfFKctrl:
			pm.parent( fkCtrlsZeroGrps[0], midOriNull, IKzeroGrps[0][:-1], body_ctrl )
		elif numOfFKctrl:
			pm.parent( fkCtrlsZeroGrps[0], IKzeroGrps[0][:-1], body_ctrl )

		elif midCtrl:
			pm.parent( midOriNull, IKzeroGrps[0], body_ctrl )
		else:
			pm.parent( IKzeroGrps[0], body_ctrl )

		bodyCtrlZeroGrp = ZeroGrp( objs=body_ctrl )


		# lock and hide extra attributes
		if numOfFKctrl:
			for i in range(numOfFKctrl):
				LockHideAttr(objs=fkCtrls[i],attr='t')
				LockHideAttr(objs=fkCtrls[i],attr='s')
				LockHideAttr(objs=fkCtrls[i],attr='v')


		# create ik spline handle
		ikhStuff = pm.ikHandle ( solver = "ikSplineSolver" , startJoint = jnts[0]  , endEffector = jnts[-1] , curve=crv, freezeJoints=True, simplifyCurve = True, numSpans=numOfSpans  )  #, createCurve = False, rootOnCurve = True 

		if midCtrl:
			skinClust = pm.skinCluster( ikhStuff[2], startJnt , midJnt , endJnt)
		else:
			skinClust = pm.skinCluster( ikhStuff[2], startJnt ,  endJnt)

		
		# set skin weights for ik spline curve
		if midCtrl and numOfSpans==3:
			pm.skinPercent( skinClust , crv.cv[1], transformValue=[(startJnt, 0.8),(midJnt, 0.2)] )
			pm.skinPercent( skinClust , crv.cv[3], transformValue=[(midJnt, 0.8),(endJnt, 0.2)] )


		# rename IK stuff
		pm.rename (ikhStuff[0], "%s_ikh"%limbName )
		pm.rename (ikhStuff[1], "%s_eff"%limbName )
		ikCrv = pm.rename (ikhStuff[2], "%s_crv"%limbName )


		# outliner cleaup and hide extra objects
		pm.group( ikhStuff[::2],jnts[0], name='%s_skinJnts_grp'%limbName )
		pm.setAttr ( ikhStuff[2] + ".inheritsTransform" , 0 )
		LockHideAttr( objs=ikhStuff[::2],attr='vv')


		# stretchable back if ss in ON
		if ss :
			MakeSplineStretchy( ikCrv=crv, volume=True, stretchSwitch=True, thicknessPlace="mid" )
		pm.select (clear=True)
		
		# clean memory
		del ( self.spine_initJnts )
		del ( self.tmpCrv )
