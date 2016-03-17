# ---------------------------------------------------------------------------------
# synopsis : 			guideCrv ( )
#
# what does this script do ?	 creates a guide curve between selected objects. useful for pole vectores
#
#
# how to use:        select two objects and run this 
#
# ---------------------------------------------------------------------------------

import pymel.core as pm

def GuideCrv ( startGuider=None , endGuider=None ):

	if startGuider==None or endGuider==None:
		startGuider,endGuider = pm.ls(sl=True)
	
	pm.select(clear=True)
	
	startJnt = pm.joint ( n = startGuider.name()+"_guideCrvJnt")
	pm.parent (startJnt , startGuider)
	startJnt.translate.set (0,0,0)
	startJnt.visibility.set (0)
	pm.setAttr ( startJnt.visibility , lock=True  )
	
	
	endJnt = pm.joint (  n = endGuider.name()+"_guideCrvJnt" )
	pm.parent (endJnt , endGuider)
	endJnt.translate.set (0,0,0)
	endJnt.visibility.set (0)
	pm.setAttr ( endJnt.visibility , lock=True  )
	
	startJntPos = pm.xform ( startJnt , q=True , ws=True , t=True)
	endJntPos = pm.xform ( endJnt , q=True , ws=True , t=True)
	
	guideCrv = pm.curve ( degree=1 , p = (startJntPos ,endJntPos) , k=(1,2)  )
	
	pm.rename ( guideCrv , startGuider.name()+"_guideCrv")
	
	pm.skinCluster ( guideCrv , startJnt , endJnt  )
	
	guideCrv.inheritsTransform.set(0)
	guideCrv.template.set(1)
	
	pm.select(clear=True)
	
	return guideCrv
	
