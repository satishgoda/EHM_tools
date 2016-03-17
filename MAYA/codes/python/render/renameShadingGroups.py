import pymel.core as pm

SG_nodes = pm.ls( type='shadingEngine' )

SG_nodes.remove( 'initialShadingGroup' )
SG_nodes.remove( 'initialParticleSE' )

for SG_node in SG_nodes:
	shader = pm.listConnections( SG_node.surfaceShader ) 
	
	if not shader:
		continue
	if 'MTL' in shader[0].name():
		SG_node.rename( shader[0].name().replace('MTL','SHE') )
	else:
		SG_node.rename( shader[0].name()+'_SHE' )
