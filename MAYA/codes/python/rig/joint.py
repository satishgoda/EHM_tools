from maya import cmds
from codes.python.curve import util as curveUtil

def createOnVertex( vtx=None ):
	"""
	creates joints for eath selected vertex
	return: newly created joints
	"""
	joints = []

	if not vtx:
		vtx = cmds.ls(sl=True, fl=True)
	for v in vtx:
		cmds.select(cl=True)
		jnt = cmds.joint()
		pos = cmds.xform(v, q=True, ws=True, t=True)
		cmds.xform(jnt, ws=True, t=pos)
		cmds.joint(jnt, e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)
		joints.append(jnt)

	return joints

def createOnCurve( curve=None, numOfJnts=5, parent=True ):
	"""
	create specified number of joints on input curve
	"""
	curve = curveUtil.getShape(curve)
	if numOfJnts < 2 :
		cmds.error( "number of joints must be greater than 1.")	
	newJnts = []

	curve = cmds.duplicate(curve)[0]
	cmds.rebuildCurve (curve , ch=False ,rpo=True ,rt=0 ,end=1 ,kr=0 ,kcp=False ,kep=True ,kt=0 , s=200 , d=1 , tol=0.01 )
	curveShape = curveUtil.getShape(curve)

	cmds.select(clear=True)
	segSize = 1.0/ (numOfJnts-1)

	for i in range(numOfJnts):
		pos = curveUtil.getPointAtParam(curveShape, segSize*i, 'world')
		if not parent:
			cmds.select(clear=True)
		newJnts.append( cmds.joint(p=pos) )

	cmds.delete(curve)

	return newJnts

