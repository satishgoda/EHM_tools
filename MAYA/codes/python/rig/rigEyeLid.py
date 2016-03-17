from maya import cmds
from codes.python import util
from codes.python.curve import util as curveUtil

#center = "center"
#vtx = cmds.ls(sl=True, fl=True)
def createJointFromCenterToEyelidVertex( center=None, vtx=None ):
	"""
	creates 2 joints from center to selected vertex, works with multiple vertices 
	"""
	for v in vtx:
		cmds.select(cl=True)
		jnt = cmds.joint()
		pos = cmds.xform(v, q=True, ws=True, t=True)
		cmds.xform(jnt, ws=True, t=pos)
		posC = cmds.xform(center, q=True, ws=True, t=True)
		cmds.select(cl=True)
		jntC = cmds.joint()
		cmds.xform(jntC, ws=True, t=posC)
		cmds.parent(jnt, jntC)
		cmds.joint(jntC, e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)


#sel = cmds.ls(sl=True)
#upv = "L_eye_upv"
def aimConstraintToLocator():
	"""
	creates a locator in joint's position and aim constraints the parent to this locator.
	these locators serve as controler for each joint of eye lid.
	works with multiple selection. 
	"""
	for s in sel:
		loc = cmds.spaceLocator()[0]
		pos = cmds.xform(s, q=1, ws=1, t=1)
		cmds.xform(loc, ws=1, t=pos)
		par = cmds.listRelatives(s, p=1)[0]
		cmds.aimConstraint(loc, par, mo=1, weight=1
							, aimVector=(1,0,0)	, upVector = (0,1,0)
							, worldUpType="object", worldUpObject = upv )



#sel = cmds.ls(sl=True)
#crv = "R_lowerLidHigh_crvShape"
#curveUtil.attachToCurve(sel=sel, crv=crv)



import pymel.core as pm
from codes.python.rig import zeroGrp
reload( zeroGrp )
def connectControlToJoint( jnts = None ):
	"""
	connects lid controls to joint which are the drivers of low res lid curve.
	can't use parent constraint, because we need to keep the joints in center
	to avoid double transform.
	works with multiple inputs
	"""
	zeros = zeroGrp.ZeroGrp(jnts)
	for ofs in zeros[1]:
	    ctrl = pm.PyNode(ofs.name().replace("ofs","ctrl"))
	    ref = pm.group(empty=True,n=ofs.name().replace("ofs","ctrlRef") )
	    ref.setParent( ctrl.getParent(generations=2) )
	    pm.parentConstraint( ctrl, ref )
	    ref.t >> ofs.t
	    ref.r >> ofs.r