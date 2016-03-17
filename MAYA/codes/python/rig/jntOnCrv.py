# ---------------------------------------------------------------------------------
# synopsis : 			jntOnCrv ( )
#
# what does this script do ?	 creates joints on a curve
#
# flags :				crv 		=>  nurbsCurvs
#						numOfJnts	=>  number of joints.
#
# how to usse:        jntOnCrv( curve1 , 20 )
#
# ---------------------------------------------------------------------------------

import pymel.core as pm
from functools import partial

class JntOnCrv():
	
	def __init__(self, *args, **kwargs):
	
		self.newJnts = []
	
		if args or kwargs:
			self.jntOnCrv(*args, **kwargs)
		else:
			self.UI()
	
	def UI(self):
		
		# create window
		if pm.window( 'ehm_JntOnCrv_UI', exists=True ):
			pm.deleteUI( 'ehm_JntOnCrv_UI' )
		pm.window( 'ehm_JntOnCrv_UI', title='create joint on curve', w=250, h=100, mxb=False, mnb=False, sizeable=False )
		
		# main layout
		mainLayout = pm.columnLayout(w=250, h=100)
		formLayout = pm.formLayout(w=250, h=100 )
		
		# num of joints slider
		self.slider = pm.intSliderGrp( label='num of joints: ',value=6, minValue=2,maxValue=20,fieldMaxValue=10000, h=50, field=True,columnWidth=([1,70], [2,50], [3,70] )   )
		
		# button
		button = pm.button( label='apply', w=200, h=40,  c=partial( self.jntOnCrv, 5 , None )  )
		
		# place controls
		pm.formLayout( formLayout, edit=True, attachForm=(self.slider,'left', 10) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.slider,'right', 10) )
		
		pm.formLayout( formLayout, edit=True, attachForm=(button,'left', 10) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'right', 10) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'bottom', 10) )
		pm.formLayout( formLayout, edit=True, attachControl=(button,'top', 0, self.slider ) )
		
		
		# show window
		pm.showWindow( 'ehm_JntOnCrv_UI' )


	def jntOnCrv( self, numOfJnts=5, crv=None, *args):

		try:# if in UI mode, get number of joints from UI
			numOfJnts = pm.intSliderGrp( self.slider,q=True,value=True)
		except:
			pass

		if crv==None:
			try:
				crv = pm.ls(sl=True)[0]
			except:
				pm.warning( 'ehm_tools...JntOnCrv: Select a curve to create joints on it.' )
				return None
		if numOfJnts < 2 :
			pm.warning( "number of joints must be greater than 1.")
			return None
		try:
			curveShape = crv.getShape().type()
		except:
			pm.warning( "specified object is not a curve.")
			return None			

		if curveShape != 'nurbsCurve' :
			pm.warning( "specified object is not a curve.")		
			return None

		crv = pm.duplicate(crv)[0]
		pm.rebuildCurve (crv , ch=False ,rpo=True ,rt=0 ,end=1 ,kr=0 ,kcp=False ,kep=True ,kt=0 , s=200 , d=1 , tol=0.01 )
		crvShape = crv.getShape()

		pm.select(clear=True)
		segSize = 1.0/ (numOfJnts-1)
		
		for i in range(numOfJnts):
			pos = crvShape.getPointAtParam(segSize*i, 'world')
			self.newJnts.append( pm.joint(p=pos) )
		
		pm.delete(crv)
