import pymel.core as pm
import maya.mel as mel

def IsolateSelected( state=True, showSelected=False ):

	if state: # turn ON isolation
		if not showSelected: # hide everything ( useful during point cache )
			pm.select( clear=True )
			
		allModelPanels = pm.getPanel( type='modelPanel' )

		for onePanel in allModelPanels:
				
			if pm.isolateSelect( onePanel, q=True, state=True ):
				pm.isolateSelect( onePanel, loadSelected=True )
				#pm.isolateSelect( onePanel, update=True )
				mel.eval( 'doReload %s;'%onePanel )
			else:
				pm.isolateSelect( onePanel, state=True )
				#pm.isolateSelect( onePanel, update=True )
				mel.eval( 'doReload %s;'%onePanel )
	
	else: # turn OFF isolation
		allModelPanels = pm.getPanel( type='modelPanel' )
		for onePanel in allModelPanels:
			pm.isolateSelect( onePanel, state=False )




