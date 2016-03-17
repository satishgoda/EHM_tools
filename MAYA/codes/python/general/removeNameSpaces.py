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

def RemoveNameSpaces ( add_version=False ) :
	
	'''
	allObjs = pm.ls( type="mesh" )
	pm.lockNode( allObjs, lock=0 )

	
	pm.namespace( set=':' )
	nameSpaces = pm.namespaceInfo( listOnlyNamespaces=True )
	nameSpaces.remove( 'UI' )
	nameSpaces.remove( 'shared' )


	for i in range( len(nameSpaces) ):
		pm.namespace( set=':' )
		pm.namespace( set=nameSpaces[i] )
		objs = pm.namespaceInfo( listOnlyDependencyNodes=True )
		
		# loop through all nodes
		for obj in  objs:
			# if there is ":" in their name then remove the parts before ":"
			buffer  =  obj.name().split ( ":" ) 
			if len(buffer) > 1 :
				if add_version:
					ver = '_v%s' % i
					if ver not in obj.name():
						newName =  '%s%s' % ( buffer[-1] ,ver )
						pm.rename (  obj , newName )
				else:
					newName =  '%s' %  buffer[-1] 
					pm.rename (  obj , newName )					
		pm.namespace( set=':' )
		pm.namespace( mv=(nameSpaces[i], ':') , force=True  )
		pm.namespace( rm=nameSpaces[i] )
	'''
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