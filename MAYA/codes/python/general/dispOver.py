import pymel.core as pm
def DispOver( obj , task , color = 20 ) :

	if task == "on" :
		pm.setAttr ( obj.attr("overrideEnabled")  , 1 )
	
	elif task == "off" :
		pm.setAttr ( obj.attr("overrideEnabled")  , 0 )
	elif task == "col" :
		pm.setAttr ( obj.attr("overrideEnabled")  , 1 )
		pm.setAttr ( obj.attr("overrideColor")  , color )
	else :
		print 'Select "on" , "off" or "col" with a color name.'
		
 