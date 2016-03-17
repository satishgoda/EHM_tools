from maya import cmds, OpenMaya
import maya.OpenMaya as om 
from codes.python import util

def getUParam(pnt=[], curve=None):
    """
    returns the U parameter on the point on curve closest to the given point
    """
    point = om.MPoint(pnt[0], pnt[1], pnt[2])
    curveFn = om.MFnNurbsCurve(util.getDagPath(curve))
    paramUtil = om.MScriptUtil()
    paramPtr = paramUtil.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve:
        curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)
    else:
        point = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kObject)
        curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)
    param = paramUtil.getDouble(paramPtr)
    return param

#sel = cmds.ls(sl=True)
#curve = "R_lowerLidHigh_curveShape"
#attachToCurve(sel=sel, curve=curve)
def attachToCurve(sel=None, curve=None):
    """
    attachs selected object to curve using pointOnCurveInfo node
    """
    curve = getShape(curve)
    for s in sel:
        pos = cmds.xform(s, q=1, ws=1, t=1)
        u = getUParam(pos, curve)
        name = s.replace("_loc", "_pci")
        pci = cmds.createNode("pointOnCurveInfo", n=name)
        cmds.connectAttr(curve+".worldSpace", pci+".inputCurve")
        cmds.setAttr(pci+".parameter", u)
        cmds.connectAttr(pci+".position", s+".t")

def numOfCvs( curve=None ):
    """
    return number of CVs
    """
    curve = getShape( curve )   
    degree = cmds.getAttr(curve + ".degree")
    spans = cmds.getAttr(curve + ".spans")
    return (spans + degree)

def getShape(curve=None):
    """
    return itself or it's shape if input is a nurbsCurve
    otherwise errors.
    """
    if cmds.objectType(curve, isType="nurbsCurve"):
        return curve
    else:
        shapes = cmds.listRelatives(curve, shapes=True)
        if shapes and cmds.objectType(shapes[0], isType="nurbsCurve"):
            return shapes[0]
    cmds.error('object "{}" is not a nurbsCurve!'.format(curve))

def getCvs( curve=None ):
    """
    return number of CVs
    """
    curve = getShape(curve)
    cvList = []
    for i in range(numOfCvs(curve)):
        cvList.append( curve+".cv[{}]".format(i) )
    return  cvList


def getPointAtParam(curve=None, param=0, space='world'):
    """
    return a world position of specified point on curve.
    """
    curve = getShape(curve)
    crvDag = util.getDagPath(curve)
    nurbsFn = om.MFnNurbsCurve(crvDag)
    pointPtr = om.MPoint()
    if space=='world':
        nurbsFn.getPointAtParam(param, pointPtr, om.MSpace.kWorld )
    elif space=='object':
        nurbsFn.getPointAtParam(param, pointPtr, om.MSpace.kObject )
    else:
        cmds.error("wrong space specied. valid inputs are 'world' and 'object'.")

    return (pointPtr[0], pointPtr[1], pointPtr[2])  
