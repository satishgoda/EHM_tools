# ---------------------------------------------------------------------------------
# synopsis :
#              ctrlForThis( createZeroGroup, dist )
#
# what does this method do ?
#       			create control curves for selected objects
#
# flags :
#                        createZeroGroup, (boolean)   =>  whether create empty groups for the controls or not
#
#                        dist, (float)   =>  size of the controls
#
#
# how to use:       select objects and and run this
#                             ctrlForThis(True,0.5)
#
# return :        newly created controls
#
#
# bugs : # DeprecationWarning: The function 'pymel.core.general.PyNode.__getitem__' is deprecated and will become unavailable in future pymel versions. Convert to string first using str() or PyNode.name(), at line 248, in "C:\Program Files\Autodesk\Maya2012\bin\maya.exe"
#
import pymel.core as pm
from codes.python.rig import zeroGrp
reload( zeroGrp )
ZeroGrp = zeroGrp.ZeroGrp


def CtrlForThis(  createZeroGroup=False , dist=1):

	ctrls = [] # ctrls names for return

	objsToPutCtrlOn =  pm.ls ( sl = True )

	# for every selected object create ctrl curves

	for i in range (len(objsToPutCtrlOn)):
		objToPutCtrlOn = objsToPutCtrlOn[i]
		# create circle, find the proper name for the contorl curve and name the circle
		if str(objToPutCtrlOn)[-3:] == "jnt":
			ctrl = pm.circle(nr = (1 , 0 , 0) , r= dist, ch=False,  name =   str(objToPutCtrlOn).replace("jnt", "ctrl") )
		else:
			ctrl = pm.circle(nr = (1 , 0 , 0) , r= dist, ch=False,   name =  (str(objToPutCtrlOn) + "_ctrl") )


		# parent curve to corisponding joint
		pm.parent ( ctrl[0] , objToPutCtrlOn )

		#reset tranform values on circles
		pm.xform (ctrl[0] , t = (0,0,0) , ro= (0,0,0))

		firstParent = pm.listRelatives ( objToPutCtrlOn , fullPath = True , parent = True )

		# parent ctrls to their firstgrandparent
		if firstParent  :
			pm.parent ( ctrl[0] , firstParent[0] )
		else :
			pm.parent ( ctrl[0] , world = True  )


		pm.parent ( objToPutCtrlOn , ctrl[0] )

		ctrls.append ( ctrl[0] )
		



	# create zero groups if needed - add zero groups as well to return value
	if createZeroGroup == True:
		pm.select (ctrls)
		ctrls.extend (  ZeroGrp()  )

	return ctrls

