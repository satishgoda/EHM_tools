import pymel.core as pm

# ---------------------------------------------------------------------------------
# Synopsis : removeNameSpaces ()
#
# What does this script do ?
#                                removes ":" from names in the entire scene or selected objects if any
# How to use :
#
# Version: 1.1
#
# Author: Ehsan HM ( hm.ehsan@yahoo.com )
#
# ---------------------------------------------------------------------------------
def ReplaceNameSpaces() :

	pm.namespace( set=':' )

	namespaces = pm.namespaceInfo( listOnlyNamespaces=True )

	namespaces.remove( 'UI' )
	namespaces.remove( 'shared' )

	for ns in namespaces:
		try:
			pm.namespace( moveNamespace=(ns,":"), force=True )
			pm.namespace( rm = ns )
		except:
			pass
	'''
	
	objs = pm.ls( type='transform' )

	for obj in objs:
		try:
			pm.rename( obj, obj.name().replace(':','__')  )
		except:
			continue

	'''