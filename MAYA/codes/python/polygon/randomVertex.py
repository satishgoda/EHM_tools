import pymel.core as pm
import random as random

def RandomVertex( objs = None, displace = 0.5 ):
	
	if objs==None:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	for obj in objs:
		
		shape = obj.getShape()
		numOfVtxs = pm.polyEvaluate( shape, vertex=True )
		
		for i in range( numOfVtxs ):

			currentDisp = random.uniform( -displace , displace )
			axis =  random.randint( 0 , 2 )
			if axis == 0:
				shape.vtx[i].translateBy( (currentDisp,0,0) )
			if axis == 1:
				shape.vtx[i].translateBy( (0,currentDisp,0) )
			if axis == 2:
				shape.vtx[i].translateBy( (0,0,currentDisp) )