import pymel.core as pm
import os, inspect
from functools import partial


ehsan_script_directory = (inspect.getfile(inspect.currentframe()).partition('\\codes'))[0]


class Colorize():
	
	def __init__(self, *args, **kwargs ):
		
		if args or kwargs :
			self.colorize( *args, **kwargs )
		else:
			self.UI()
	
	def UI(self):
		width = 410
		height = 210
		# create window
		if pm.window( 'ehm_Colorize_UI', exists=True ):
			pm.deleteUI( 'ehm_Colorize_UI' )
		pm.window( 'ehm_Colorize_UI', title='change color', w=width, h=height, mxb=False, mnb=False, sizeable=False )
		
		# main layout
		mainLayout = pm.columnLayout(w=width, h=height)
		formLayout = pm.formLayout(w=width-10, h=height-10)
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)	
		
		# left column and form
		pm.setParent( formLayout )
		buttonsLayout = pm.rowColumnLayout( nc=8 )
		
		# find color icons
		iconPath = os.path.join ( ehsan_script_directory, 'ui', 'icons' )
		icons = os.listdir( iconPath )

		colorIcons=[]
		for icon in icons:
			if 'color_' in icon:
				colorIcons.append( icon )
		

		# button
		for icon in colorIcons:
			colorCode =  int( icon.partition('.')[0].partition('_')[2] )
			pm.symbolButton( image=os.path.join(iconPath,icon), w=50, h=50,  c=partial( self.colorize, None, colorCode ) )
	

		
		
		# show window
		pm.showWindow( 'ehm_Colorize_UI' )



	def colorize( self, shapes=None, color= 'r', *args, **kwargs ):

		if shapes==None:
			try:
				shapes = pm.ls(sl=True)
			except:
				pm.warning( 'ehm_tools...colorize: Select objects to change their colors.' )
				return None
		else:
			shapes = pm.ls(shapes)
		
		for shape in shapes:
			try:
				shape.overrideEnabled.set( 1 )
				if color == 'r' or color =='red' or color =='L' or color == 13:
					shape.overrideColor.set( 13 )
				elif color == 'g' or color =='green' or color == 14:
					shape.overrideColor.set( 14 )
				elif color == 'b' or color =='blue' or color =='R' or color == 6:
					shape.overrideColor.set( 6 )	
				elif color == 'c' or color =='cyan' or color == 18:
					shape.overrideColor.set( 18 )
				elif color == 'm' or color =='magenta' or color == 31:
					shape.overrideColor.set( 31 )
				elif color ==  'y' or color =='yellow' or color == 22:
					shape.overrideColor.set( 22 )
				else:
					shape.overrideColor.set( color )
				pm.select(cl=True)
			except:
				pm.warning( "color override failed. skipped." )
				pass