import pymel.core as pm

##############################################
# num of ctrls
##############################################
num_ctrls = 3


##############################################
# num of joints
##############################################
num_jnts = 5


##############################################
# get nurbs surface
##############################################
def returnNurbs( objs=None ):
	surf = []
	for obj in objs:
		if obj.getShape().type() == "nurbsSurface":
			surf.append(obj)
	return surf

objs = pm.ls( sl=True )
surfs = returnNurbs( objs )


##############################################
# create follicles and joints
##############################################
folShape = pm.createNode('follicle' )

folShape.parameterU.set( U )  ?????
folShape.parameterV.set( V )  ?????

fol = folShape.getParent()
pm.rename( fol, '%s_flc'%source.name() )


surfShape.local >> folShape.inputSurface
surfShape.worldMatrix[0] >> folShape.inputWorldMatrix

folShape.outRotate >> fol.rotate
folShape.outTranslate >> fol.translate

folList.append( fol )
folShapeList.append( folShape )


# create ctrl objects

# make ctrl objects control the surface

# clean up

