import pymel.core as pm
from functools import partial

from codes.python.rig import findPosBetween
FindPosBetween = findPosBetween.FindPosBetween

class DivideJnt():

	def __init__(self, *args, **kwargs):
	
		self.newJnts=[]
		if args or kwargs:
			self.divideJnt(*args, **kwargs)
		else:
			self.UI()
			
	
	def UI(self):
		
		# create window
		if pm.window( 'ehm_DivideJnt_UI', exists=True ):
			pm.deleteUI( 'ehm_DivideJnt_UI' )
		pm.window( 'ehm_DivideJnt_UI', title='Divide Joint', w=250, h=100, mxb=False, mnb=False, sizeable=False )
		
		# main layout
		mainLayout = pm.columnLayout(w=250, h=100)
		formLayout = pm.formLayout(w=250, h=100 )
		
		# num of joints slider
		self.slider = pm.intSliderGrp( label='num of joints: ',value=6, minValue=2,maxValue=20,fieldMaxValue=10000, h=50, field=True,columnWidth=([1,70], [2,50], [3,70] )   )
		
		# button
		button = pm.button( label='apply', w=200, h=40,  c=partial( self.divideJnt, None, 5 )  )
		
		# place controls
		pm.formLayout( formLayout, edit=True, attachForm=(self.slider,'left', 10) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.slider,'right', 10) )
		
		pm.formLayout( formLayout, edit=True, attachForm=(button,'left', 10) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'right', 10) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'bottom', 10) )
		pm.formLayout( formLayout, edit=True, attachControl=(button,'top', 0, self.slider ) )
		
		
		# show window
		pm.showWindow( 'ehm_DivideJnt_UI' )

		
	def divideJnt ( self, jnt=None , numOfDivisions=5, *args, **kwargs ):

		if jnt==None:
			jnt = pm.ls(sl=True)[0]

		try:# if in UI mode, get number of joints from UI
			numOfDivisions = pm.intSliderGrp( self.slider,q=True,value=True)
		except:
			pass

		if jnt.type() != 'joint':
			pm.error("%s is not a joint." %(jnt.name()) )

		if numOfDivisions <= 0 :
			pm.error("numOfDivisions must be bigger than zero.")


		self.newJnts.append(jnt)

		radi = jnt.radius.get()

		children = jnt.getChildren()
		if len(children) < 1:
			pm.error("Selected joint must have a child joint.")
		else:
			child = children[0]


		percentage = 0.0
		incrementPercent = 100.0 / numOfDivisions

		pm.select( jnt )
		for  i in ( range(numOfDivisions-1) ) :
			percentage += incrementPercent
			pos = FindPosBetween( percent = percentage, base=jnt, tip=child )

			currentJnt = pm.joint ( p = pos )
			pm.setAttr( currentJnt.radius, radi )
			self.newJnts.append ( currentJnt  )
		
		pm.parent( child, self.newJnts[ -1 ] )
		self.newJnts.append(child)