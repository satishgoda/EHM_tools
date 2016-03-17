import maya.mel as mel

def RemovePastedFromNames():
	mel.eval( 'searchReplaceNames "pasted__" " " "all";' )

