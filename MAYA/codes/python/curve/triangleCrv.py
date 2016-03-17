import pymel.core as pm
def TriangleCrv ( size=0.1, name='triangleCrv' ) :
	ctrlName = pm.curve (d = 1 , p =    (       ( 0                , 0  ,     -3.314462*size  ),
												( 3.626265*size    , 0  ,     -3.626265*size  ),
												( 5.736098*size    , 0  ,     -2.432378*size  ),
												( 0.615568*size    , 0  ,      5.394739*size  ),
												( 0                , 0  ,      6.410073*size  ),
												( -0.615568*size   , 0  ,      5.394739*size  ),
												( -5.736098*size   , 0  ,     -2.432378*size  ),
												( -3.626265*size   , 0  ,     -3.626265*size  ),
												( 0                , 0  ,     -3.314462*size  )     
										),
	
								k =     (0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 ), name = name )
	return ctrlName

