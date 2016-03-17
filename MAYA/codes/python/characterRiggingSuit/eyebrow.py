from maya import cmds
import maya.OpenMaya as om 
from codes.python import util
from codes.python.curve import util as curveUtil
reload( curveUtil )
from codes.python.rig import joint as jointUtil
reload( jointUtil )
from codes.python.rig import addControl
reload(addControl)

def build( curve=None, numOfJnts=10, name="brow" ):
	# soften input curve and delete history
	curve = util.rename(curve, name=(name+"Low"), suffix="crv")[0]
	curve = curveUtil.getShape( curve=curve )
	cmds.rebuildCurve(curve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=1, kep=1, kt=0, s=4, d=3, tol=0.01 )[0]
	cmds.makeIdentity(curve, apply=True, t=1, r=1, s=1 )

	# create the high res curve
	curveHigh = cmds.rebuildCurve(curve, ch=0, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=numOfJnts, d=1, tol=0.01 )[0]
	curveHigh = util.rename(curveHigh, name=(name+"High"), suffix="crv")[0]

	return curve, curveHigh

def connect(curve=None,curveHigh=None):
	# create control joints
	cvs = curveUtil.getCvs( curve=curve )
	controlJnts = jointUtil.createOnVertex( cvs )
	
	# skin control joints to input curve
	cmds.skinCluster ( curve , controlJnts  )

	# create control curves and connect to control joints
	addControl.AddControl(objsToPutCtrlOn=controlJnts, shape='cube')

	# wire deform high curve using input curve
	# wire, gw false -en 1 -ce 0 -li 0 -w curve1 curve1rebuiltCurve1;
	#cmds.wire(curveHigh, gw=False, en=1, ce=0, li=0, w=(curve) )
	#cmds.wire(curveHigh, w=(curve) )

	# create skin joints
	skinJnts = jointUtil.createOnCurve( curve=curveHigh, numOfJnts=10, parent=False )
	curveUtil.attachToCurve( sel=skinJnts, curve=curveHigh )