#nm_python_bendy_proc
from __future__ import division
import maya.cmds as cmds
import string
import operator
import maya.mel as mel

def bendy_proc():
	cmds.scriptEditorInfo(suppressWarnings=True)
	global globalScale
	globalScale = cmds.textField( "textField", q = True, tx = True )
	
	#get the selected objects and add them
	tsl = []
	tsl = cmds.textScrollList( "tsList", q = True, ai = True )
	cmds.textScrollList( "tsList", e = True, di = ("(only works on joints)")  )

	#select the textScrollList
	if ( len(tsl) > 0 ):
		list = ('' )
		
		for item in tsl:
			list += ('"' + item )
			list += '", '
			
		list = list[:-2]
		list = list.replace("(only works on joints)", "")
		list = list[4:]
		list = ('cmds.select(' + list + ', r = True )' )
	eval(list)
	
	#list and count only the joints in tsList
	joints = []
	joints = cmds.ls( sl = True, type = 'joint' )
	num = len(joints)
	
	
	#isolates the bottom most child joints in tsList
	i = 0
	#a = 0
	children = []
	while (i < num):
		pod = cmds.select( joints[i], hi = True )
		pods = cmds.ls( sl = True, type = 'joint' )
		hi = len(pods)
		f = 0
		b = 1
		while( f == 0 ):
			cmds.select(pods[hi-b], r = True)
			bottom = cmds.ls( sl = True )
			if any( ch in bottom for ch in joints):
				f = 1
			b += 1
		cmds.select( bottom, r = True )
		cmds.pickWalk( d = 'down' )
		bottom = cmds.ls( sl = True )
		children.append(str(bottom)[3:][:-2])
		i += 1
		
	#Babies!? Babies are childless.
	global babies
	babies = []
	for b in children:
		if b not in babies:
			babies.append(b)
	
	num = len(babies)
	i = 0
	while (i < num):
		babies[i] = str(babies[i])
		i += 1

	cmds.select( joints, r = True )
	cmds.select( babies, d = True )
	parents = cmds.ls( sl = True )

	n = len(parents)
	i = 0
	while( i < n ):
		child = cmds.pickWalk( parents[i], d = 'down' )
		cmds.select( parents[i], child, r = True )
		split()
		getBent()
		i += 1
	
	#organizes end controls that are not at root
	i = 0
	while( i < n ):
		cmds.select( '%s_segment_*_joint' % parents[i] )
		seg = []
		seg = cmds.ls( sl = True )
		segNum = len(seg)
		cmds.select( parents[i], r = True )
		pick = cmds.ls( sl = True )
		cmds.pickWalk( d = 'up' )
		check = cmds.ls( sl = True )
		endSeg = str(check[0])
		jointName = seg[0][:-16]
		if( pick != check ):
			if any( pa in check for pa in parents):
				cmds.parent( '%s_segment_%d_curve_tipClusterHandle_grp' % ( endSeg, segNum - 1 ), '%s_segment_%d_ikh' % ( endSeg, segNum - 1 ), '%s_ctrl' % jointName )
		i += 1
	
	#create ik/cluster groups
	i = 0
	while( i < n ):
		q = 0
		cmds.select( '%s_segment_*_joint' % parents[i] )
		segLen = ( len(cmds.ls( sl = True ) ) - 1 )			
		while( q < segLen - 1):
			global s
			s = cmds.intSliderGrp( "seg", q = True, v = True )
			tac = 1
			cmds.select( '%s_segment_*_joint' % parents[i] )
			segs = []
			segs = cmds.ls( sl = True )
			tac = 0
			if(q >= 9):
				tac = 1
			jointName = segs[q][:-16 - tac]
			cmds.select( '%s_segment_%d_curve_tipClusterHandle_grp' % ( jointName, (q + 1) ), '%s_segment_%d_curve_baseClusterHandle_grp' % ( jointName, (q + 2) ), '%s_segment_%d_ikh' % ( jointName, (q + 1) ), r = True )
			groupSpecial()
			q += 1
			
		x = ( s/2 ) - 1
		d = 0		
		#create constraints that control bend:
		#upper segment
		while ( d < ( s/2 ) - 1):
			y = (s / x) - 1
			W0 =  ( 1 / y )
			W1 = 1 - W0
			cmds.select( '%s_segment_*_joint' % parents[i] )
			tac = 0
			
			j = []
			j = cmds.ls( sl = True )
			j = str(j[1])
			tx = abs(cmds.getAttr( '%s.tx' % j ))
			ty = abs(cmds.getAttr( '%s.ty' % j ))
			tz = abs(cmds.getAttr( '%s.tz' % j ))

			if( tx > .001 ):
				prim = 'X'
			if( ty > .001):
				prim = 'Y'
			if( tz > .001 ):
				prim = 'Z'	
			
			if(s > 9):
				tac = 1
			segs = []
			segs = cmds.ls( sl = True )
			jointName = segs[q][:-16 - tac]
			
			#translate	
			cmds.parentConstraint( '%s_upper_ctrl_const_grp' % jointName, '%s_bendy_ctrl_const_grp' % jointName, '%s_segment_%d_ikh_grp' % (jointName, d + 1 ), mo = True, sr = ('x','y','z') ) ###Make sr = xyz - primary axis
			cmds.setAttr( '%s_segment_%d_ikh_grp_parentConstraint1.%s_upper_ctrl_const_grpW0' % (jointName, d + 1, jointName ), W0 )
			cmds.setAttr( '%s_segment_%d_ikh_grp_parentConstraint1.%s_bendy_ctrl_const_grpW1' % (jointName, d + 1, jointName ), W1 )
			
			#twist
			cmds.select( '%s_segment_%d_ikh' % (jointName, (d + 1)), r = True )
			cmds.rename( groupSpecial(), '%s_segment_%d_ikh_rot_grp' % ( jointName, (d + 1)) )
			cmds.select( '%s_segment_%d_ikh_rot_grp' % (jointName, (d + 1)), '%s_segment_%d_ikh' % (jointName, (d + 1)), r = True )
			nm_alignLRAs()
			
			cmds.createNode ('multiplyDivide', n = '%s_segment_%d_md' % (jointName, (d + 1)) )
			cmds.createNode ('addDoubleLinear', n = '%s_segment_%d_adl' % (jointName, (d + 1)) )
			cmds.createNode ('multDoubleLinear', n = '%s_segment_%d_twist_mdl' % (jointName, (d + 1)) )
			
			cmds.setAttr('%s_segment_%d_md.input2X' % (jointName, (d + 1)), W1 )
			cmds.setAttr('%s_segment_%d_md.input2Y' % (jointName, (d + 1)), W0 )
			
			cmds.connectAttr('%s_bendy_ctrl.rotate%s' % (jointName, prim), '%s_segment_%d_md.input1X' % (jointName, (d + 1)) )
			cmds.connectAttr('%s_ctrl.rotate%s' % (jointName, prim), '%s_segment_%d_md.input1Y' % (jointName, (d + 1)) )
			cmds.connectAttr('%s_segment_%d_md.outputX' % (jointName, (d + 1)), '%s_segment_%d_adl.input1' % (jointName, (d + 1)) )
			cmds.connectAttr('%s_segment_%d_md.outputY' % (jointName, (d + 1)), '%s_segment_%d_adl.input2' % (jointName, (d + 1)) )
			cmds.connectAttr('%s_twist_mdl.output' % jointName, '%s_segment_%d_twist_mdl.input1' % (jointName, (d + 1)) )
			cmds.connectAttr('%s_segment_%d_adl.output' % (jointName, (d + 1)), '%s_segment_%d_twist_mdl.input2' % (jointName, (d + 1)) )
			cmds.connectAttr('%s_segment_%d_twist_mdl.output' % (jointName, (d + 1)), '%s_segment_%d_ikh_rot_grp.rotate%s' % (jointName, (d + 1), prim) )
			
			x -= 1
			d += 1
		
		#lower segment
		x = ( s/2 ) - 1
		m = d + x
		while( d >= 1):
			y = (s / x) - 1
			W0 =  ( 1 / y )
			W1 = 1 - W0
			cmds.select( '%s_segment_*_joint' % parents[i] )

			if(s > 8):
				tac = 1
			segs = []
			segs = cmds.ls( sl = True )
			jointName = segs[q+1][:-16 - tac]

			cmds.select( jointName, r = True )
			cmds.pickWalk( d = 'down' )
			joint2Name = cmds.ls( sl = True )
			joint2Name = str(joint2Name)[3:][:-2]
			
			#translate
			cmds.parentConstraint( '%s_lower_ctrl_const_grp' % joint2Name, '%s_bendy_ctrl_const_grp' % jointName, '%s_segment_%d_ikh_grp' % (jointName, m + 1 ), mo = True, sr = ('x','y','z') )
			cmds.setAttr( '%s_segment_%d_ikh_grp_parentConstraint1.%s_lower_ctrl_const_grpW0' % (jointName, m + 1, joint2Name ), W0 )
			cmds.setAttr( '%s_segment_%d_ikh_grp_parentConstraint1.%s_bendy_ctrl_const_grpW1' % (jointName, m + 1, jointName ), W1 )
			
			#twist
			cmds.select( '%s_segment_%d_ikh' % (jointName, (m + 1)), r = True )
			cmds.rename( groupSpecial(), '%s_segment_%d_ikh_rot_grp' % ( jointName, (m + 1)) )
			cmds.select( '%s_segment_%d_ikh_rot_grp' % (jointName, (m + 1)), '%s_segment_%d_ikh' % (jointName, (m + 1)), r = True )
			nm_alignLRAs()
			
			cmds.createNode ('multiplyDivide', n = '%s_segment_%d_md' % (jointName, (m + 1)) )
			cmds.createNode ('addDoubleLinear', n = '%s_segment_%d_adl' % (jointName, (m + 1)) )
			cmds.createNode ('multDoubleLinear', n = '%s_segment_%d_twist_mdl' % (jointName, (m + 1)) )
			
			cmds.setAttr('%s_segment_%d_md.input2X' % (jointName, (m + 1)), W1 )
			cmds.setAttr('%s_segment_%d_md.input2Y' % (jointName, (m + 1)), W0 )
			
			cmds.connectAttr('%s_bendy_ctrl.rotate%s' % (jointName, prim), '%s_segment_%d_md.input1X' % (jointName, (m + 1)) )
			cmds.connectAttr('%s_ctrl.rotate%s' % (joint2Name, prim), '%s_segment_%d_md.input1Y' % (jointName, (m + 1)) )
			cmds.connectAttr('%s_segment_%d_md.outputX' % (jointName, (m + 1)), '%s_segment_%d_adl.input1' % (jointName, (m + 1)) )
			cmds.connectAttr('%s_segment_%d_md.outputY' % (jointName, (m + 1)), '%s_segment_%d_adl.input2' % (jointName, (m + 1)) )
			cmds.connectAttr('%s_twist_mdl.output' % jointName, '%s_segment_%d_twist_mdl.input1' % (jointName, (m + 1)) )
			cmds.connectAttr('%s_segment_%d_adl.output' % (jointName, (m + 1)), '%s_segment_%d_twist_mdl.input2' % (jointName, (m + 1)) )
			cmds.connectAttr('%s_segment_%d_twist_mdl.output' % (jointName, (m + 1)), '%s_segment_%d_ikh_rot_grp.rotate%s' % (jointName, (m + 1), prim) )
			
			d -= 1
			m -= 1
			x -= 1
		i += 1
	#group cluster and ikh for the last ctrl
	i = 0

	while( i < num ):
		cmds.select( babies[i], r = True )
		cmds.pickWalk( d = 'up' )
		babyMama = str(cmds.ls( sl = True ))[3:][:-2]
		cmds.select( '%s_segment_%d_curve_tipClusterHandle_grp' % (babyMama, s), '%s_segment_%d_ikh' % (babyMama, s), r = True )
		groupSpecial()
		cmds.parentConstraint( '%s_ctrl' % (babies[i]), '%s_segment_%d_ikh_grp' % (babyMama, s), mo = True, sr = ('x','y','z') )
		i += 1
		
	#middle segment
	i = 0
	if( s%2 == 0 ):
		cmds.select( joints, r = True )
		cmds.select( babies, d = True )
		parents = cmds.ls( sl = True )
		while ( i < n ):
			parent = parents[i]
			cmds.select( '%s_segment_*_joint' % parent )
			j = []
			j = cmds.ls( sl = True )
			j = str(j[1])
			tx = abs(cmds.getAttr( '%s.tx' % j ))
			ty = abs(cmds.getAttr( '%s.ty' % j ))
			tz = abs(cmds.getAttr( '%s.tz' % j ))

			if( tx > .001 ):
				prim = 'X'
			if( ty > .001):
				prim = 'Y'
			if( tz > .001 ):
				prim = 'Z'	

			#translate
			cmds.parentConstraint( '%s_bendy_ctrl_const_grp' % parent, '%s_segment_%d_ikh_grp' % ( parent, (s/2)), mo = True, sr = ('x','y','z') )
			
			#twist
			cmds.select( '%s_segment_%d_ikh' % ( parent, (s/2)), r = True )
			cmds.rename( groupSpecial(), '%s_segment_%d_ikh_rot_grp' % ( parent, (s/2)) )
			cmds.select( '%s_segment_%d_ikh_rot_grp' % ( parent, (s/2)), '%s_segment_%d_ikh' % ( parent, (s/2)), r = True )
			nm_alignLRAs()
			
			cmds.createNode ('multDoubleLinear', n = '%s_segment_%d_twist_mdl' % ( parent, (s/2)) )
			
			cmds.connectAttr('%s_twist_mdl.output' % parent, '%s_segment_%d_twist_mdl.input1' % ( parent, (s/2)) )
			cmds.connectAttr('%s_bendy_ctrl.rotate%s' % (parent, prim), '%s_segment_%d_twist_mdl.input2' % ( parent, (s/2)))
			cmds.connectAttr('%s_segment_%d_twist_mdl.output' % ( parent, (s/2)), '%s_segment_%d_ikh_rot_grp.rotate%s' % ( parent, (s/2), prim) )

			i += 1

	cmds.select( "*_segment_*_curve", r = True )
	curves = []
	curves = cmds.ls( sl = True )
	curveNum = len(curves)
	i = 0
	while( i < curveNum ):
		cmds.setAttr( '%s.inheritsTransform' % curves[i], 0 )
		i += 1

	if cmds.objExists( 'curve_segment_dnt_grp' ):
		cmds.parent( cmds.ls( sl = True ), 'curve_segment_dnt_grp' )
	else:
		cmds.group( n = 'curve_segment_dnt_grp' )

	
	#make joint_segment_grps
	i = 0
	while( i < n ):
		cmds.select( '%s_segment_*_ikh_grp' % parents[i], '%s_bendy_ctrl_orientPad' % parents[i], '%s_ctrl_orientPad' % parents[i], r = True )
		cmds.select( '%s_segment_1_ikh_grp' % parents[i], add = True )
		cmds.rename( groupSpecial(), '%s_segment_grp' % parents[i] )
		cmds.parentConstraint( parents[i], '%s_segment_grp' % parents[i], mo = True )
		i += 1
	i = 0
	while( i < num ):
		cmds.select( babies[i], r = True )
		cmds.pickWalk( d = 'up' )
		babyMama = str(cmds.ls( sl = True ))[3:][:-2]
		cmds.parent( '%s_ctrl_orientPad' % babies[i], '%s_segment_grp' % babyMama )
		i += 1
	
	if cmds.objExists( 'main_ctrl_const_grp' ):
		cmds.parent( '**_ctrl_const_grp_orientPad', 'main_ctrl_const_grp' )
	else:
		cmds.select( '**_ctrl_const_grp_orientPad', r = True )
		cmds.group ( n = 'main_ctrl_const_grp' )

	if cmds.objExists( 'main_segment_grp' ):
		cmds.select('**_segment_grp', r = True )
		cmds.select( 'main_segment_grp', d = True )
		grps = cmds.ls(sl = True)
		cmds.parent( grps, 'main_segment_grp' )
	else:
		cmds.select( '**_segment_grp', r = True )
		cmds.group( n = 'main_segment_grp' )

	i = 0
	elders = []
	while( i < n ):
		cmds.select( parents[i], r = True )
		b = 0
		while( b == 0 ):
			gp = cmds.ls( sl = True )
			cmds.pickWalk( d = 'up' )
			root = cmds.ls( sl = True )
			if( gp == root ):
				b = 1
		elders.append(root)
		i += 1
	roots = []
	for eld in elders:
		if eld not in roots:
			roots.append(eld)
			
	num = len(roots)
	i = 0
	while (i < num):
		roots[i] = str(roots[i])[3:][:-2]
		i += 1

	if( globalScale != '' ):	
		gs, sep, tail = globalScale.partition('.')	
		gsPos = cmds.xform( gs, q = True, piv = True, ws = True )
		if cmds.objExists( 'joint_scale_grp' ):
			cmds.parent( roots, 'joint_scale_grp' )
			cmds.select( 'joint_scale_grp', r = True )
			cmds.xform( os = True, piv = gsPos[0:3] )
		else:
			cmds.group( em = True, n = 'joint_scale_grp' )
			cmds.parent( roots, 'joint_scale_grp' )
			cmds.select( 'joint_scale_grp', r = True )
			cmds.xform( os = True, piv = gsPos[0:3] )
			cmds.parent( 'main_ctrl_const_grp', 'main_segment_grp', gs )
			cmds.scaleConstraint( gs, 'joint_scale_grp', mo = True )
		
	seg = cmds.intSliderGrp( "seg", q = True, v = True ) + 1
	cmds.select( '*_segment_*_joint', r = True )
	cmds.select( '*_segment_%d_joint' % seg, d = True )	
	if cmds.objExists( 'segmentBindSet' ):
		cmds.delete( 'segmentBindSet' )
		cmds.sets( n = 'segmentBindSet')
	else:
		cmds.sets( n = 'segmentBindSet' )
	
	print 'huzzah!'
	
def split():

	sel = []
	sel = cmds.ls( sl = True )
	
	global cir
	cir = cmds.floatSliderGrp( "fsg", q = True, v = True )
	
	#get the number of segments
	global seg
	seg = cmds.intSliderGrp( "seg", q = True, v = True )	
	
	#get the start and end position of the joint you want to segment
	start = cmds.xform( sel[0], q = True, piv = True, ws = True )
	end = cmds.xform( sel[1], q = True, piv = True, ws = True )
	s = start[0:3]
	e = end[0:3]
	name = '%s_segment_1_joint' % sel[0]
	rel = cmds.listRelatives( sel[0], p = True )
	
	#get the joints orientation
	#check to see if the joint has a parent
	if( rel is None ): #if it does
		startX = cmds.getAttr( '%s.jox' % sel[0] )
		startY = cmds.getAttr( '%s.joy' % sel[0] )
		startZ = cmds.getAttr( '%s.joz' % sel[0] )
	else:              #if it does not
		#create a joint to store the .jointOrientXY&Z values
		cmds.select( d = True )
		cmds.joint( p = (s), n = 'getInfo_joint' )
		cmds.orientConstraint( sel[0], 'getInfo_joint', mo = False )
		cmds.delete( 'getInfo_joint_orientConstraint1' )
		cmds.select( 'getInfo_joint', r = True )
		cmds.makeIdentity( a = True, r = True )
		
		startX = cmds.getAttr( 'getInfo_joint.jox' )
		startY = cmds.getAttr( 'getInfo_joint.joy' )
		startZ = cmds.getAttr( 'getInfo_joint.joz' )
		
		cmds.delete( 'getInfo_joint' )

	#create the start joint segment
	cmds.select( d = True )
	cmds.joint( p = (s), n = name)

	cmds.setAttr( ( '%s.jox' % name ), startX )
	cmds.setAttr( ( '%s.joy' % name ), startY )
	cmds.setAttr( ( '%s.joz' % name ), startZ )
	
	#create the middle joint segments
	i = 1
	seg = (seg - 1)
	while( i <= seg ):
		name = '%s_segment_%d_joint' % ( sel[0], (i + 1) )
		x = start[0] + ( i * (( end[0] - start[0]) / (seg + 1)))
		y = start[1] + ( i * (( end[1] - start[1]) / (seg + 1)))
		z = start[2] + ( i * (( end[2] - start[2]) / (seg + 1)))
		
		cmds.joint( p = (x,y,z), n = name )
		cmds.xform( cp = True )
		i += 1
		
	#create the end joint
	name = '%s_segment_%d_joint' % ( sel[0], (i + 1) )
	cmds.joint( p = e, n = name )
	
	#find the primary axis
	tx = abs(cmds.getAttr( '%s.tx' % sel[1] ))
	ty = abs(cmds.getAttr( '%s.ty' % sel[1] ))
	tz = abs(cmds.getAttr( '%s.tz' % sel[1] ))
	if( tx > 0.001 ):
		circleAxis = ( 1, 0, 0 )
		prim = 'X'
		ax1 = 'Z'
		ax2 = 'Y'
	if( ty > 0.001 ):
		circleAxis = ( 0, 1, 0 )
		prim = 'Y'
		ax1 = 'X'
		ax2 = 'Z'
	if( tz > 0.001 ):
		circleAxis = ( 0, 0, 1 )
		prim = 'Z'
		ax1 = 'X'
		ax2 = 'Y'

	#create/position the middle bendy control
	p1 = cmds.xform( sel[0], q = True, piv = True, ws = True )[0:3]
	p2 = cmds.xform( sel[1], q = True, piv = True, ws = True )[0:3]
	m = [p2 + p1 for p2, p1 in zip(p2, p1)]
	m = [x/2 for x in m]
	cmds.circle(n = '%s_bendy_ctrl' % sel[0], r = cir, nr = circleAxis, d = 3, s = 8 )
	cmds.xform( t = m, ws = True )
	cmds.orientConstraint( sel[0], '%s_bendy_ctrl' % sel[0], mo = False )
	cmds.delete( '%s_bendy_ctrl_orientConstraint1' % sel[0] )
	cmds.makeIdentity( a = True, t = True, r = True )
	cmds.delete( ch = True )
	cmds.select( sel[0], tgl = True )
	nm_alignLRAs()
	cmds.select( '%s_bendy_ctrl_orientPad' % sel[0], r = True )
	mel.eval('CenterPivot;')
	cmds.pointConstraint( sel[0], sel[1], '%s_bendy_ctrl_orientPad' % sel[0], mo = True )

	
	#create the ctrl_const_grp
	cmds.select( cl = True )
	cmds.group( em = True, n = '%s_bendy_ctrl_const_grp' % sel[0] )
	cmds.xform( t = m, ws = True )
	cmds.makeIdentity( a = True, t = True, r = True )
	cmds.select( '%s_bendy_ctrl_const_grp' % sel[0], '%s_bendy_ctrl' % sel[0], r = True )
	nm_alignLRAs()
	cmds.pointConstraint( '%s_bendy_ctrl' % sel[0], '%s_bendy_ctrl_const_grp_orientPad' % sel[0], mo = True )
	cmds.orientConstraint( '%s_bendy_ctrl' % sel[0], '%s_bendy_ctrl_const_grp' % sel[0], mo = True )
	cmds.connectAttr( '%s_bendy_ctrl.scale%s' % (sel[0], prim), '%s_bendy_ctrl_const_grp.scale%s' % (sel[0], prim) )
	cmds.setAttr( '%s_bendy_ctrl.scale%s' % (sel[0], ax1), l = True, k = False, cb = False )
	cmds.setAttr( '%s_bendy_ctrl.scale%s' % (sel[0], ax2), l = True, k = False, cb = False )

	
	#create twist attribute
	cmds.addAttr( '%s_bendy_ctrl' % sel[0], ln = 'twist', at = "double", min = 0, max = 10, dv = 10, k = True )
	cmds.createNode ('multDoubleLinear', n = '%s_twist_mdl' % sel[0] )
	cmds.connectAttr( '%s_bendy_ctrl.twist' % sel[0], '%s_twist_mdl.input1' % sel[0] )
	cmds.setAttr( '%s_twist_mdl.input2' % sel[0], 0.1 )
	
	
	#check to see if joint has a parent
	cmds.select( sel[0], r = True )
	pick = cmds.ls( sl = True )
	cmds.pickWalk( d = 'up' )
	check = cmds.ls( sl = True )
	cmds.select( sel[0], r = True )
	cmds.pickWalk( d = 'down' )
	down = cmds.ls( sl = True )
	p1 = cmds.xform( check, q = True, piv = True, ws = True )[0:3]
	p2 = cmds.xform( pick, q = True, piv = True, ws = True )[0:3]
	p3 = cmds.xform( down, q = True, piv = True, ws = True )[0:3]
	m = [p3 + p1 for p3, p1 in zip(p3, p1)]
	m = [x/2 for x in m]
	#v = [m - start for m, start in zip(m, start)]
	p1 = cmds.xform( check, q = True, piv = True, ws = True )[0:3]
	p3 = cmds.xform( down, q = True, piv = True, ws = True )[0:3]
	if( pick == check ):
		cmds.circle(n = '%s_ctrl' % sel[0], r = cir, nr = circleAxis, d = 3, s = 8 )
		cmds.delete( ch = True )
		cmds.parentConstraint( sel[0], '%s_ctrl' % sel[0], mo = False )
		cmds.delete( '%s_ctrl_parentConstraint1' % sel[0])
		cmds.select( '%s_ctrl' % sel[0], r = True )
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.select( '%s_ctrl' % sel[0], sel[0], r = True )
		nm_alignLRAs()
		cmds.setAttr( '%s_ctrl.scaleX' % sel[0], l = True, k = False, cb = False )
		cmds.setAttr( '%s_ctrl.scaleY' % sel[0], l = True, k = False, cb = False )
		cmds.setAttr( '%s_ctrl.scaleZ' % sel[0], l = True, k = False, cb = False )
		cmds.pointConstraint( sel[0], '%s_ctrl_orientPad' % sel[0], mo = True )
		
		#create the ctrl_const_grp
		cmds.select( cl = True )
		cmds.group( em = True, n = '%s_upper_ctrl_const_grp' % sel[0] )
		cmds.xform( t = p1, ws = True )
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.select( '%s_upper_ctrl_const_grp' % sel[0], '%s_ctrl' % sel[0], r = True )
		nm_alignLRAs()
		cmds.pointConstraint( '%s_ctrl' % sel[0], '%s_upper_ctrl_const_grp_orientPad' % sel[0], mo = True )
		cmds.select('%s_upper_ctrl_const_grp' % sel[0], r = True)
		cmds.rename( groupSpecial(), '%s_upper_ctrl_const_rot_grp' % sel[0] )
		cmds.connectAttr( '%s_ctrl.rotate' % sel[0], '%s_upper_ctrl_const_grp.rotate' % sel[0] )
		cmds.orientConstraint( sel[0], '%s_upper_ctrl_const_rot_grp' % sel[0], mo = True )
		
	if ( pick != check ):
		cmds.circle(n = '%s_ctrl' % sel[0], r = cir, nr = circleAxis , d = 3, s = 8 )
		cmds.delete( ch = True )
		cmds.setAttr( '%s_ctrl.scaleX' % sel[0], l = True, k = False, cb = False )
		cmds.setAttr( '%s_ctrl.scaleY' % sel[0], l = True, k = False, cb = False )
		cmds.setAttr( '%s_ctrl.scaleZ' % sel[0], l = True, k = False, cb = False )
		
		cmds.group( em = True, n = 'orient_grp' )
		cmds.delete( cmds.pointConstraint( sel[0], 'orient_grp' ) )
		cmds.select( 'orient_grp', sel[0], check, r = True )
		nm_align2LRAs()
		
		cmds.delete( cmds.pointConstraint( sel[0], '%s_ctrl' % sel[0] ) )
		cmds.delete( cmds.orientConstraint( 'orient_grp_orientPad', '%s_ctrl' % sel[0] ) )
		cmds.select( '%s_ctrl' % sel[0], r = True )
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.delete( 'orient_grp_orientPad')
		cmds.select( '%s_ctrl' % sel[0], sel[0], check, r = True )
		nm_align2LRAs()
		cmds.pointConstraint( sel[0], '%s_ctrl_orientPad' % sel[0], mo = True )
		
		#create the ctrl_const_grp
		cmds.select( cl = True )
		cmds.group( em = True, n = '%s_upper_ctrl_const_grp' % sel[0] )
		cmds.xform( t = p2, ws = True )
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.select( '%s_upper_ctrl_const_grp' % sel[0], '%s_ctrl' % sel[0], r = True )
		nm_alignLRAs()
		cmds.pointConstraint( '%s_ctrl' % sel[0], '%s_upper_ctrl_const_grp_orientPad' % sel[0], mo = True )
		cmds.select('%s_upper_ctrl_const_grp' % sel[0], r = True)
		cmds.rename( groupSpecial(), '%s_upper_ctrl_const_rot_grp' % sel[0] )
		cmds.connectAttr( '%s_ctrl.rotate' % sel[0], '%s_upper_ctrl_const_grp.rotate' % sel[0] )
		cmds.orientConstraint( sel[0], '%s_upper_ctrl_const_rot_grp' % sel[0], mo = True )
		
		cmds.select( cl = True )
		cmds.group( em = True, n = '%s_lower_ctrl_const_grp' % sel[0] )
		cmds.xform( t = p2, ws = True )
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.select( '%s_lower_ctrl_const_grp' % sel[0], '%s_ctrl' % sel[0], r = True )
		nm_alignLRAs()
		cmds.pointConstraint( '%s_ctrl' % sel[0], '%s_lower_ctrl_const_grp_orientPad' % sel[0], mo = True )
		cmds.select('%s_lower_ctrl_const_grp' % sel[0], r = True )
		cmds.rename( groupSpecial(), '%s_lower_ctrl_const_rot_grp' % sel[0] )
		cmds.connectAttr( '%s_ctrl.rotate' % sel[0], '%s_lower_ctrl_const_grp.rotate' % sel[0] )
		cmds.orientConstraint( str(check)[3:][:-2], '%s_lower_ctrl_const_rot_grp' % sel[0], mo = True )

	#create/position the end bendy control
	cmds.select( down, r = True )
	cmds.pickWalk( d = 'down' )
	dd = cmds.ls( sl = True )
	if any( j in str(down)[3:][:-2] for j in babies ):
		cmds.circle(n = '%s_ctrl' % sel[1], r = cir, nr = circleAxis, d = 3, s = 8 )
		cmds.xform( t = p3, ws = True )
		cmds.orientConstraint( sel[0], '%s_ctrl' % sel[1], mo = False )
		cmds.delete( '%s_ctrl_orientConstraint1' % sel[1])
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.select ( '%s_ctrl' % sel[1], sel[1], r = True )
		nm_alignLRAs()
		cmds.setAttr( '%s_ctrl.scaleX' % sel[1], l = True, k = False, cb = False )
		cmds.setAttr( '%s_ctrl.scaleY' % sel[1], l = True, k = False, cb = False )
		cmds.setAttr( '%s_ctrl.scaleZ' % sel[1], l = True, k = False, cb = False )
		cmds.pointConstraint( sel[1], '%s_ctrl_orientPad' % sel[1], mo = True )
		
		#create the ctrl_const_grp
		cmds.select( cl = True )
		cmds.group( em = True, n = '%s_lower_ctrl_const_grp' % sel[1] )
		cmds.xform( t = p3, ws = True )
		cmds.makeIdentity( a = True, t = True, r = True )
		cmds.select( '%s_lower_ctrl_const_grp' % sel[1], '%s_ctrl' % sel[1], r = True )
		nm_alignLRAs()
		cmds.pointConstraint( '%s_ctrl' % sel[1], '%s_lower_ctrl_const_grp_orientPad' % sel[1], mo = True )
		cmds.select('%s_lower_ctrl_const_grp' % sel[1], r = True )
		cmds.rename( groupSpecial(), '%s_lower_ctrl_const_rot_grp' % sel[1] )
		cmds.connectAttr( '%s_ctrl.rotate' % sel[1], '%s_lower_ctrl_const_grp.rotate' % sel[1] )
		cmds.orientConstraint( sel[0], '%s_lower_ctrl_const_rot_grp' % sel[1], mo = True )

		
	#select the segments of the current bone
	cmds.select( '%s_segment_*_joint' % sel[0] )

	
def getBent():
	sel = []
	sel = cmds.ls( sl = True )
	size = len(sel)

	i = 0
	while( i < size - 1 ):
		start = cmds.xform( sel[i], q = True, piv = True, ws = True )
		end = cmds.xform( sel[i + 1], q = True, piv = True, ws = True )
		s = start[0:3]
		e = end[0:3]
		name = sel[i][:-6]
		jointName = sel[0][:-16]
		cmds.select( sel[0][:-16], r = True )
		cmds.pickWalk( d = 'down' )
		joint2Name = str(cmds.ls( sl = True ))[3:][:-2]
		infoName = '%s_curveInfo' % name
		curve = '%s_curve' % name
		cmds.curve( n = curve, d = 1, ep = ( s, e ) )
		
		sx = int(round(cmds.getAttr( '%s.tx' % joint2Name )))
		sy = int(round(cmds.getAttr( '%s.ty' % joint2Name )))
		sz = int(round(cmds.getAttr( '%s.tz' % joint2Name )))

		if( sx != 0 ):
			scale = 'X'
		if( sy != 0 ):
			scale = 'Y'
		if( sz != 0 ):
			scale = 'Z'		
	
		#create curve info node
		cmds.select( curve, r = True )
		info = cmds.arclen( ch = True )
		cmds.rename( info, infoName )
		arcLen = cmds.getAttr( '%s.arcLength' % infoName )
		
		#create the IKH
		cmds.ikHandle( sol = "ikSCsolver", sj = sel[i], ee = sel[i + 1], s = 'sticky', n = '%s_ikh' % name )
	
		#create clusters for stretch
		cmds.select( curve + '.cv[0]', r = True )
		cmds.cluster( n = '%s_baseCluster' % curve )
		groupSpecial()
		cmds.select( curve + '.cv[1]', r = True )
		cmds.cluster( n = '%s_tipCluster' % curve )
		groupSpecial()

		#create/connect multiplyDivide nodes for stretch
		cmds.createNode ('multiplyDivide', n = '%s_stretch_md' % name )
		cmds.createNode ('multiplyDivide', n = '%s_normalizeScale_md' % name )
		cmds.setAttr( '%s_stretch_md.operation' % name,2 )
		cmds.setAttr( '%s_stretch_md.input2X' % name, arcLen )
		cmds.setAttr( '%s_normalizeScale_md.operation' % name, 2 )
		cmds.connectAttr( infoName + '.arcLength', '%s_stretch_md.input1X' % name, force = True )
		cmds.connectAttr( '%s_stretch_md.outputX' % name, '%s_normalizeScale_md.input1X' % name, force = True )
		cmds.connectAttr( '%s_normalizeScale_md.outputX' % name, '%s.scale%s' % (sel[i], scale) )
		if( globalScale != '' ):
			cmds.connectAttr( globalScale, '%s_normalizeScale_md.input2X' % name, force = True )
		
		cmds.select( sel[0], r = True )
		pick = cmds.ls( sl = True )
		cmds.pickWalk( d = 'up' )
		check = cmds.ls( sl = True )
		if( i == 0 and pick == check):
			ctrl = sel[0][:-16]
			cmds.parent( '%s_baseClusterHandle_grp' % curve, sel[0], '%s_ctrl' % jointName )
		i += 1


		
def nm_alignLRAs():
	sel = []
	sel = cmds.ls( sl = True )
	ctrl = sel[0]
	joint = sel[1]
	
	rememberPad = cmds.group( ctrl, n = ctrl + '_rememberPad' )
	orientPad = cmds.createNode( 'transform', n = ctrl + '_orientPad' ) 
	cmds.delete( cmds.parentConstraint( joint, orientPad ) )
	cmds.parent( orientPad, rememberPad )
	cmds.parent( ctrl, orientPad )
	cmds.makeIdentity( ctrl, a = True, t = 1, r = 1, n = 0)
	cmds.ungroup( rememberPad )
	
def nm_align2LRAs():
	sel = []
	sel = cmds.ls( sl = True )
	ctrl = sel[0]
	joint = sel[1]
	joint2 = sel[2]
	
	rememberPad = cmds.group( ctrl, n = ctrl + '_rememberPad' )
	orientPad = cmds.createNode( 'transform', n = ctrl + '_orientPad' ) 
	cmds.delete( cmds.pointConstraint( joint, orientPad ) )
	cmds.delete( cmds.orientConstraint( joint, joint2, orientPad ) )
	cmds.parent( orientPad, rememberPad )
	cmds.parent( ctrl, orientPad )
	cmds.makeIdentity( ctrl, a = True, t = 1, r = 1, n = 0)
	cmds.ungroup( rememberPad )
	
def groupSpecial():
	sel = []
	sel = cmds.ls( sl = True )
	selSize = len(sel)

	lastPos = cmds.xform( sel[selSize - 1], q = True, piv = True, ws = True )
	lPoints  = lastPos[0:3]

	cmds.group( n = sel[selSize - 1] + '_grp' )
	cmds.xform(  ws = True, piv = lPoints )