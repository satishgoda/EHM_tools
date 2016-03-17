import pymel.core as pm
import pymel.core.datatypes as dt

'''
import pymel.core as pm
import sys
sys.path.append( r"D:\all_works\MAYA_DEV\EHM_tools\MAYA" ) 

from codes.python.curves import pivotToStartCurve
reload( pivotToStartCurve )

from codes.python.curves import createBlendedCurve
reload( createBlendedCurve )
CreateBlendedCurve = createBlendedCurve.CreateBlendedCurve


objs = pm.ls(sl=True)
pivotToStartCurve.PivotToStartCurve( objs=objs )
pm.makeIdentity( apply=True, t=True, r=True, s=True )

resultCurves = []
for i in range(len(objs)-1):
    resultCurves.append( objs[i] )
    resultCurves.append( CreateBlendedCurve( objs[i], objs[i+1] ) )

resultCurves.append( objs[i+1] )
pm.select( resultCurves )
pivotToStartCurve.PivotToStartCurve( objs=resultCurves )
pm.group()
pm.select( resultCurves )

'''

def CreateBlendedCurve( curve1, curve2 ):
    # check inputs
    curveShape1  = getShapeOfType(curve1,"nurbsCurve")
    curveShape2  = getShapeOfType(curve2,"nurbsCurve")
    if not (curveShape1 and curveShape2):
        pm.error( "createBlendedCurve needs two curve!" )
    if not haveSameNumberOfCVs(curve1,curve2):
        pm.error( "createBlendedCurve - number of CVs must match!" )
    # do it
    curve3 = pm.duplicate( curve1 )[0]
    numberOfCVs = curve3.getShape().numCVs()
    
    cvPositions1 = dt.Array( curve1.getCVs() )
    cvPositions2 = dt.Array( curve2.getCVs() )
    cvPositions3 = cvPositions1.blend(cvPositions2, weight=0.5)
    curve3.setCVs(cvPositions3)
    return curve3

def haveSameNumberOfCVs( curve1, curve2 ):
    return True if curve1.getShape().numCVs()==curve2.getShape().numCVs() else False
    
def getShapeOfType( obj, type ):
    if obj.type() == type:
        return obj
    else:
        shape = obj.getShape()
        if not shape:
            pm.warning( "given object doesn't have a shape of type '{}'".format( type ))
            return None
    if shape.type() == type:
        return shape
    else:
        pm.warning( "given object is not or doesn't have a shape of type '{}'".format( type ))
        return None