# ---------------------------------------------------------------------------------
# synopsis : 			makeSplineStretchy ( )
#
# what does this script do ?	makes the IK splines stretchy	
#
#
# flags :
#                     ikCrv
#                     volume
#                     stretchSwitch        
#                     thicknessPlace (string) => "start" , "mid" , "end" 
#
#
# return :            None
# ---------------------------------------------------------------------------------

import pymel.core as pm



def MakeSplineStretchy ( **kwargs ):
	thicknessPlace = kwargs.setdefault('thicknessPlace', 'mid')
	stretchSwitch = kwargs.setdefault('stretchSwitch', True)
	volume = kwargs.setdefault('volume', True)	
	ikCrv = kwargs.setdefault( 'ikCrv' )	

	if ikCrv==None:
		ikCrv = pm.ls( sl=True )[-1]
	else:
		ikCrv = pm.ls( ikCrv )[-1]
	
	if not ikCrv.getShape().type() == 'nurbsCurve' :
		pm.error('ehm_tools...MakeSplineStretchy: Select an IK Spline Curve!')
	
	# the value used for keyging ss
	ssv = 0 
	if  volume==True :
		ssv = 1
	
	#===============================================================================
	# create curveInfo node

	curveShape = ikCrv.getShape()

	crvLenNode = pm.createNode ("curveInfo" , n = (  ikCrv.name() + "_Info") )

	pm.addAttr (  ikCrv , keyable =  True , ln = "scalePower" , at = "double")

	ikH = pm.listConnections ( curveShape , type = "ikHandle"  ) 

	jntsToSS = pm.ikHandle ( ikH[0] , q = True , jointList = True  )



	#================================================================================
	# key the curve
	

	if   thicknessPlace == "mid"  :
	
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = 1 , v = 0  )
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = len(jntsToSS)/2 , v = ssv  )
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = len(jntsToSS) , v = 0  )
	
	elif  thicknessPlace == "start"  :
		
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = 1 , v = ssv  )
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = len(jntsToSS) , v = 0  )       

	elif  thicknessPlace == "end"  :
		
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = 1 , v = 0  )
		pm.setKeyframe ( ( ikCrv + ".scalePower") , t = len(jntsToSS) , v = ssv  )
	else:
		print "ThinknessPlace not defined. Select one of these : 'start' , 'mid' , 'end' "


	curveShape.worldSpace[0] 		>> 		crvLenNode.inputCurve
	pm.addAttr (crvLenNode , ln = "normalizedScale"  , at = "double"  )

	normScl = pm.createNode ( "multiplyDivide" , n = ( ikCrv + "_normalizedScale") )
	pm.setAttr ( ( normScl + ".operation") , 2 )



	arcLen = pm.getAttr ( crvLenNode + ".arcLength")
	pm.setAttr ( (normScl + ".input2X") , arcLen )
	pm.connectAttr ( ( crvLenNode + ".arcLength") , (normScl + ".input1X") , f = True )
	pm.connectAttr ( (normScl + ".outputX") , (crvLenNode + ".normalizedScale") , f = True)
	stretchedScale = pm.createNode( "multiplyDivide" , n = ( ikCrv + "_scale_mdn") )
	pm.connectAttr ((normScl + ".outputX") , ( stretchedScale + ".input1X") , f = True)
	pm.setAttr  ( (stretchedScale + ".operation") , 2 )



	lenJnts = len(jntsToSS)

	for k in range (lenJnts):

		pm.addAttr ( jntsToSS[k] , keyable = True , ln = "pow"  , at = "double"  )
		cacheN = pm.createNode ( "frameCache" , n = (jntsToSS[k] + "_FCnode") )
		pm.connectAttr ( (cacheN + ".varying") , (jntsToSS[k] + ".pow") )
		pm.connectAttr ( ( ikCrv + ".scalePower") , (cacheN + ".stream") )
		pm.setAttr ( (cacheN + ".varyTime") , (k + 1) )



	#=================================================================================== 
	# create scale, sqrt and power nodes for keeping the volume using nodes instead of expression
	
	normScaleSqrt = pm.createNode ( "multiplyDivide" , n = "normScaleSqrt" )
	pm.connectAttr ( (stretchedScale + ".outputX") , (normScaleSqrt + ".input1X") )
	pm.setAttr ( (normScaleSqrt + ".operation") , 3 )
	pm.setAttr  ( (normScaleSqrt + ".input2X") , 0.5 )

	sqrtMult = pm.createNode ( "multiplyDivide" , n = "sqrtMult" )
	pm.setAttr ( (sqrtMult + ".input1X") , 1 )

	pm.setAttr ( (sqrtMult + ".operation") , 2 )
	pm.connectAttr ( (normScaleSqrt + ".outputX") , (sqrtMult + ".input2X") )


	for k in range(lenJnts) :
		scaleMult = pm.createNode( "multiplyDivide" , n = (jntsToSS[k] + "_scale_mdn") )
		pm.setAttr ( (scaleMult + ".operation") , 3 )

		sqrtMult.outputX 		>> 		scaleMult.input1X
		jntsToSS[k].pow 		>> 		scaleMult.input2X
		
		stretchedScale.outputX 	>> 		jntsToSS[k].scaleX
		scaleMult.outputX 		>> 		jntsToSS[k].scaleY
		scaleMult.outputX 		>> 		jntsToSS[k].scaleZ



	#=================================================================================== 
	# making the spine scalable by connecting the scale of the mian_ctrl to it's network


	if  stretchSwitch==True :
		pm.addAttr (  ikCrv , ln = "stretchSwitch"  , at = "double"  , keyable = True ,  min = 0 , max = 1 , dv = 1  )
		back_stretchSwitch_bln = pm.createNode ("blendColors" , n = "back_stretchSwitch_bln")

		back_stretchSwitch_bln.color1R.set ( 1 )
		normScl.outputX 	>>	back_stretchSwitch_bln.color2R
		ikCrv.stretchSwitch 	>>	back_stretchSwitch_bln.blender
		
		pm.connectAttr (  (back_stretchSwitch_bln + ".outputR") , (stretchedScale + ".input2X") , f = True  )