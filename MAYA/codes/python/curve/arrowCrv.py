import pymel.core as pm

def ArrowCrv( size=1, name='arrowCrv') :
	
	ctrlName =  pm.curve (d = 1 , p =  ( 
											( 0 , 0.621772 , 0 ),
											( 0 , 0.621772 , -0.1 ),
											( 0 , 1 , 0 ),
											( 0 , 0.621772 , 0.1  ),
											( 0 , 0.621772 , 0 ),
											( 0 , 0 , 0 )

											),
											
											k = (0 , 1 , 2 , 3 , 4 , 5  ),
											name  = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName
