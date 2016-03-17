#nm_python_bendy_UI
import maya.cmds as cmds
import maya.mel as mel

def bendy_UI():
	#check to see if our window exists
	if cmds.window("bendy_UI", exists = True):
		cmds.deleteUI("bendy_UI")
		
#=============================================================================================================================#     

	#create our window
	window = cmds.window("bendy_UI", title = 'Bendy Joint Creator', w = 426, h = 280, mnb = True, mxb = False, sizeable = False)
	
	#create a main layout
	mainLayout = cmds.columnLayout( w = 425, h = 280 )
	
#-----------------------------------------------------------------------------------------------------------------------------#    
	#add columns
	global tsList
	tsList = cmds.textScrollList( "tsList", ams = 1, a = ('(only works on joints)'), w = 426, h = 200, dcc = dClick )
	
	rowColumnLayout1 = cmds.rowColumnLayout(nc = 4, cw = [(1, 22) , (2, 22) , (3, 60), (4, 320)], columnOffset = [(1, "left", 0), (2, "left", 0), (3, "left", 0), (4, "left", 20)])
	add = cmds.button( l = '+', bgc = (0.1, 0.4, 0.1), w = 20, c = addToList )
	remove = cmds.button( l = '-', bgc = (0.5, 0.1, 0.1), w = 20, c = remFromList )
	removeAll = cmds.button( l = 'remove all', bgc = (0.3, 0.1, 0.1), c = remAllFromList )
	seg = cmds.intSliderGrp( "seg", f = True, l = 'Segment Joints:', minValue = 2, maxValue = 20, fmn = 2, fmx = 20, v = 2 )
	#rowColumnLayout = cmds.rowColumnLayout(nc = 3, cw = [(1, 300) , (2, 30) , (3, 95)], columnOffset = [(1, "both", 5), (2, "left", 5), (3, "both", 5)])
	
#-----------------------------------------------------------------------------------------------------------------------------#	
	rowColumnLayout2 = cmds.rowColumnLayout(nc = 3, cw = [(1, 63), (2, 61)], columnAttach = (1, "right", 0), columnOffset = [(1, "left", 0), (2, "left", 0)], parent = mainLayout)
	text = cmds.text( 'text',  l = 'Global Scale:' )
	textField = cmds.textField( 'textField', w = 111 )
	fsg = cmds.floatSliderGrp( "fsg", f = True, l = 'Control Size:', minValue = .1, maxValue = 20, fmn = .1, fmx = 20, v = 1, w = 300 )

#-----------------------------------------------------------------------------------------------------------------------------#	
	cmds.separator (h = 5)
	#create the build and close button
	grid = cmds.gridLayout( nc = 2, cwh = (213,30), parent = mainLayout )
	b1 = cmds.button(label = "Get bendy!", w = 213, h = 30, c = 'nm_python_bendy_proc.bendy_proc()', parent = grid )
	b2 = cmds.button(label = "Go home.", w = 213, h = 30, c = 'cmds.deleteUI("bendy_UI")', parent = grid )
	
#=============================================================================================================================#       
	#show window
	cmds.showWindow(window)
	
#=============================================================================================================================#   

def dClick():
	tslDC = []
	tslDC = cmds.textScrollList( tsList, q = True, si = True )
	cmds.select( tslDC[0], r = True )
	
def addToList(tsList):
	#get the selected objects and add them
	global objs
	objs = []
	objs =  cmds.ls( sl = True ) 
	
	for ob in objs:
		#check to see if it's already in the tsList
		global currentObjs
		currentObjs = []
		currentObjs = cmds.textScrollList( 'tsList', q = True, ai = True )
		match = 0
		global cur

		for cur in currentObjs:
			if ( cur == ob ):
				match = 1
		if ( match == 0):
			cmds.textScrollList( 'tsList', e = True, a = ob )
		
def remFromList(tsList):
	#get the selected objects and add them
	global selObj

	selObj = []
	cmds.textScrollList( "tsList", e = True, di = ("(only works on joints)")  )
	selObj = cmds.textScrollList( "tsList", q = True, si = True )

	if ( len(selObj) > 0 ):
		cmd = ('cmds.textScrollList( "%s", e = True, ri = (' ) % ('tsList')
		for item in selObj:
			cmd += ("'" + item )
			if( len(selObj) == 1 ):
				cmd += "'"
			else:
				cmd += "', "
		
		cmd += ('))')
		print cmd
		eval( cmd )
	
def remAllFromList(tsList):
	#get the selected objects and add them
	selObj = []
	selObj = cmds.textScrollList( "tsList", q = True, ai = True )
	
	if ( len(selObj) > 0 ):
		cmd = ('cmds.textScrollList( "%s", e = True, ri = (' ) % ('tsList')
		
		for item in selObj:
			cmd += ('"' + item )
			cmd += '", '
			
		cmd = cmd[:-2]
		cmd += ('))')
		eval( cmd )
		cmds.textScrollList( 'tsList', e = True, a = ('(only works on joints)') )
	
	
	
	
	
	
	
	
	
# i = 0
# sel = cmds.ls(sl = True)
# sel = str(sel)[3:][:-2] + '.'
# items = []
# items = cmds.listAttr( cmds.ls( sl = True ), k = True )
# n = len(items)
# pop = cmds.popupMenu('pop',parent=btn, ctl=False, button=3) 
# com = 'print cmds.menuitem( itemNum, q = True, l = True )'
# list = []
# while ( i < n ):
	# name = 'hello%d' % (i)
	# list = 'cmds.menuItem( name, l=items[' + str(i) + '], c=' + '"print sel + items[' + str(i) + ']")'
	# eval(list)
	# i += 1

# cmds.showWindow(win) 

	
	
	
	
	
	
	
	