import pymel.core as pm

flcs = pm.ls(sl=True)

for flc in flcs:
	revSkin = pm.PyNode( flc.name().replace('flc','revSkin') )
	skinJnt = pm.PyNode( flc.name().replace('flc','secondaryRig_skin') )
	ctrl = pm.PyNode( flc.name().replace('flc','ctrl') )
	ctrlZero = pm.PyNode( flc.name().replace('flc','ctrl_zero') )
	ctrlOfs = pm.PyNode( flc.name().replace('flc','ctrl_ofs') )
	
	pm.pointConstraint(flc, ctrlZero, mo=True)
	pm.parentConstraint(ctrlOfs, revSkin, mo=True)
	pm.parentConstraint(ctrl, skinJnt, mo=True)