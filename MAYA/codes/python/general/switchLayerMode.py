import pymel.core as pm



class SwitchLayerMode():
	'''
	Switches all display layer's state, between Normal, Reference and Template.
	'''

	layerMode = 0 # holds layer's current state, 0 ( Normal ), 1 ( Reference ) and 2 ( Template ) 
	
	def __init__( self, *args ):
		self.switchLayerMode()
	
	def switchLayerMode( self, *args ):
		
		layers = pm.ls(type='displayLayer')
		
		layers.remove( pm.PyNode( 'defaultLayer' ) )
		
		if len(layers): # if any layer found, get first layer's displayType
			self.layerMode = layers[0].displayType.get()
		else:
			pm.warning( 'There is no layer to change it\'s state.')
			return None
		
		for layer in layers: # switch layer's mode
			if self.layerMode == 0:
				layer.displayType.set( 1 )
			elif self.layerMode == 1:
				layer.displayType.set( 2 )
			elif self.layerMode == 2:
				layer.displayType.set( 0 )
		
		if self.layerMode > 2: # switch between 0 ( Normal ), 1 ( Reference ) and 2 ( Template ) mode for layers
			self.layerMode = 0
		else:
			self.layerMode *= 1