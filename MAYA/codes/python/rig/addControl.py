# ---------------------------------------------------------------------------------
# synopsis :
#              addControl( createZeroGroup, dist )
#
# what does this method do ?
#       			create control curves for selected objects
#
# flags :
#                        createZeroGroup, (boolean)   =>  whether create empty groups for the controls or not
#
#                        dist, (float)   =>  size of the controls
#
#
# how to use:       select objects and and run this
#                             	import sys
# 								sys.path.append( r"D:\all_works\MAYA_DEV\EHM_tools\MAYA" ) 
# 								import codes
# 								from codes.python.rig import addControl
# 								reload( addControl )
# 								addControl.AddControl(createZeroGroup=True , size=1.0, shape='circle')
#
# return :        newly created controls
#
#
# version notes:
#	2016-03-12	ehassani	use parentConstraint instead of parent
#
#
# bugs : # DeprecationWarning: The function 'pymel.core.general.PyNode.__getitem__' is deprecated and will become unavailable in future pymel versions. Convert to string first using str() or PyNode.name(), at line 248, in "C:\Program Files\Autodesk\Maya2012\bin\maya.exe"
# ---------------------------------------------------------------------------------

import pymel.core as pm
from functools import partial
from codes.python.rig import zeroGrp
reload( zeroGrp )
ZeroGrp = zeroGrp.ZeroGrp 
from codes.python.curve.sphereCrv import SphereCrv
from codes.python.curve.cubeCrv import CubeCrv
from codes.python.curve.circle8Crv import Circle8Crv


class AddControl():
	def __init__(self, *args, **kwargs):
	
		self.ctrls = []
	
		if args or kwargs:
			self.addControl(*args, **kwargs)
		else:
			self.UI()	
	
	def UI(self):
		
		# create window
		if pm.window( 'ehm_AddControl_UI', exists=True ):
			pm.deleteUI( 'ehm_AddControl_UI' )
		pm.window( 'ehm_AddControl_UI', title='Create Control For Objects', w=280, h=100, mxb=False, mnb=False, sizeable=False )
		
		# main layout
		mainLayout = pm.columnLayout(w=280, h=130)
		formLayout = pm.formLayout(w=270, h=120)
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)	
		pm.setParent( formLayout )
		
		# num of joints slider
		self.shapeType = pm.optionMenuGrp(  label='shape type: '
												, h=30
												, columnAttach2=('left','left')
												, columnOffset2=(20,0)
												, columnWidth2=(90,60)	)												
		pm.menuItem(label="sphere")
		pm.menuItem(label="cube")
		pm.menuItem(label="circle")
		
		# size of shapes
		self.sizeSlider = pm.floatSliderGrp( label='shape size: '
												, value=1
												, minValue=0.0
												, maxValue=20
												, fieldMaxValue=10000, h=30, field=True
												, columnAttach3=('left','left','left' )
												, columnOffset3=(20,0,0 )
												, columnWidth3=(80,60,120)   )
	
		# button
		button = pm.button( label='apply', w=100, h=30,  c=partial( self.addControl, None, 1.0 , 'sphere' )  )
		
		# place controls
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'left', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'right', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'bottom', 38) )
				
		
		pm.formLayout( formLayout, edit=True, attachForm=(self.shapeType,'left', 0) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.shapeType,'top', 8) )
		
		pm.formLayout( formLayout, edit=True, attachForm=(self.sizeSlider,'left', 5) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.sizeSlider,'top', 40) )
				
		
		pm.formLayout( formLayout, edit=True, attachForm=(button,'left', 5) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'right', 5) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'bottom', 5) )
		
		
		# show window
		pm.showWindow( 'ehm_AddControl_UI' )


	def addControl( self, objsToPutCtrlOn=None, createZeroGroup=False , size=1.0, shape='sphere', *args ):

		self.ctrls = [] # ctrls names for return

		if not objsToPutCtrlOn:
			objsToPutCtrlOn =  pm.ls ( sl = True )
		
		
		try:# if in UI mode, get info from UI
			shape =  pm.optionMenuGrp( self.shapeType, q=True,  value= True  )
			size = pm.floatSliderGrp( self.sizeSlider, q=True,  value= True  )
		except:
			pass	
		
		
		shapeCmd = { 'sphere': SphereCrv
					,'cube'  : CubeCrv
					,'circle': Circle8Crv
					}
		
		# for every selected object create ctrl curve

		for i in range (len(objsToPutCtrlOn)):
		
	
			objToPutCtrlOn = objsToPutCtrlOn[i]
			
			ctrl = shapeCmd[shape]( size=size,  name = "%s_ctrl" %objToPutCtrlOn  )
			
			'''
			# create circle, find the proper name for the contorl curve and name the circle
			if str(objToPutCtrlOn)[-3:] == "jnt":
				pm.rename( ctrl , objToPutCtrlOn.name().replace("jnt", "ctrl") )
			else:
				pm.rename( ctrl , objToPutCtrlOn.name() + "_ctrl" )
			'''

			# parent curve to corisponding joint
			pm.parent( ctrl, objToPutCtrlOn )

			#reset tranform values on circles
			pm.xform (ctrl , t = (0,0,0) , ro= (0,0,0))

			firstParent = pm.listRelatives ( objToPutCtrlOn , fullPath = True , parent = True )

			# parent ctrls to their firstgrandparent
			if firstParent  :
				pm.parent ( ctrl , firstParent[0] )
			else :
				pm.parent ( ctrl , world = True  )


			pm.parentConstraint ( ctrl, objToPutCtrlOn )

			self.ctrls.append ( ctrl )
			



		# create zero groups if needed - add zero groups as well to return value
		if createZeroGroup == True:
			pm.select (self.ctrls)
			self.ctrls.extend (  ZeroGrp()  )


