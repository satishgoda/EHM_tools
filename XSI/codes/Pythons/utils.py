
from Pythons import xsi, c


def searchAndReplace():
	prop = xsi.ActiveSceneRoot.AddProperty( 'customProperty', False, 'search and replace' )

	pSearch = prop.AddParameter3( 'Search', c.siString )
	pReplace = prop.AddParameter3( 'Replace', c.siString )
	

	cancelled = xsi.InspectObj ( prop, '', 'Search And Repalce', c.siModal , False )

	sSearch = pSearch.Value
	sReplace = pReplace.Value
	
	xsi.deleteObj( prop )
	
	if cancelled:
		return

	for obj in xsi.Selection:
		obj.Name = obj.Name.replace( sSearch, sReplace )