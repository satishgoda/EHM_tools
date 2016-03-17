import pymel.core as pm
import maya.mel as mel
import math

from codes.python.rig import attachToCurve
reload( attachToCurve )
AttachToCurve = attachToCurve.AttachToCurve

from codes.python.general import colorize
reload( colorize )
Colorize = colorize.Colorize

from codes.python.general import searchReplaceNames
reload( searchReplaceNames )
SearchReplaceNames = searchReplaceNames.SearchReplaceNames

from codes.python.rig import zeroGrp
reload( zeroGrp )
ZeroGrp = zeroGrp.ZeroGrp

# get info
# =========================================================================
objs = pm.ls(sl=True)
uppCurve = objs[0]
lowCurve = objs[1]
center = objs[2]
prefix = "L"
centerPos = pm.xform( center, q=1, t=1, ws=1 )
uppCurve  = uppCurve.getShape()
lowCurve  = lowCurve.getShape()

# creates joints running from center object to 
# each curve's CV except second and the one to the last CV
# =========================================================================
def jointChainOnCurveCVs(size=1, crv=None, prefix="lid"):
	jnts = []
	endJnts = []
	for i,cv in enumerate(crv.cv):
		pm.select( clear=1 )
		cvPose = pm.xform( cv, q=1, t=1, ws=1 )
		jnts.append( pm.joint(p=centerPos, name="%s_%s_jnt"%(prefix,i)) )
		jnts[i].radius.set( size )
		endJnts.append( pm.joint(p=cvPose, name="%s_%s_end"%(prefix,i)) )
		endJnts[i].radius.set( size )	
		pm.joint( jnts[i], e=True, oj="xyz", sao="yup", zso=1, ch=1 )
	pm.delete( (jnts[1],jnts[-2]) )
	jnts.remove( jnts[1] )
	jnts.remove( jnts[-2] )
	endJnts.remove( endJnts[1] )
	endJnts.remove( endJnts[-2] )
	return(jnts, endJnts)

# creates locators on all curve's CVs except second and one to last ones
# =========================================================================
def locatorOnCurveCVs(size=1, crv=None, prefix="lid"):
	locs = []
	for i,cv in enumerate(crv.cv):
		pm.select( clear=1 )
		cvPose = pm.xform( cv, q=1, t=1, ws=1 )
		locs.append( pm.spaceLocator(name="%s_%s_loc"%(prefix,i)) )
		locs[i].translate.set( cvPose )		
		locs[i].localScale.set(size,size,size)
	pm.delete( (locs[1],locs[-2]) )
	locs.remove( locs[1] )
	locs.remove( locs[-2] )	
	return(locs)
	
# creates joints on all curve's CV except second and one to last ones
# =========================================================================
def jointOnCurveCVs(size=1, crv=None, prefix="lid"):
	jnts = []
	for i,cv in enumerate(crv.cv):
		pm.select( clear=1 )
		cvPose = pm.xform( cv, q=1, t=1, ws=1 )
		jnts.append( pm.joint(p=cvPose, name="%s_%s_jnt"%(prefix,i)) )
		jnts[i].radius.set( size )	
		pm.joint( jnts[i], e=True, oj="xyz", sao="yup", zso=1, ch=1 )
	pm.delete( (jnts[1],jnts[-2]) )
	jnts.remove( jnts[1] )
	jnts.remove( jnts[-2] )
	return jnts

# create upVec object
# =========================================================================
estimatedEyeSize = pm.util.max(uppCurve.boundingBoxMax.get()-uppCurve.boundingBoxMin.get())
upVec = pm.spaceLocator( name=prefix+"_lid_upVec")
upVec.localScale.set(estimatedEyeSize/10,estimatedEyeSize/10,estimatedEyeSize/10)
pm.delete( pm.pointConstraint(center, upVec) )
pm.delete( pm.orientConstraint(center, upVec) )
upVec.translateY.set( upVec.translateY.get() + estimatedEyeSize )


# for each CV of curves create joints running from center to them
# =========================================================================
uppJnts, uppEndJnts = jointChainOnCurveCVs(size=estimatedEyeSize/20, crv=uppCurve, prefix=prefix+"_upp_lid")
lowJnts, lowEndJnts = jointChainOnCurveCVs(size=estimatedEyeSize/20, crv=lowCurve, prefix=prefix+"_low_lid")

# for each CV of curves create Locators
# =========================================================================
uppLocs = locatorOnCurveCVs(size=estimatedEyeSize/5, crv=uppCurve, prefix=prefix+"_upp_lid")
lowLocs = locatorOnCurveCVs(size=estimatedEyeSize/5, crv=lowCurve, prefix=prefix+"_low_lid")

# aimConstraint joints to locators
# =========================================================================
for jnt,loc in zip(uppJnts,uppLocs):
	pm.aimConstraint( loc, jnt, aimVector=(1,0,0), upVector=(0,1,0), worldUpObject=upVec, worldUpType="object" )
for jnt,loc in zip(lowJnts,lowLocs):
	pm.aimConstraint( loc, jnt, aimVector=(1,0,0), upVector=(0,1,0), worldUpObject=upVec, worldUpType="object" )

# lower the resolution of the curves
# =========================================================================
pm.rebuildCurve(uppCurve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=4, d=3, tol=10)
pm.rebuildCurve(lowCurve, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=4, d=3, tol=10)

# attach locators to curves
# =========================================================================
for loc in uppLocs:
	locPos = pm.xform( loc, q=True, t=True, ws=True )
	AttachToCurve( createNewLocator=False, objectToConnect=loc, worldPos=locPos, crv=uppCurve )
for loc in lowLocs:
	locPos = pm.xform( loc, q=True, t=True, ws=True )
	AttachToCurve( createNewLocator=False, objectToConnect=loc, worldPos=locPos, crv=lowCurve )

# create control objects for each cv of the curves
# =========================================================================
# control joints
uppControlJnts = jointOnCurveCVs(size=estimatedEyeSize/5, crv=uppCurve, prefix=prefix+"_upp_lidControl")
lowControlJnts = jointOnCurveCVs(size=estimatedEyeSize/5, crv=lowCurve, prefix=prefix+"_low_lidControl")
pm.skinCluster(uppControlJnts, uppCurve)
pm.skinCluster(lowControlJnts, lowCurve)	
# conrner controls of the eyes are the same for upper and lower lids
controlJntsTemp = list(uppControlJnts)
controlJntsTemp.extend(lowControlJnts)
controlJntsTemp.remove(lowControlJnts[0])
controlJntsTemp.remove(lowControlJnts[-1])
# control curves
ctrls=[]
for i,jnt in enumerate(controlJntsTemp):
	ctrls.append(pm.circle(r=estimatedEyeSize/6, ch=False, name="%s_lid_%s_ctrl"%(prefix,i+1)))
	# parent all joints under coresponding control except first and last lower joints
	pm.delete(pm.pointConstraint(jnt, ctrls[i]))
	pm.parentConstraint(ctrls[i], jnt)
	Colorize(ctrls[i],color='r')
# parent first and last lower joints to first and last upper controls curves
pm.parentConstraint(ctrls[0], lowControlJnts[-1])
pm.parentConstraint(ctrls[4], lowControlJnts[0])
# create extra groups above control curves
ctrlZeroGrps = ZeroGrp(ctrls)[0]
# make controls more animation friendly by parenting them under each other
pm.parentConstraint(ctrls[0], ctrls[2], ctrlZeroGrps[1], mo=True)
pm.parentConstraint(ctrls[2], ctrls[4], ctrlZeroGrps[3], mo=True)
pm.parentConstraint(ctrls[0], ctrls[2], ctrlZeroGrps[1], mo=True)
pm.parentConstraint(ctrls[4], ctrls[6], ctrlZeroGrps[5], mo=True)
pm.parentConstraint(ctrls[6], ctrls[0], ctrlZeroGrps[7], mo=True)

# cleanup outliner
# =========================================================================
lidSkinJnts_grp = pm.group( uppJnts, lowJnts, name=prefix+"_lidSkinJnts_grp" )
lidControlJnts_grp = pm.group( uppControlJnts, lowControlJnts, name=prefix+"_lidControlJnts_grp" )
lidLocs_grp = pm.group( uppLocs, lowLocs, name=prefix+"_lidLocs_grp" )
lidCtrls_grp = pm.group( ctrlZeroGrps, name=prefix+"_lidCtrls_grp" )
pm.hide(uppLocs, lowLocs, uppControlJnts, lowControlJnts)

# mirror everthing
# =========================================================================
lid_rig_grp = pm.group(lidSkinJnts_grp, lidControlJnts_grp, lidLocs_grp, lidCtrls_grp, uppCurve, lowCurve, center, upVec, upVec, name=prefix+"_lid_rig_grp")
pm.xform(lid_rig_grp, os=True, piv=(0,0,0))
otherSide_lid_rig_grp = pm.duplicate(lid_rig_grp,rr=True,un=True)[0]
otherSide_lid_rig_grp.scaleX.set(-1)
mel.eval( 'searchReplaceNames "L_" "R_" "hierarchy"' )
mel.eval( 'searchReplaceNames "grp1" "grp" "selected"' )
