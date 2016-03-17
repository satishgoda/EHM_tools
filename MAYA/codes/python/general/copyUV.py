# copyUV()
import pymel.core as pm

def copyUV( objs=None ):
	
	if not objs:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )
	
	if len( objs ) < 2:
		return None
	
	for i in range( len( objs )-1 ):
		pm.select( objs[-1] )
		pm.select( objs[i], add=True )
		pm.transferAttributes(
				transferPositions= 0 
				,transferNormals=0 
				,transferUVs=2 
				,transferColors=2 
				,sampleSpace=4 
				,sourceUvSpace="map1" 
				,targetUvSpace="map1" 
				,searchMethod=3
				,flipUVs=0 
				,colorBorders=1 )

