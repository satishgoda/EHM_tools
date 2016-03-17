from Pythons.character_rigging_suit.guide import ComponentGuide
from Pythons.character_rigging_suit.components import Component
from Pythons import log

class ControlGuide( ComponentGuide ):
	markerNames = [ 'Root' ]
	def __init__( self, property ):
		ComponentGuide.__init__( self, property )
		log( '---------------------------------poses---------------------------------' )
		for poses in self.apos:
			log(  str(self.name) + ' position: ' + str(poses.X) + ', ' + str(poses.Y)  + ', ' + str(poses.Z) )

class Control( Component ):
	
	def createObjects( self ):
		log( ' creating Objects....................' )

	def createParameters( self ):
		log( ' creating Parameters....................' )

	def createOperators( self ):
		log( ' creating Operators....................' )

	def createSlots( self ):
		log( ' creating Slots....................' )

	def createConnections( self ):
		log( ' creating Connections....................' )
