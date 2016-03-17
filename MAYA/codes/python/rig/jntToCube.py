import pymel.core as pm

from codes.python.general.dist  import  Dist

def JntToCube( jnts=None ):

	if jnts==None:
		jnts= pm.ls(sl=True)

	for jnt in jnts:
		children = jnt.getChildren()
		if len(children) > 0:
			childJnt = jnt.getChildren()[0]
			length = Dist(jnt, childJnt)
			cube = pm.polyCube( ch=False )[0]
			pm.parent(cube, jnt)
			cube.translate.set( length/2.0 ,0,0 )
			cube.rotate.set(0,0,0)
			cube.scale.set( length, 1-length*0.1, 1-length*0.1 )
			pm.makeIdentity(cube, apply=True, t=True, r=True, s=True)
			cubeShape = cube.getShape()
			pm.parent( cubeShape, jnt, add=True, shape=True )
			pm.delete(cube)