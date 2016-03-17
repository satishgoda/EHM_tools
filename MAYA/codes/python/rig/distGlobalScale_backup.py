import pymel.core as pm
# ==========================================================================================
# distance dimentions global scale def
# ==========================================================================================
def DistGlobalScale ( dist=None, mainCtrl=None ) :
	
	if dist==None or mainCtrl==None :
		dist, mainCtrl = pm.ls (sl=True)
	else:
		dist = pm.ls( dist )[0]
		mainCtrl = pm.ls( mainCtrl )[0]
	if dist and mainCtrl:
		distShape = dist.getShape()

		distShapeOuts = pm.listConnections (distShape ,s=False, p =True)
		
		if len (distShapeOuts) != 0 :
		
			globalScale_mdn = pm.createNode ("multiplyDivide" , n = "globalScale_mdn" )
			
			distShape.distance >> globalScale_mdn.input1X
			
			mainCtrl.scaleY >> globalScale_mdn.input2X
			
			globalScale_mdn.operation.set ( 2 )
			
			for out in distShapeOuts:
				
				globalScale_mdn.outputX >> out
