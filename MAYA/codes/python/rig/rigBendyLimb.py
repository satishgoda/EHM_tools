'''

select 3 joints and one control curve ( eg: control curve could be your ik-fk control curve. )
objs = pm.ls(sl=True)
RigBendyLimb( jnts= objs[:3], bendyCtrl=objs[3] )

'''
import pymel.core as pm

from codes.python.rig import segmentor
Segmentor= segmentor.Segmentor

from codes.python.rig.findPosBetween import FindPosBetween


def RigBendyLimb( **kwargs ):
	jnts = 				kwargs.setdefault( 'jnts' )	
	volume = 			kwargs.setdefault( 'volume' , False )
	limbName = 			kwargs.setdefault( 'limbName', 'arm' )
	side = 				kwargs.setdefault( 'side', 'L' )
	numOfSegs = 		kwargs.setdefault( 'numOfSegs', 5 )
	FKIKMode = 			kwargs.setdefault( 'FKIKMode', 'FKIK' )
	bendyCtrl = 		kwargs.setdefault( 'bendyCtrl' )
	isMirroredJoint = 	kwargs.setdefault( 'isMirroredJoint' , False )	

	if not ( jnts and bendyCtrl ):
		objects = pm.ls(sl=True)
		if not len( objects ) == 4 :
			pm.error('ehm_tools...rigBendyLimb: select 3 joint and a control curve')
		uparmJnt = objects[0]
		elbowJnt = objects[1]
		handJnt  = objects[2]	
		bendyCtrl = objects[3]
	else:
		uparmJnt = jnts[0]
		elbowJnt = jnts[1]
		handJnt  = jnts[2]



	# if limb is not straight, make it so. necessary for for skinning bendy curves.
	if not FKIKMode == "IK" :
		tempElbowOri = elbowJnt.jointOrient.get()
		elbowJnt.jointOrient.set( 0,0,0 )
	else : # find position for putting the ik so that arm gets straight
		tempHandIKLoc = pm.spaceLocator ()
		pm.parent ( tempHandIKLoc , uparmJnt  )
		tempHandIKLoc.rotate.set(0,0,0)
		armLen =  elbowJnt.translate.translateX.get() + handJnt.translate.translateX.get()
		tempHandIKLoc.translate.set( armLen ,0,0)
		tempHandIKPos = pm.xform ( tempHandIKLoc , q=True , ws=True ,  translation = True )
		pm.parent (IKarmDistLocs[1], w=True)
		# straighten the arm for skinning
		IKarmDistLocs[1].translate.set( tempHandIKPos )


	# create bendy joint
	uparmSegStuff = Segmentor( jnt = uparmJnt
								,numOfSegs= numOfSegs
								,volume= volume
								,thicknessPlace= 'end'
								,isMirroredJoint= isMirroredJoint
								)

	elbowSegStuff = Segmentor( jnt = elbowJnt 
								,numOfSegs= numOfSegs
								,volume= volume
								,thicknessPlace= 'start'
								,isMirroredJoint= isMirroredJoint
								)


	# avoid shear on elbow seg joints
	pm.scaleConstraint( uparmJnt, elbowSegStuff[1][2].getParent() )


	# create the uparm orientaion loc, point and aim constraint it so that it aims to hand joint
	uparmOriLoc = pm.spaceLocator ()
	pm.pointConstraint( uparmJnt, uparmOriLoc )
	pm.aimConstraint( handJnt, uparmOriLoc )



	# create the elbow orientation loc, connect it to uparm ori loc and elbow joint
	elbowOriLoc = pm.spaceLocator ()
	pm.pointConstraint( elbowJnt, elbowOriLoc )
	pm.orientConstraint( uparmOriLoc, elbowOriLoc )



	# move second and forth CVs of the bendy curves very close to where joints are.
	uparm_seg_crv = uparmSegStuff[1][2]
	elbow_seg_crv = elbowSegStuff[1][2]

	closeToUparm       =  FindPosBetween( percent=1, base=uparmJnt, tip=elbowJnt )
	closeToElbow       =  FindPosBetween( percent=99, base=uparmJnt, tip=elbowJnt )
	closeToElbowAfter  =  FindPosBetween( percent=1, base=elbowJnt, tip=handJnt )
	closeToHand        =  FindPosBetween( percent=99, base=elbowJnt, tip=handJnt )

	pm.xform( uparm_seg_crv.cv[1], ws=True, t=closeToUparm )
	pm.xform( uparm_seg_crv.cv[3], ws=True, t=closeToElbow )
	pm.xform( elbow_seg_crv.cv[1], ws=True, t=closeToElbowAfter )
	pm.xform( elbow_seg_crv.cv[3], ws=True, t=closeToHand )



	# create joints, sking to bendy curves and parent the middle one under elbow ori loc.
	bendyJnts_dict = { 'one':uparmJnt
						, 'two':elbowJnt
						, 'three':handJnt }

	for i in bendyJnts_dict.keys() :
		pm.select( clear=True )
		tmp =   pm.joint( name='%s_%s_bendy_%s_jnt' %( side, limbName, i )  ) 
		tmp.setParent( bendyJnts_dict[i] )
		tmp.translate.set(0,0,0)
		bendyJnts_dict[i] = tmp

	bendyJnts_dict['two'].setParent( elbowOriLoc )



	# skin the seg_crvs and set the weights
	uparm_seg_crv_skinCluster = ( pm.skinCluster( uparm_seg_crv ,  bendyJnts_dict['one'] , bendyJnts_dict['two'] , toSelectedBones = True ) )
	elbow_seg_crv_skinCluster = ( pm.skinCluster( elbow_seg_crv ,  bendyJnts_dict['two'] , bendyJnts_dict['three'] , toSelectedBones = True ) )

	pm.skinPercent ( uparm_seg_crv_skinCluster , (uparm_seg_crv + ".cv[2:4]") , transformValue = ( bendyJnts_dict['two'], 1)  )
	pm.skinPercent ( elbow_seg_crv_skinCluster , (elbow_seg_crv + ".cv[0:2]") , transformValue = ( bendyJnts_dict['two'], 1)  )

	pm.skinPercent ( uparm_seg_crv_skinCluster , (uparm_seg_crv + ".cv[0:1]") , transformValue = ( bendyJnts_dict['two'], 0)  )
	pm.skinPercent ( elbow_seg_crv_skinCluster , (elbow_seg_crv + ".cv[3:4]") , transformValue = ( bendyJnts_dict['two'], 0)  )



	# setting the twist parameters for the segmenty joints




	# add bendy attribute to finger ctrl and connect it
	if not pm.attributeQuery( 'bendy', n=bendyCtrl, exists=True  ):
		try:
			pm.addAttr( bendyCtrl, ln="bendy", at = 'double', min = 0, dv = 0 )
			pm.setAttr( bendyCtrl.bendy, e=True, keyable=True )
		except:
			pm.error( 'ehm_tools...rigBendyLimb: could not add bendy attr to %s'%bendyCtrl )
	
	
	# slow down the bendy attribute by 10 times
	bendySlower_mdn = pm.createNode( 'multiplyDivide', name='%s_%s_bendySlower_mdn'%(side,limbName) )
	bendyCtrl.bendy >> bendySlower_mdn.input1X
	bendySlower_mdn.input2X.set(0.1)
	bendySlower_mdn.outputX >> elbowOriLoc.scaleX


	# set the limb back to it's old position.
	if not FKIKMode == "IK" :
		elbowJnt.jointOrient.set( tempElbowOri )
	else:
		pm.parent  ( IKarmDistLocs[1] , handIKCtrl  )
		IKarmDistLocs[1].translate.set( 0,0,0 )
		
	segStuffGrp = pm.group( uparmSegStuff[2], elbowSegStuff[2], name='%s_%s_bendyStuff_grp'%(side,limbName) )
	pm.xform( os=True, piv=(0,0,0) )
	# return
	return( uparmSegStuff, elbowSegStuff, segStuffGrp )