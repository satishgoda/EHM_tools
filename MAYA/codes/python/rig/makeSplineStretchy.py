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
	
		pm.setKeyframe ( ikCrv.scalePower , t = 1 , v = 0  )
		pm.setKeyframe ( ikCrv.scalePower , t = len(jntsToSS)/2 , v = ssv  )
		pm.setKeyframe ( ikCrv.scalePower , t = len(jntsToSS) , v = 0  )
	
	elif  thicknessPlace == "start"  :
		
		pm.setKeyframe ( ikCrv.scalePower , t = 1 , v = ssv  )
		pm.setKeyframe ( ikCrv.scalePower , t = len(jntsToSS) , v = 0  )       

	elif  thicknessPlace == "end"  :
		
		pm.setKeyframe ( ikCrv.scalePower , t = 1 , v = 0  )
		pm.setKeyframe ( ikCrv.scalePower , t = len(jntsToSS) , v = ssv  )
	else:
		print "ThinknessPlace not defined. Select one of these : 'start' , 'mid' , 'end' "


	curveShape.worldSpace[0] 		>> 		crvLenNode.inputCurve
	pm.addAttr (crvLenNode , ln = "normalizedScale"  , at = "double"  )

	normScl = pm.createNode ( "multiplyDivide" , n = ( ikCrv + "_normalizedScale") )
	normScl.operation.set( 2 )



	arcLen = pm.getAttr ( crvLenNode + ".arcLength")
	pm.setAttr ( (normScl + ".input2X") , arcLen )
	crvLenNode.arcLength >> normScl.input1X
	normScl.outputX >> crvLenNode.normalizedScale
	stretchedScale = pm.createNode( "multiplyDivide" , n = ( ikCrv + "_scale_mdn") )
	normScl.outputX >> stretchedScale.input1X
	stretchedScale.operation.set( 2 )


	#=================================================================================== 
	# create scale, sqrt and power nodes for keeping the volume using nodes instead of expression
	
	normScaleSqrt = pm.createNode ( "multiplyDivide" , n = "normScaleSqrt" )
	stretchedScale.outputX >> normScaleSqrt.input1X
	normScaleSqrt.operation.set( 3 )
	normScaleSqrt.input2X.set( 0.5 )

	sqrtMult = pm.createNode ( "multiplyDivide" , n = "sqrtMult" )
	sqrtMult.input1X.set( 1 )

	sqrtMult.operation.set( 2 )
	normScaleSqrt.outputX >> sqrtMult.input2X


	# find animCurve and disconnect if from spline curve.scalePower
	# we used scalePower just for creating the animCurve. Now that we have the anim curve we no longer need it
	animCurve = pm.listConnections( ikCrv.scalePower, d=True )[0]
	animCurve.output // ikCrv.scalePower	
	
	# but we can use curve.scalePower as a multiplyer to our auto valume result	
	volumeMultiplyer = pm.createNode ( "multiplyDivide" , n = "volume_multiplyer" )
	ikCrv.scalePower >> volumeMultiplyer.input1X
	animCurve.output >> volumeMultiplyer.input2X
	
	
	

	for k in range ( len(jntsToSS) ):
		
		cacheN = pm.createNode ( "frameCache" , n = (jntsToSS[k] + "_FCnode") )
		volumeMultiplyer.outputX >> cacheN.stream
		cacheN.varyTime.set( k + 1 )
		
		
		scaleMult = pm.createNode( "multiplyDivide" , n = (jntsToSS[k] + "_scale_mdn") )
		scaleMult.operation.set( 3 )

		sqrtMult.outputX 		>> 		scaleMult.input1X
		cacheN.varying			>> 		scaleMult.input2X
		
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