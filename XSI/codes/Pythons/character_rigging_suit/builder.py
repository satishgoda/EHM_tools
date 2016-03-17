from Pythons import xsi, log, c
import datetime

class Builder( object ):

	def __init__( self, guide ):
		log( '' )
		log( '' )
		log( '------------ Builder class was instantiated ----------')
		log( '------------------------------------------------------' )		
		log( '' )		
		self.guide = guide
		self.settings = self.guide.settings
		self.components = {}


	
	def build( self ):

		startTime = datetime.datetime.now()
		
		#xsi.SetValue("preferences.scripting.msglog", False )
		
		self.buildInitialHierarchy()
		self.initComponents()
		self.buildComponents()
		
		#xsi.SetValue("preferences.scripting.msglog", True )

		endTime = datetime.datetime.now()
		log( endTime - startTime )
	

	def buildInitialHierarchy( self ):
		log( 'BUILD - 1 ..................... builing initial hierarchy ')

		# model
		self.model = xsi.ActiveSceneRoot.AddModel( None, self.settings[ 'name' ] )
		self.model.Properties('Visibility').Parameters('viewvis').Value = False

		# groups
		self.hidden_grp = self.model.AddGroup( None, 'hidden_grp' )
		self.unselectable_grp = self.model.AddGroup( None, 'unselectable_grp')
		self.controllers_grp = self.model.AddGroup( None, 'controllers_grp')		
		self.deformers_grp = self.model.AddGroup( None, 'deformers_grp')


		self.hidden_grp.Parameters( 'viewvis' ).Value = 0
		self.unselectable_grp.Parameters( 'selectability' ).Value = 0
		self.deformers_grp.Parameters( 'viewvis' ).Value = 0


		# orgenizers
		self.deformers_org = self.model.AddNull( 'deformers_org')
		self.geometries_org = self.model.AddNull( 'geometries_org')

		self.hidden_grp.AddMember( self.deformers_org )
		self.hidden_grp.AddMember( self.geometries_org )


	def initComponents( self ):
		log( 'BUILD - 2 ..................... initializing Components ')

		for key, controlGuide in self.guide.components.items(): # ie: key = Arm_Left, controlGuide = components.ArmGuide()

			type_ = controlGuide.type_

			log( 'init component builder: %s (%s)'%( key, type_ ) )
			
			moduleName = type_.lower()
			module = __import__( 'Pythons.character_rigging_suit.components.' + moduleName, globals(), locals(), ['*'], -1 )
			componentClass = getattr( module, type_ )
			self.components[ key ] = componentClass( self, controlGuide ) # ie: components.Arm(  )'''

	
	def buildComponents( self ):
		log( 'BUILD - 3 ..................... building Components' )
		for i in xrange( 5 ):
			for key, component in self.components.items():
				component.build[i]()






		