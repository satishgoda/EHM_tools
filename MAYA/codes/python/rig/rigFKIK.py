# rigFKIK()
# objs = pm.ls(sl=True)
# rigFKIK( jnts=objs )
#======================================================================================

import pymel.core as pm

from codes.python.general     import     getAllChildren
GetAllChildren = getAllChildren.GetAllChildren 
from codes.python.general import searchReplaceNames
SearchReplaceNames = searchReplaceNames.SearchReplaceNames
from codes.python.general.colorize import Colorize
from codes.python.general.lockHideAttr import LockHideAttr
from codes.python.general.reverseShape import ReverseShape
from codes.python.curves.handCrv import HandCrv
from codes.python.curves.footCrv import FootCrv
from codes.python.rig.zeroGrp import ZeroGrp
from codes.python.rig.rigFK import RigFK
from codes.python.rig	import rigIK
RigIK = rigIK.RigIK
from codes.python.rig.matchTransform import MatchTransform
from codes.python.rig.blendAttrs import BlendAttrs
from codes.python.rig.noJointInViewport import NoJointInViewport


def RigFKIK( jnts=None, side='L', mode='arm',footRotate=None,rigHandOrFoot=False,  ctrlSize = 1.0,mirrorMode=False,poleVectorTransform=None	):

	if not jnts:
		jnts = pm.ls( sl=True )
	else:
		jnts = pm.ls( jnts )
	
	if mode=='arm':
		limbName = 'hand'
		secondLimb = 'elbow'
		optionCrv = HandCrv
	elif mode=='leg':
		limbName = 'foot'
		secondLimb = 'knee'
		optionCrv = FootCrv
	else:
		pm.error('ehm_tools...rigFKIK: mode argument must be either "arm" or "leg"!')


	
	uparmJnt	=	jnts[0]
			
	handJnt		=	jnts[2]

	# FK
	FKjnt = pm.duplicate( uparmJnt )[0]
	FKjnts = GetAllChildren( FKjnt )
	SearchReplaceNames(  'jnt', 'FK_jnt', FKjnts)
	FKjnts[0].rename( FKjnts[0].name()[:-1] )
	FKshapes = RigFK( jnts =  FKjnts[:2] , side=side )
	FKshapes.append( RigFK( jnts =  FKjnts[2:-1]  , stretch=False, side=side  ) )
	NoJointInViewport( FKjnts )



	# IK
	IKjnt = pm.duplicate( uparmJnt )[0]
	IKjnts = GetAllChildren( IKjnt )
	SearchReplaceNames(  'jnt', 'IK_jnt', IKjnts)
	IKjnts[0].rename( IKjnts[0].name()[:-1] )
	IKjnts = pm.ls( IKjnts, jnts[-3:] )
	IKstuff = RigIK( 			  jnts=IKjnts
								, side=side
								, mode=mode
								, mirrorMode=mirrorMode
								, poleVectorTransform=poleVectorTransform
								, footRotate=footRotate
								, rigHandOrFoot=rigHandOrFoot
								, ctrlSize=1.0 )
	IKjnts[0].v.set( False )
	pm.setAttr ( IKjnts[0].v  , lock = True )


	# Fingers Ctrl which is FKIK control as well
	fingersCtrl =  optionCrv ( name = '%s_fingers_ctrl' %side )
	
	# find color of the ctrls
	color = 'y'
	if side == 'L':
		color = 'r'
	elif side == 'R':
		color = 'b'

		
	
	Colorize(  shapes=fingersCtrl.getShape() , color=color )
	fingerCtrlZO = ZeroGrp ( fingersCtrl )
	pm.addAttr (  fingersCtrl , ln = "FKIK"  , at = "double"  , min = 0 , max = 1 , dv = 0 , k = True  )
	fingerCtrlZO[0].translate.set( pm.xform(IKstuff[0],q=True,t=True,ws=True) )
	
	if side=='L' and mode=='leg':
		fingersCtrl.translateX.set( ctrlSize )
	elif side=='R':
		fingersCtrl.translateX.set( - ctrlSize )
		ReverseShape( fingersCtrl , 'x' )
	pm.parentConstraint( handJnt, fingerCtrlZO[0], mo=True )


	# blend FK IK joints
	for j in range( 4 ) :
		for att in ( 'rotate', 'scale' ):
			BlendAttrs( IKjnts[j].attr(att), FKjnts[j].attr(att),  jnts[j].attr(att) , fingersCtrl.FKIK )


	BlendAttrs( 0 , 1 , FKjnts[0].v, fingersCtrl.FKIK )
	BlendAttrs( 1 , 0 , IKstuff[0].v, fingersCtrl.FKIK )
	BlendAttrs( 1 , 0 , IKstuff[1].v, fingersCtrl.FKIK )

	LockHideAttr( objs= ( FKjnts, IKstuff[0], IKstuff[1] ) , attrs='v' )

	# clean up
	FKIKgrp = pm.group( jnts[0], IKstuff[-1], FKjnts[0], fingerCtrlZO[0], name='%s_%s_grp'%(side,mode) )
	
	return ( FKjnts, IKjnts, IKstuff, fingersCtrl, FKIKgrp )

