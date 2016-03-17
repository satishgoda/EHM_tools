import pymel.core as pm

def SphereCrv( size=0.5, name='sphereCrv') :
	
	ctrlName =  pm.curve (d = 1 , p =  ( 
											( 0 , 1 , 0 ),
											( -0.382683, 0.92388, 0),
											( -0.707107, 0.707107, 0 ),
											( -0.92388, 0.382683, 0 ),
											( -1 ,0 ,0 ),
											( -0.92388, -0.382683, 0 ),
											(  -0.707107, -0.707107, 0 ),
											(  -0.382683, -0.92388, 0),
											( 0 ,-1, 0  ),
											( 0.382683, -0.92388, 0),
											(  0.707107, -0.707107, 0),
											( 0.92388, -0.382683, 0),
											( 1, 0, 0 ),
											( 0.92388, 0.382683, 0),
											( 0.707107, 0.707107, 0 ),
											(  0.382683, 0.92388 ,0),
											(  0 ,1, 0),
											(  0 ,0.92388, 0.382683),
											(  0 ,0.707107, 0.707107),
											(  0 ,0.382683, 0.92388),
											(  0 ,0, 1),
											(  0 ,-0.382683,0.92388),
											(  0 ,-0.707107,0.707107),
											(  0 ,-0.92388, 0.382683),
											(  0 ,-1, 0),
											(  0 ,-0.92388, -0.382683),
											( 0 ,-0.707107, -0.707107 ),
											(  0 ,-0.382683 ,-0.92388),
											( 0 ,0 ,-1),
											( 0 ,0.382683, -0.92388),
											( 0 ,0.707107 ,-0.707107),
											( 0 ,0.92388, -0.382683),
											( 0 ,1 ,0),
											( 0.382683, 0.92388, 0),
											( 0.707107, 0.707107, 0),
											( 0.92388, 0.382683, 0),
											( 1 ,0 ,0),
											( 0.92388, 0 ,0.382683),
											( 0.707107 ,0, 0.707107),
											( 0.382683 ,0, 0.92388),
											( 0 ,0, 1),
											( -0.382683, 0 ,0.92388),
											( -0.707107 ,0 ,0.707107),
											( -0.92388 ,0 ,0.382683),
											( -1,0 ,0),
											( -0.92388 ,0,-0.382683),
											( -0.707107 ,0, -0.707107),
											( -0.382683 ,0, -0.92388),
											( 0 ,0 ,-1),
											( 0.382683 ,0 ,-0.92388),
											( 0.707107 ,0 ,-0.707107),
											( 0.92388 ,0, -0.382683),
											(  1,0, 0)

											),
											
											k = (0 , 1 , 2 , 3 , 4 , 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52  ),
											name  = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName