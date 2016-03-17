from Pythons import log 


class Guide( object ):

	def __init__( self, model ):
		log( '' )
		log( '' )
		log( '------------ Guide class was instantiated ------------' )
		log( '------------------------------------------------------' )		
		log( '' )		
		assert self.isValid( model ), 'Guide is not Valid.'
		
		self.settings = { 'name':'unknown'
							,'color_R':'0,0,1'
							,'color_M':'.75,.25,.75'
							,'color_L':'1,0,0'  }
		
		self.components = {}
		self.initFromModel()
	
	
	
	def isValid( self, model ):
		log( 'GUIDE - 1 .................................. cheking model')
		self.model = model
		if not self.model.Type == "#model":
			return False
		
		self.settings_prop = model.Properties('Settings')
		if not self.settings_prop:
			return False

		self.components_org = model.FindChild( 'components_org')
		if not self.components_org:
			return False

		return True

	
	def initFromModel( self ):
		log( 'GUIDE - 2 .................................. get info From Model')
		for parameter in self.settings_prop.Parameters:
			self.settings[ parameter.ScriptName ] = parameter.Value

		self.settings[ 'color_R' ] = [ float(s) for s in self.settings[ 'color_R' ].split(',') ]
		self.settings[ 'color_M' ] = [ float(s) for s in self.settings[ 'color_M' ].split(',') ]
		self.settings[ 'color_L' ] = [ float(s) for s in self.settings[ 'color_L' ].split(',') ]

		
		for property in self.components_org.Properties:
			
			if not property.Name.startswith('settings_'):
				continue
			
			type_ = property.Type_.Value
			name =  property.Name_.Value
			location =  property.Location.Value			
			log( 'Initializing........%s_%s (%s)'%(type_,name,location) )

			moduleName = type_.lower()
			module = __import__( 'Pythons.character_rigging_suit.components.' + moduleName, globals(), locals(), ['*'], -1 )
			guideClass = getattr( module, type_+'Guide' ) 
			self.components[ name+'_'+location ] = guideClass( property ) # ie: components.ArmGuide(  )




class ComponentGuide( object ):

	markerNames = ()

	def __init__( self, property ):

		self.prop = property
		self.model = self.prop.Model

		self.type_ = self.prop.Type_.Value
		self.name = self.prop.Name_.Value
		self.location = self.prop.Location.Value

		self.settings = {}
		for parameter in self.prop.Parameters:
			self.settings[ parameter.Name ] = parameter.Value

		self.pos={}
		self.tfm={}
		self.apos=[]
		self.atfm=[]

		for markerName in self.markerNames:
			marker = self.model.FindChild( self.getMarkerName( markerName ) )
			assert marker, 'missing marker: ' + self.getMarkerName( markerName )
			self.saveMarkerTransform( marker, markerName )


	def saveMarkerTransform( self, marker, markerName ):
			log( 'COMPONENT GUIDE - 1 .................................. saveMarkerTransform')
			tfm = marker.Kinematics.Global.Transform
			tfm.SetScalingFromValues(1,1,1)
			self.pos[ markerName ] = tfm.Translation
			self.tfm[ markerName ] = tfm
			self.apos.append( tfm.Translation )
			self.atfm.append( tfm )

	

	def getMarkerName( self, name ):
		return 'Gde_' + self.name + '_' + self.location + '_' + name