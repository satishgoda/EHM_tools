# blendAttrs
# blends A and B by the amount of blender, connects them to C.
# needs four attributes.
#============================================================

import pymel.core as pm

def BlendAttrs( A=None, B=None, C=None, blender=None  ):
	
	result_bln = pm.createNode ( "blendColors", n =  "_bln"    )

	if A==0:
		result_bln.color1R.set( 0 )
	elif A==1:
		result_bln.color1R.set( 1 )
	else:	
		A					>>		result_bln.color1

	
	if B==0 :
		result_bln.color2R.set( 0 )
	elif B==1:
		result_bln.color2R.set( 1 )
	else:
		B					>>		result_bln.color2 

	
	if blender:
		blender				>>		result_bln.blender 

	
	if A==0 or A==1 or B==0 or B==1:
		result_bln.outputR		>>	C
	else:
		result_bln.output		>>	C
	
	
	return result_bln