import pymel.core as pm
def Circle8Crv( size=0.5, name='circle8Crv') :
	
	ctrlName =  pm.curve (d = 1 , p =  ( 
											( 0 , 0 , 1.108194 ),
											( 0 , 0.783612 , 0.783612 ),
											( 0 , 1.108194 , 0 ),
											( 0 , 0.783612 , -0.783612 ),
											( 0 , 0 , -1.108194 ),
											( 0 , -0.783612 , -0.783612 ),
											( 0 , -1.108194 , 0 ),
											( 0 , -0.783612 , 0.783612 ),
											( 0 , 0 , 1.108194 )
											
											),
											
											k = (0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 ),
											name  = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName