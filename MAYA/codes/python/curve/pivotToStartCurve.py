# move pivot of selected curve to it's start CV

import pymel.core as pm

def PivotToStartCurve(objs=None):
	if not objs:
		objs = pm.ls( sl=True )

	for obj in objs:
		pivPoint = pm.xform( obj.cv[0], q=True, ws=True, t=True )
		obj.scalePivot.set( pivPoint )
		obj.rotatePivot.set( pivPoint )	