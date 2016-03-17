import pymel.core as pm

def FindDeformers ( shape=None , type=''):
	
	if shape==None:
		obj = pm.ls(sl=True)[0]
		shape = obj.getShape()
	
	if shape :
		# List Deformers
		history = pm.listHistory( shape, pruneDagObjects=True, interestLevel=2 ) 
		
		deformers = []
		
		for node in  history :
			nodeTypes = pm.nodeType( node, inherited=True )
		
			if 'geometryFilter' in nodeTypes:
				
				if type=='' and  nodeTypes[1] != 'tweak' :
					deformers.append(node)
			
				elif nodeTypes[1] == type and nodeTypes[1] != 'tweak':
					deformers.append(node)
		
		return deformers
	else:
		pm.warning('No shape found.')