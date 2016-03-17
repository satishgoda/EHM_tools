import pymel.core as pm
def SquareSpiralCrv ( size=0.15, name='squareSpiral') :
	ctrlName =  pm.curve ( d = 1 , 
				p = [ (0 , -3.316654 , -0.758092) ,( 0 , 0.331665 , 3.624629) ,( 0 , 3.221892 , -0.497498) , ( 0 , 0.355356 , -3.032369)
				,( 0 , -1.516185 , -0.994996) , ( 0 , 0.61595 , 1.184519) ,( 0 , 0.994996 , -0.213213) ,( 0 , -0.0473808 , -0.63964) ] , 
				k = [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 ] , n = name )
	ctrlName.scale.set(size,size,size)
	pm.makeIdentity (ctrlName , apply=True , s=True)
	return ctrlName

