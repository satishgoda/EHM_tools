import pymel.core as pm
def CubeCrv(  size=1, name='cubeCrv') :
	ctrlName = pm.curve (d = 1 , p =    (       
										( 0.5 , -0.5  , -0.5 ) , 
										( -0.5 ,  -0.5 ,  -0.5 ) , 
										( -0.5 ,  -0.5 ,  0.5 ) , 
										( 0.5  , -0.5  , 0.5 ) , 
										( 0.5  , -0.5  , -0.5 ) , 
										( 0.5  , 0.5  , -0.5 ) , 
										( -0.5 ,  0.5 ,  -0.5 ) , 
										( -0.5 ,  -0.5 ,  -0.5 ) , 
										( -0.5 ,  0.5  , -0.5 ) , 
										( -0.5 ,  0.5  , 0.5 ) , 
										( -0.5 ,  -0.5 ,  0.5 ) , 
										( -0.5 ,  0.5  , 0.5 ) , 
										( 0.5  , 0.5  , 0.5 ) , 
										( 0.5 , -0.5 ,  0.5 ) , 
										( 0.5  , 0.5  , 0.5 ) , 
										( 0.5 , 0.5  , -0.5 )
										),
	
								k =     (0 , 1 , 2 , 3 , 4 , 5 , 6 , 7,8,9,10,11,12,13,14,15 ) , name = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName

