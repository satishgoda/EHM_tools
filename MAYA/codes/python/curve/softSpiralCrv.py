import pymel.core as pm
def SoftSpiralCrv (   size=1, name='softSpiral') :
	ctrlName = pm.curve (d = 3 , p =    (       
										( 0 , -0.41351,0.273544  ) ,
										( 0 ,-0.266078, 0.436295 ) ,
										( 0 ,0.352504 ,0.402532 ),
										( 0 ,0.566636 ,0.0764715 ),
										( 0 ,-0.0118138 ,-0.661953 ),
										( 0 ,-0.326706 ,-0.161112 ),
										( 0 ,-0.360884, 0.121381 ),
										( 0 ,0.00392279,0.219307 ),
										( 0, 0.268341, 0.0741531 ),
										( 0 ,-0.0467836 ,-0.31263 ),
										( 0 ,-0.123964 ,0.02545 ) 
										),
	
								k =     (0 , 0 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 8 , 8 ) , name = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName

