#=================================================================================
'''
Script Name: poser

Author: Ehsan HM - hm.ehsan@yahoo.com

What does it do?
	helps to select all animatable controls of characters. Mirror, Flip or resetAll poses

How does it work?
	select at least one control on your character, then try UI buttons.
	
'''
#=================================================================================


import pymel.core as pm
from functools import partial

from codes.python.rig import matchTransform
MatchTransform = matchTransform.MatchTransform

class Poser():
	
	# list of node types that if are connected as input to our attributes, we can still change the attributes' values
	alterableInputTypes = pm.nodeType( 'animCurve', derived=True, isTypeName=True )
	alterableInputTypes.append( 'character' )
	
	def __init__(self, UI=True, *args, **kwargs):
	
		if UI:
			self.UI()
		
	
	def UI(self):
		
		# create window
		if pm.window( 'ehm_Poser_UI', exists=True ):
			pm.deleteUI( 'ehm_Poser_UI' )
		pm.window( 'ehm_Poser_UI', title='Pose Tools', w=400, h=235, mxb=False, mnb=True, sizeable=True )
		
		# main layout
		#mainLayout = pm.rowColumnLayout()
		formLayout = pm.formLayout(w=400, h=235)
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)
		pm.setParent( formLayout )
			
		
		# select and default buttons
		self.selectAndDefaultText = pm.text(label='Selection: ', align='right')
		self.selectAllButton = pm.button( label='Select All', h=30, backgroundColor=[0.5,0.7,0.5],  c= self.selectAllControls  )			
		self.setDefaultButton = pm.button( label='Set Default Pose',  h=30, backgroundColor=[0.5,0.7,0.5],  c=self.setDefaultPose  )			
		
		
		# reset buttons
		self.resetText = pm.text(label='Resets: ', align='right')		
		self.resetAllButton = pm.button( label='Reset All Attributes',  h=30, backgroundColor=[0.7,0.5,0.5], c=self.resetAllAttributes  )
		self.resetSRTButton = pm.button( label='Reset SRT',  h=30, backgroundColor=[0.7,0.5,0.5], c=self.resetTransformAttributes  )
		
		
		# reset and mirror mode separator 
		self.resetMirrorSEP = pm.separator( style='out' )
		
		# mirror mode radio buttons
		self.mirrorModeText = pm.text(label='Mirror Mode: ', align='right')
		self.mirrorModeRC = pm.radioCollection()
		self.behaviorRB = pm.radioButton(label="Behavior", select=True )
		self.orientationRB = pm.radioButton(label="Orientation")
		self.hybridRB = pm.radioButton(label="Hybrid")		
		
		
		# flip and mirror buttons
		self.mirrorText = pm.text(label='Mirror: ', align='right')	
		self.flipButton = pm.button( label='Flip', h=30, backgroundColor=[0.5,0.5,0.7],  c=partial( self.flip_pose, True )   )
		self.mirrorButton = pm.button( label='Mirror', h=30, backgroundColor=[0.5,0.5,0.7],  c=partial( self.mirror_pose, True )  )
		
		
		# match FK IK separator 
		self.matchFKIKSEP = pm.separator( style='out' )		
		
		
		# match FK IK buttons
		self.matchFKIKText = pm.text(label='Match FK IK: ', align='right')	
		self.matchFKIKButton = pm.button( label='FK <---> IK   ,   IK <---> FK', h=30, backgroundColor=[0.4,0.3,0.6],  c = self.matchFKIK   )
		
		
		# place frame layout
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'left', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'right', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'bottom', 3) )

		
		# place select and default buttons
		pm.formLayout( formLayout, edit=True, attachPosition=(self.selectAndDefaultText,'right', 0 , 20) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.selectAndDefaultText,'top', 30) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.selectAllButton,'left', 2 , 30) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.selectAllButton,'right', 2 , 65) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.selectAllButton,'top', 20) )		

		pm.formLayout( formLayout, edit=True, attachPosition=(self.setDefaultButton,'left', 2, 65) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.setDefaultButton,'right', 8, 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.setDefaultButton,'top', 20) )	

		# palce reset buttons		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetText,'right', 0 , 20) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.resetText,'top', 65) )		
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetAllButton,'left', 2, 30) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetAllButton,'right', 2 , 65) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.resetAllButton,'top', 55) )
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetSRTButton,'left', 2, 65) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetSRTButton,'right', 8 , 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.resetSRTButton,'top', 55) )	
		

		# place reset and mirror mode separator 
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetMirrorSEP,'left', 2, 1) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.resetMirrorSEP,'right', 2 , 99) )		
		pm.formLayout( formLayout, edit=True, attachForm=(self.resetMirrorSEP,'top', 105) )

		
		# place mirror mode radio buttons
		pm.formLayout( formLayout, edit=True, attachPosition=(self.mirrorModeText,'right', 0 , 20) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.mirrorModeText,'top', 115) )
				
		pm.formLayout( formLayout, edit=True, attachPosition=(self.behaviorRB,'left', 2, 30) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.behaviorRB,'right', 2 , 55) )		
		pm.formLayout( formLayout, edit=True, attachForm=(self.behaviorRB,'top', 115) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.orientationRB,'left', 2, 55) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.orientationRB,'right', 8 , 80) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.orientationRB,'top', 115) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.hybridRB,'left', 2, 80) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.hybridRB,'right', 8 , 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.hybridRB,'top', 115) )			
		
		
		# palce mirror buttons		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.mirrorText,'right', 0 , 20) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.mirrorText,'top', 145) )						
		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.flipButton,'left', 2,30) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.flipButton,'right', 2,65) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.flipButton,'top', 135) )

		
		pm.formLayout( formLayout, edit=True, attachPosition=(self.mirrorButton,'left', 2, 65) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.mirrorButton,'right', 8 , 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.mirrorButton,'top', 135) )
		

		#  place match FKIK separator
		pm.formLayout( formLayout, edit=True, attachPosition=(self.matchFKIKSEP,'left', 2, 1) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.matchFKIKSEP,'right', 2 , 99) )		
		pm.formLayout( formLayout, edit=True, attachForm=(self.matchFKIKSEP,'top', 180) )		

		
		# place match FK IK buttons
		pm.formLayout( formLayout, edit=True, attachPosition=(self.matchFKIKText,'right', 2 , 20) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.matchFKIKText,'top', 200) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.matchFKIKButton,'left', 2, 30) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.matchFKIKButton,'right', 8 , 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.matchFKIKButton,'top', 195) )

		# show window
		pm.showWindow( 'ehm_Poser_UI' )


	# set default values for all selected objects' attributes	
	def resetAllAttributes(self,*args):
		
		objs = pm.ls( sl=True )

		for obj in objs:
			
			allAttrs = pm.listAttr( obj, keyable=True, unlocked=True )
			userAttrs =  pm.listAttr(obj, ud=True, unlocked=True)
			
			for attr in allAttrs:
				
				# if attribute has incomming connections, go to next attribute, unless incomming connections is comming from character set
				inConnections = pm.listConnections( obj.attr(attr), d=False, s=True )
				if inConnections:
					if not ( self.alterableInputTypes ): 
						continue
				
				if attr not in userAttrs:# match main attributes
					try:
						if attr == 'visibility':
							pass
						elif ('scale' in attr.lower() ) :
							obj.attr(attr).set( 1 )
						else:
							obj.attr(attr).set( 0 )
					except:
						pm.warning( "ehm_tools...resetAllPose: Could not resetAll some of transform attributes, skipped! \t %s" %obj )
				else:# find and resetAll user defined attributes
					try:
						# pass typed attributes
						typed = pm.addAttr( obj.attr(attr), q=True, attributeType=True )
						if typed == 'typed': 
							continue
						# get default value and set it
						value = pm.addAttr( obj.attr(attr), q=True, defaultValue=True )	
						obj.attr(attr).set( value )
					except:
						pm.warning( "ehm_tools...resetAllPose: Could not resetAll some of user defined attributes, skipped! \t %s" %obj )
	
	

		# set default values for all selected objects' attributes	
	def resetTransformAttributes(self,*args):
		
		objs = pm.ls( sl=True )

		for obj in objs:
			
			allAttrs = pm.listAttr( obj, keyable=True, unlocked=True )
			userAttrs =  pm.listAttr(obj, ud=True, unlocked=True)
			
			for attr in allAttrs:
				
				# if attribute has incomming connections, go to next attribute, unless incomming connections is comming from character set
				inConnections = pm.listConnections( obj.attr(attr), d=False, s=True )
				if inConnections:
					if not ( self.alterableInputTypes ): 
						continue
				
				if attr not in userAttrs:# match main attributes
					try:
						if attr == 'visibility':
							pass
						elif ('scale' in attr.lower() ) :
							obj.attr(attr).set( 1 )
						else:
							obj.attr(attr).set( 0 )
					except:
						pm.warning( "ehm_tools...resetAllPose: Could not resetAll some of transform attributes, skipped! \t %s" %obj )
				else:# do not reset user defined attributes
					continue



	
	# get top parent
	def topParent( self, obj, *args ):
		tempFather = obj.getParent()
		father = None
		while tempFather:
			father = tempFather
			tempFather = tempFather.getParent()
		return father

	# get all name spaces
	def getNameSpace( self, obj, *args ):
		objName = obj.name()
		if len( objName.split(':') ) > 1 :
			return objName.split(':')[0]
		else:
			return None

	# find and select all animatable controls based on selected object
	def selectAllControls( self, objs=None, method='hierarchy', suffix='ctrl', *args ):
		
		suffixes = [ 'ctrl', 'Ctrl', 'CTRL', 'anim', 'Anim' ]
		
		if not objs:
			objs = pm.ls( sl=True )
		else:
			objs = pm.ls( objs )
		

		objList = []
		if method == 'reference': # select all animatable control and joints in the same referenced character
			for obj in objs:
				# guess control suffix accoriding to selection, else uses 'ctrl' suffix
				guessedSuffix = obj.name()[-4:]
				if guessedSuffix in suffixes:
					suffix = guessedSuffix
				
				character = self.getNameSpace( obj )				
				if character:
					objList.append( pm.ls( ( '%s:*_%s'%(character,suffix) ), type=['transform', 'joint'] ) )
					# objList.append( pm.ls( ( '%s:*_%s'%(character,suffix[0].lower(),suffix[1:]) ), type=['transform', 'joint'] ) )
				else:
					objList.append( obj )
		
		elif method == 'hierarchy': # select all animatable control and joints in the same hierarchy of selected object
			fathers = []
			for obj in objs:
				# guess control suffix accoriding to selection, else uses 'ctrl' suffix
				guessedSuffix = obj.name()[-4:]
				if guessedSuffix in suffixes:
					suffix = guessedSuffix
				
				father = self.topParent( obj )
				if not father: # if selected object is the same as top parent, take it as top parent
					father = obj
				if father not in fathers: # don't loop through same character over and over
					neighbours =  pm.listRelatives( father , ad=True, type=['transform', 'joint'] )			
					neighbours.append( father )
					for neighbour in neighbours:
						if neighbour.name().rpartition( suffix )[-2] == suffix and not neighbour.name().rpartition( suffix )[-1] : # find '*suffix' not '*suffix*'
							objList.append( neighbour )
						else:
							objList.append( obj )	
					fathers.append( father ) # don't loop through same character over and over
		pm.select( objList )

	# find object's mirrored object, if None found, return object itself
	def findMirror( self, obj, *args ):
		prefixes = { 'L_':'R_', 'Lf':'Rt' }
	
		nameSpaceAndName = obj.name().split(":")
		if len( nameSpaceAndName ) > 1:
			objNameSpace = nameSpaceAndName[0]
			objName = nameSpaceAndName[1]
		else:
			objName = obj.name()
		
		name = None
		for i in prefixes: # If prefix 'L_', finds 'R_'. If prefix 'Lf', finds 'Rt' and so on
			if objName[:2]==i and pm.objExists( obj.name().replace(i,prefixes[ i ]) ) : 
				name = obj.name().replace(i,prefixes[ i ])
			elif objName[:2]==prefixes[ i ] and pm.objExists( obj.name().replace(prefixes[ i ],i) ) :
				name = obj.name().replace(prefixes[ i ],i)
			if name:
				break
		if not name:
			#name = obj.name()
			return None
		
		return name


	# create a locator under given object and resets it's transforms
	def createChildLoc( self, father, *args ):
		loc = pm.spaceLocator()
		pm.parent( loc, father )
		loc.translate.set( 0,0,0 )
		loc.rotate.set( 0,0,0 )
		return loc		
		
		
	# takes current values from user defined attributes and sets it as the default value for them.
	def setDefaultPose( self,*args):

		objs = pm.ls( sl=True )

		for obj in objs:
			
			allAttrs = pm.listAttr( obj, keyable=True, unlocked=True )
			userAttrs =  pm.listAttr(obj, ud=True, unlocked=True)
			
			for attr in allAttrs:
				if pm.connectionInfo( obj.attr(attr), isDestination=True ):
					pass
				if attr in userAttrs:# match main attributes
					try:
						value = obj.attr(attr).get()
						pm.addAttr( obj.attr(attr) , e=True, dv=value )
					except:
						pm.warning( "ehm_tools...setDefaultPose: Could not set some of user defined attributes, skipped! \t %s" %obj )


	def matchFKIK( self, objs=None, *args ):					
		objs = pm.ls( sl=True )
		
				
		for obj in objs:
			name = obj.name()
			
			# find out whether "FK" and "IK" in control names is lower case or upper case
			if ('IK' in name) or ('FK' in name):
				IK = 'IK'
				FK = 'FK'
			elif ('ik' in name) or ('fk' in name):
				IK = 'ik'
				FK = 'fk'
			else:
				pm.warning( "Make sure your controls have 'IK' or 'FK' in their name" )
				continue
			
			
			if IK in name: # IKtoFK
				try:
					MatchTransform( folower=obj, lead=pm.PyNode(name.replace(IK,FK))  )	
				except:
					pass #pm.error( "The only difference between IK and FK control names must be 'IK' and 'FK', for example: 'L_hand_IK_ctrl' and 'L_hand_FK_ctrl'." )
			
			elif FK in name: # FKtoIK
				try:
					obj.rotate.set( pm.PyNode(name.replace('FK_ctrl','IK_jnt')).rotate.get() )
					obj.scale.set( pm.PyNode(name.replace('FK_ctrl','IK_jnt')).scale.get() )
				except:
					try:
						obj.rotate.set( pm.PyNode(name.replace('FK_ctrl','IK_jnt')).rotate.get() )
						obj.length.set( pm.PyNode(name.replace('FK_ctrl','IK_jnt')).scaleX.get() )					
					except:
						pm.error( "The only difference between FK control and IK joint names must be 'FK_ctrl' and 'IK_jnt', for example: 'L_hand_FK_ctrl' and 'L_hand_IK_jnt'." )
		
	
	def mirror_pose( self, mirrorMode='behavior', *args ):

		
		try:
			selectedItem = pm.radioCollection( self.mirrorModeRC, q=True, select=True )
			mirrorModeInUI = (pm.radioButton( selectedItem, q=True, label=True )).lower()
		except:
			pass
		
		objs = pm.ls( sl=True )

		for obj in objs:
			name = self.findMirror( obj ) # find mirrored object's name
			
			if not name:
				continue
			
			mirrorMode = mirrorModeInUI
			mirrorModeAttrExists = pm.attributeQuery( 'mirrorMode', node=obj, exists=True )
			if mirrorModeAttrExists:
				mirrorMode = obj.mirrorMode.get()
			
			
			# get object's attributes
			allAttrs = pm.listAttr( obj, keyable=True, unlocked=True )
			userAttrs =  pm.listAttr(obj, ud=True, unlocked=True)
					
			for attr in allAttrs:
				if pm.connectionInfo( pm.PyNode(name).attr(attr), isDestination=True ):
					pass  				
				if attr not in userAttrs:# match main attributes
					try:
						value = obj.attr(attr).get()
						
						if attr == 'visibility': # no need to mirror visibility
							pass
						
						elif attr=='translateX': # translate x is always reversed
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( -value )							
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( -value )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )							
				
						elif attr=='translateY': # translate x is always reversed
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( -value )							
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( value )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )							
						
						elif attr=='translateZ': # translate x is always reversed
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( -value )							
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( value )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )							
						
						elif attr=='rotateX':
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( value )							
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( value )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
						
						elif attr=='rotateY':
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( value )							
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( -value )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( value )
						
						elif attr=='rotateZ':
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( value )							
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( -value )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
												
						else:
							pm.PyNode(name).attr(attr).set( value )
					
					except:
						pm.error('ehm_tools...mirrorPose: Mirror failed on main attributes!')

				
				for userAttr in userAttrs:# find and match user defined attributes
					try:
						value = obj.attr(userAttr).get()
						pm.PyNode(name).attr(userAttr).set( value )
					except:
						pm.error('ehm_tools...mirrorPose: Mirror failed on user defined attributes!')    
				

	def flip_pose( self, mirrorMode=True, *args ):
		
		try:
			selectedItem = pm.radioCollection( self.mirrorModeRC, q=True, select=True )
			mirrorModeInUI = (pm.radioButton( selectedItem, q=True, label=True )).lower()
		except:
			pass

		objs = pm.ls( sl=True )

		flippedObjs = [] # list of objects already flipped
		
		for obj in objs:
			
			mirrorMode = mirrorModeInUI
			mirrorModeAttrExists = pm.attributeQuery( 'mirrorMode', node=obj, exists=True )
			if mirrorModeAttrExists:
				mirrorMode = obj.mirrorMode.get()

			name = self.findMirror( obj ) # find mirrored object's name
			
			if name in flippedObjs: # prevent object to get flipped twice
				continue
			flippedObjs.append( obj )				

			# get object's attributes
			allAttrs = pm.listAttr( obj, keyable=True, unlocked=True )
			userAttrs =  pm.listAttr(obj, ud=True, unlocked=True)

			
			if not name: # if mirror not found go to next object

				# 1. create 3 locators representing Position, aimVector and upVector
				pos = self.createChildLoc( obj )
				aim = self.createChildLoc( obj )
				upv = self.createChildLoc( obj )


				# 2. get the flip plane from our control object, default is YZ. place aim and up vectors accordingly
				try:
					flipPlane = obj.mirrorPlane.get()
				except:
					flipPlane = 'YZ'

				if flipPlane == 'YZ':
					aim.translateZ.set(1)
					upv.translateY.set(1)
					
				elif flipPlane == 'XZ':
					aim.translateX.set(1)
					upv.translateZ.set(1)
					
				elif flipPlane == 'XY':
					aim.translateX.set(1)
					upv.translateY.set(1)


				# 3. parent locators under control's parent. They should be in the same group as our control object we want to flip

				try:
					controlParent = obj.getParent() 
				except:
					controlParent = None

				if controlParent:
					pm.parent( pos, controlParent )
					pm.parent( aim, controlParent )
					pm.parent( upv, controlParent )


				# 4. group all locators and scale the group according to our flip plane

				grp = pm.group( pos, aim, upv )
				pm.xform( grp, os=True, piv=(0,0,0) )

				if flipPlane == 'YZ':
					grp.scaleX.set(-1)
				elif flipPlane == 'XZ':
					grp.scaleY.set(-1)	
				elif flipPlane == 'XY':
					grp.scaleZ.set(-1)



				# 5. create point and aim constraints to achieve the pose on a null object and apply the values to our control

				result = pm.group( empty=True )

				result.rotateOrder.set( obj.rotateOrder.get() )

				if controlParent:
					pm.parent( result, controlParent )
				pm.pointConstraint( pos, result )

				if flipPlane == 'YZ':
					pm.aimConstraint( aim, result, aimVector=[0,0,1], upVector=[0,1,0], worldUpType="object", worldUpObject=upv  )
				elif flipPlane == 'XZ':
					pm.aimConstraint( aim, result, aimVector=[1,0,0], upVector=[0,0,1], worldUpType="object", worldUpObject=upv  )
				elif flipPlane == 'XY':
					pm.aimConstraint( aim, result, aimVector=[1,0,0], upVector=[0,1,0], worldUpType="object", worldUpObject=upv  )

				result.scale.set( obj.scale.get() )


				# get object's attributes
				allAttrs = pm.listAttr( obj, keyable=True, unlocked=True )
				userAttrs =  pm.listAttr(obj, ud=True, unlocked=True)

				for attr in allAttrs:
					try:
						obj.attr(attr).set( result.attr(attr).get() )
					except:
						continue

				
				# 6. delete extra nodes
				pm.delete( grp, result )
				continue
			
			
			
			for attr in allAttrs:
				if pm.connectionInfo( pm.PyNode(name).attr(attr), isDestination=True ):
					pass  				
				if attr not in userAttrs:# match main attributes
					try:
						otherValue = pm.PyNode(name).attr(attr).get()
						value = obj.attr(attr).get()					
						if attr == 'visibility': # no need to mirror visibility
							pass
						
						elif attr=='translateX': # translate x is always reversed
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( -value )					
								obj.attr(attr).set( -otherValue )
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
						
						elif attr=='translateY': # translate x is always reversed
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( -value )					
								obj.attr(attr).set( -otherValue )
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
							
						elif attr=='translateZ': # translate x is always reversed
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( -value )					
								obj.attr(attr).set( -otherValue )
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )				
						
						elif attr=='rotateX':
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
						
						elif attr=='rotateY':
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )
						
						elif attr=='rotateZ':
							if mirrorMode=='behavior':
								pm.PyNode(name).attr(attr).set( value )
								obj.attr(attr).set( otherValue )								
							elif mirrorMode=='orientation':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
							elif mirrorMode=='hybrid':
								pm.PyNode(name).attr(attr).set( -value )
								obj.attr(attr).set( -otherValue )
						
						else:
							pm.PyNode(name).attr(attr).set( value )
							obj.attr(attr).set( otherValue )		

					except:
						pm.error('ehm_tools...mirrorPose: Flip failed on main attributes!')

				
				else:#  match user defined attributes
					try:
						otherValue = pm.PyNode(name).attr(attr).get()
						value = obj.attr(attr).get()
						pm.PyNode(name).attr(attr).set( value )					
						obj.attr(attr).set( otherValue )
					except:
						pm.error('ehm_tools...mirrorPose: Flip failed on user defined attributes!')    
						
		pm.select( objs )