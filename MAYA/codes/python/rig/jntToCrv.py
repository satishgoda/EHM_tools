import pymel.core as pm
from functools import partial
from codes.python.curves.sphereCrv import SphereCrv
from codes.python.curves.cubeCrv import CubeCrv
from codes.python.curves.circle8Crv import Circle8Crv

from codes.python.general import dist
Dist = dist.Dist


class JntToCrv():
	def __init__(self, *args, **kwargs):
	
		self.newShapes = []
	
		if args or kwargs:
			self.jntToCrv(*args, **kwargs)
		else:
			self.UI()	
	
	def UI(self):
		
		# create window
		if pm.window( 'ehm_JntToCrv_UI', exists=True ):
			pm.deleteUI( 'ehm_JntToCrv_UI' )
		pm.window( 'ehm_JntToCrv_UI', title='Create Curve Shape On Joints', w=270, h=100, mxb=False, mnb=False, sizeable=False )
		
		# main layout
		mainLayout = pm.columnLayout(w=270, h=130)
		formLayout = pm.formLayout(w=260, h=120)
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
												, columnWidth3=(80,50,80)   )
	
		# button
		button = pm.button( label='apply', w=100, h=30,  c=partial( self.jntToCrv, None, 1.0 , 'sphere' )  )
		
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
		pm.showWindow( 'ehm_JntToCrv_UI' )

	def jntToCrv ( self, jnts=None, size=1.0, shape='sphere', *args ):

		if not jnts:
			try:
				jnts = pm.ls(sl=True)
			except:
				pass
		if not jnts:
			pm.warning('ehm_tools...JntToCrv: select joints to create control curve for them.')
		
		else:
			jnts = pm.ls( jnts )
			
		try:# if in UI mode, get info from UI
			shape =  pm.optionMenuGrp( self.shapeType, q=True,  value= True  )
			size = pm.floatSliderGrp( self.sizeSlider, q=True,  value= True  )
		except:
			pass		

		shapeCmd = { 'sphere': SphereCrv
					,'cube'  : CubeCrv
					,'circle': Circle8Crv
					}
		self.newShapes = []
		

		for jnt in jnts:
			# if not (jnt.type()=='joint') :
				# pm.warning('ehm_tools...JntToCrv: %s is not a joint, skipped!'% jnt)
			# else:
			currentCircle = shapeCmd[shape]( size=size )
			shapeNode = currentCircle.getShape()
			pm.select ( shapeNode , jnt )
			pm.parent ( add = True  , shape = True )
			pm.delete (currentCircle)
			self.newShapes.append( jnt.getShape() )