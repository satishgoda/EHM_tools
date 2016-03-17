import pymel.core as pm



class SwitchObjectDisplayMode():
	'''
	Switches selected or all objects' display mode, between Normal, Reference and Template.
	'''
	mode = 0


	# holds obj's current state, 0 ( Normal ), 1 ( Reference ) and 2 ( Template ) 
	
	def __init__( self, *args ):
		self.switchObjectDisplayMode()
	
	
	def switchObjectDisplayMode( self, *args ):
		
		objs = pm.ls( sl=True )
		if not objs:
			objs = pm.ls( type="transform" )
		
		
		# get first obj's displayType
		self.overrideMode = objs[0].overrideEnabled.get()
		self.displayMode = objs[0].overrideDisplayType.get()
		
		for obj in objs: # switch obj's mode
			
			try:
				if self.overrideMode and self.displayMode==2: # if first object's override is ON, turn all OFF
					obj.overrideEnabled.set( 0 )
				
				else: # if first object's override is OFF, turn all ON
					obj.overrideEnabled.set( 1 )

					if self.displayMode == 1:
						obj.overrideDisplayType.set( 2 )
					
					elif self.displayMode == 2:
						obj.overrideDisplayType.set( 1 )
			except:
				pm.warning( '%s is inside a display layers. Remove it from layers and try again.'%( obj.name() ) )