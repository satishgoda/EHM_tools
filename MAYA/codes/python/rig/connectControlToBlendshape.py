"""
what does this do:
connect controllers to face blandshapes

usage:
controller = "L_mouth_ctrl.tx"
blendAttr = "mouth_bls.L_narrow"
clampValue = -1;
multiplyer = -1;
ConnectControlToBlendshape(controller, blendAttr, clampValue, multiplyer)

controller = "R_mouth_ctrl.tx"
blendAttr = "mouth_bls.R_narrow"
clampValue = -1;
multiplyer = -1;
ConnectControlToBlendshape(controller, blendAttr, clampValue, multiplyer)
"""
from maya import cmds

def ConnectControlToBlendshape(controller, blendAttr, clampValue, multiplyer):
	
	cmds.transformLimits(controller.split(".")[0], tx=(-1,1), etx=(True,True))
	
	clampNode = cmds.createNode("clamp", n=blendAttr.replace(".","_")+"_clm")
	if (clampValue>0):
		cmds.setAttr( clampNode+".maxR", clampValue );
	else:
		cmds.setAttr( clampNode+".minR", clampValue );	

	multNode = cmds.createNode("multiplyDivide", n=blendAttr.replace(".","_")+"_mdn")
	cmds.setAttr( multNode+".input2X", multiplyer );

	cmds.connectAttr(controller, clampNode+".inputR" )
	cmds.connectAttr(clampNode+".outputR", multNode+".input1X" )


	cmds.connectAttr(multNode+".outputX", blendAttr )

