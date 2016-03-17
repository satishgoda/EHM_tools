import sys

global deformerState

if deformerState:
	clss = pm.ls( type='cluster' )
	for cls in clss:
		cls.envelope.set(0)
	
	skns = pm.ls( type='skinCluster' )
	for skn in skns:
		skn.envelope.set(0)
	
	deformerState = False
	sys.stdout.write( 'deformers are OFF' ) 

else:
	clss = pm.ls( type='cluster' )
	for cls in clss:
		cls.envelope.set(1)
	
	skns = pm.ls( type='skinCluster' )
	for skn in skns:
		skn.envelope.set(1)
	
	deformerState = True
	sys.stdout.write( 'deformers are ON' ) 