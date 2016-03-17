import maya.cmds as cmds
import os
from functools import partial
import maya.mel as mel
import sys

ehsan_script_directory = (__path__[0].partition('\\codes'))[0]

widgets = {}

def UI( *args ):

	# create the window
	if cmds.dockControl( 'ehm_dock', exists=True ):
		cmds.deleteUI( 'ehm_dock' )
	widgets['window'] = cmds.window( mnb=False, mxb=False )
	
	# main layouts
	widgets['scrollLayout'] = cmds.scrollLayout( hst=10 )
	widgets['mainLayout'] = cmds.columnLayout( w=160, adj=True )
	
	# find all icons and create a symbol button for each 
	populateToolbar(  )
	
	# make it dockable
	widgets['dock'] = cmds.dockControl( 'ehm_dock',width=185, content= widgets['window'], area='left', allowedArea='all', label='ehm toolbar')
	
	# show window - it's docked, there is no need to show it!
	#cmds.window( widgets['window'] , edit=True , w=180, h=600, sizeable=True )
	#cmds.showWindow( widgets['window'] )

def populateToolbar( *args ):

	iconPath = os.path.join ( ehsan_script_directory , 'ui', 'icons' )
	icons = os.listdir( iconPath )
	
	# find categories
	rawCategories = []
	for icon in icons:
		if '__' in str(icon): # ignore files other than ones with '__' in their names
			rawCategories.append( icon.partition('__')[0] )
	categories = list( set( rawCategories ) )
	categories.sort()
	
	# create frame layout for each category
	for category in categories:
		widgets[ category+'_frameLayout' ] = cmds.frameLayout( label=category,w=150, collapsable=True, parent=widgets['mainLayout'] )
		widgets[ category+'layout' ] = cmds.rowColumnLayout( nc=3 )
	
	
	# create icons
	for icon in icons:
		iconName = icon.partition('.')[0]
		category = icon.partition('__')[0]
		command = iconName.partition('__')[2]
		if '__' in str(icon): # ignore files other than ones with '__' in their names		
			widgets[ icon + '_button'] = cmds.symbolButton( c=partial(runMethod,category,command) , w=50, h=50, image=(os.path.join (iconPath,icon)), parent=widgets[ category+'layout' ], annotation= command )
		

def runMethod( category, curveName, *args ):

	try:
		CurveName = curveName[0].capitalize() + curveName[1:]
		exec( 'from codes.python.%s import %s'%(category,curveName) ) # ie: from ehm_tools.codes.curves import cubeCrv
		exec( 'reload(%s)'%(curveName) ) # ie: reload( cubeCrv )
		exec( '%s.%s()'%( curveName, CurveName)  ) # ie: cubeCrv.CubeCrv()
	except NameError:
		cmds.warning( '"%s" function does not exist!'%method )
	

	
#####################################################################################
# get rid of auto orient joint in move option box
cmds.manipMoveContext( 'Move', e=True, orientJointEnabled=0 )


#####################################################################################
# set time setting to 25 fps
cmds.currentUnit( t="pal" )


#####################################################################################
# Add M:\MAYA_DEV\plugins; to maya's user plugin path


# fine Maya.env file located in user pref directory
path = cmds.internalVar( upd=True )
path = os.path.join( path[:-6].replace('/','\\'), 'Maya.env' )

# add python script directory
pythonPath = os.path.join ( ehsan_script_directory, 'codes', 'python', 'others_scripts' )
if pythonPath not in sys.path:
    sys.path.append( pythonPath )

# add mel script path to env
scriptPath = ehsan_script_directory + '\codes\MELs;'
scriptPath += mel.eval('getenv "MAYA_SCRIPT_PATH"')
mel.eval( 'putenv \"MAYA_SCRIPT_PATH\" "{}";'.format(scriptPath) )

"""
f = open( path, 'r' )

# add plugin directory
if not pluginPath in f.read():
	f = open( path, 'a' )
	f.write( '\n%s' %pluginPath )


# add mel script directory
f = open( path, 'r' )
if not scriptPath in f.read():
	f = open( path, 'a' )
	f.write( '\n%s' %scriptPath )
	sys.stdout.write( "It seems this is the first time you're running EHM tools, please restart maya!" )


# add module  directory
f = open( path, 'r' )
if not modulePath in f.read():
	f = open( path, 'a' )
	f.write( '\n%s' %modulePath )
	sys.stdout.write( "It seems this is the first time you're running EHM tools, please restart maya!" )





f.close()
"""