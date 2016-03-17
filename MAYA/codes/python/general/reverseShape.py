# reverses the shape of selected object in the specified direction
#-----------------------------------------------------------------------------------------------------------------

import pymel.core as pm

import pymel.core as pm
from functools import partial
# from ehm_tools.codes.rig import zeroGrp
# from ehm_tools.codes.curves.sphereCrv import SphereCrv
# from ehm_tools.codes.curves.cubeCrv import CubeCrv
# from ehm_tools.codes.curves.circle8Crv import Circle8Crv


class ReverseShape():
	
	def __init__(self, *args, **kwargs):
			
		if args or kwargs:
			self.reverseShape(*args, **kwargs)
		else:
			self.UI()	
	
	def UI(self):
		
		# create window
		if pm.window( 'ehm_ReverseShape_UI', exists=True ):
			pm.deleteUI( 'ehm_ReverseShape_UI' )
		pm.window( 'ehm_ReverseShape_UI', title='Reverse shape', w=300, h=80, mxb=False, mnb=True, sizeable=True )

		
		# main layout
		#mainLayout = pm.rowColumnLayout()
		formLayout = pm.formLayout(w=300, h=80)
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)
		pm.setParent( formLayout )
		
		# radio buttons
		self.AxisText = pm.text(label='Axis: ', align='right')
		self.AxisRC = pm.radioCollection()
		self.xRB = pm.radioButton(label="x", select=True )
		self.yRB = pm.radioButton(label="y")
		self.zRB = pm.radioButton(label="z")

		
		# buttons
		self.applyButton = pm.button( label='Apply',  h=30,  c= partial( self.reverseShape, None, 'x'  ) )
		
		
		# place frame layout
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'left', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'right', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'bottom', 38) )


		# place radio buttons
		#pm.formLayout( formLayout, edit=True, attachPosition=(self.AxisText,'left', 5, 0) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.AxisText,'right', 0 , 25) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.AxisText,'top', 17) )
		
		#pm.formLayout( formLayout, edit=True, attachPosition=(self.xRB,'left', 5, 25) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.xRB,'right', 10 , 50) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.xRB,'top', 15) )		

		#pm.formLayout( formLayout, edit=True, attachPosition=(self.yRB,'left', 5, 50) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.yRB,'right', 10, 75) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.yRB,'top', 15) )	

		#pm.formLayout( formLayout, edit=True, attachPosition=(self.zRB,'left', 5, 75) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.zRB,'right', 20 , 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.zRB,'top', 15) )	

		# place buttons
		pm.formLayout( formLayout, edit=True, attachPosition=(self.applyButton,'left', 4, 25) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.applyButton,'right', 2 , 75) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.applyButton,'bottom', 5) )
				
				
		# show window
		pm.showWindow( 'ehm_ReverseShape_UI' )


	def reverseShape( self, objs=None, axis='x', *args ):
				
		try:
			selectedItem = pm.radioCollection( self.AxisRC, q=True, select=True )
			axis = (pm.radioButton( selectedItem, q=True, label=True )).lower()
		except:
			pass
		
		
		scaleValue = ( -1, 1, 1 )
		if axis == 'y':
			scaleValue = ( 1, -1, 1 )
		elif axis == 'z':
			scaleValue = ( 1, 1, -1 )
		elif axis != 'x':
			pm.warning('Axis was not correct, used "x" axis instead.')
		
		if objs == None:
			objs = pm.ls( sl=True )
		else:
			objs = pm.ls( objs )
		
		for obj in objs:
			try:
				shape = obj.getShape()
				if shape.type() == 'mesh':
					pm.select( shape.vtx[:] )
					pm.scale( scaleValue )
					pm.select( objs )
				elif shape.type() == 'nurbsCurve':
					pm.select( shape.cv[:] )
					pm.scale( scaleValue )
					pm.select( objs )			
			except:
				pm.warning("Object doesn't have a shape. Skipped!")

			'''
			else:
				pm.warning('general.reverseShape() : %s is not a mesh or curve, skipped.' %( obj ) )     
			'''