from Pythons import log 

class Component( object ):


	def __init__( self, builder, guide ):

		log( '===========================Creating Component==============================' )

		self.builder = builder
		self.guide = guide
		self.settings = self.guide.settings
		self.model = self.builder.model

		self.hidden_grp = self.builder.hidden_grp
		self.unselectable_grp = self.builder.unselectable_grp
		self.controllers_grp = self.builder.controllers_grp
		self.deformers_grp = self.builder.deformers_grp

		self.deformers_org = self.builder.deformers_org

		self.name = self.guide.name
		self.location =  self.guide.location

		self.build = [    self.createObjects
						, self.createParameters
						, self.createOperators
						, self.createSlots
						, self.createConnections  ]

	
	def createObjects( self ):
		pass

	def createParameters( self ):
		pass

	def createOperators( self ):
		pass

	def createSlots( self ):
		pass

	def createConnections( self ):
		pass

