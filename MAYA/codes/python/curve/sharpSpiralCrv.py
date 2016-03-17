import pymel.core as pm
def SharpSpiralCrv ( size=1, name='sharpSpiral') :
	ctrlName = pm.curve (d = 1 , p =    (       
										( 0 , -0.469591 , -0.32729 ) ,
										( 0 , 0.483821  , -0.320175 ) ,
										( 0 , 0.0711501 , 0.569201 ) ,
										( 0 , -0.401342 , -0.151363 ) ,
										( 0 , 0.226872 , -0.153968 ) ,
										( 0 , -0.0342101 , 0.158648 ) ,
										( 0 , -0.123269 , -0.0587177 ) ,
										( 0 , 0.0618337 , -0.0383726 ) 
										),
	
								k =     (0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 ) , name = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName
