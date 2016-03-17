import pymel.core as pm
from functools import partial

# ---------------------------------------------------------------------------------
# synopsis : renamer ( name , hierarchyMode)
#
# what does this method do? 
#          renames selected series of objects with an auto padding system.
#          it replaces # with number.
#          eg:  ## means 2 digits pad
#          		##### means 5 digits pad
#
# how to use :  
#          select objects
#                        renamer( "f41_####_jnt" , True )
#            ( "True" creates renames the whole hierarchy not just the selected object )
#            result :    foot_0001_jnt , foot_0002_jnt , ...
#
# return :    list of renamed objects 
# ---------------------------------------------------------------------------------

class Renamer():

	def __init__(self, *args, **kwargs):
	
		self.newJnts = []
	
		if args or kwargs:
			self.renamer(*args, **kwargs)
		else:
			self.UI()
	
	def UI(self):
		width = 250
		height = 100
		# create window
		if pm.window( 'ehm_Renamer_UI', exists=True ):
			pm.deleteUI( 'ehm_Renamer_UI' )
		pm.window( 'ehm_Renamer_UI', title='rename multiple objects', w=width, h=height, mxb=False, mnb=False, sizeable=False )
		
		# main layout
		mainLayout = pm.columnLayout(w=width, h=height)
		formLayout = pm.formLayout(w=width-10, h=height-10)
		frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)	
		
		# left column and form
		pm.setParent( formLayout )
		leftLayout = pm.columnLayout(adj=True)
		leftForm = pm.formLayout(w=(width-10)/3, h=height-10)

		# right column and form
		pm.setParent( formLayout )
		rightLayout = pm.columnLayout(adj=True)
		rightForm = pm.formLayout(w=(width-10)/3*2, h=height-10)
		
		# num of joints slider
		text = pm.text( label="New name:", parent=leftForm  )
		self.nameTF = pm.textField(  text= 'newName_###', h=20, parent=rightForm  )												


		# button
		button = pm.button( label='apply', w=100, h=30,  c=partial( self.renamer, None, 'newName_###', False ), parent=formLayout  )
		
		# place controls
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'left', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'right', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'bottom', 38) )
		
		pm.formLayout( formLayout, edit=True, attachForm=(leftLayout,'left', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(leftLayout,'right', width/3*2) )
		pm.formLayout( formLayout, edit=True, attachForm=(leftLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(leftLayout,'bottom', 38) )
		
		pm.formLayout( formLayout, edit=True, attachForm=(rightLayout,'left', width/3) )
		pm.formLayout( formLayout, edit=True, attachForm=(rightLayout,'right', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(rightLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(rightLayout,'bottom', 38) )
		

		pm.formLayout( leftForm, edit=True, attachForm=(text,'right', 5) )
		pm.formLayout( leftForm, edit=True, attachForm=(text,'top', 13) )		
		
		pm.formLayout( rightForm, edit=True, attachForm=(self.nameTF,'left', 0) )
		pm.formLayout( rightForm, edit=True, attachForm=(self.nameTF,'right', 15) )
		pm.formLayout( rightForm, edit=True, attachForm=(self.nameTF,'top', 13) )
		

		pm.formLayout( formLayout, edit=True, attachForm=(button,'left', 5) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'right', 5) )
		pm.formLayout( formLayout, edit=True, attachForm=(button,'bottom', 5) )
		
		
		# show window
		pm.showWindow( 'ehm_Renamer_UI' )

	def renamer ( self, objs=None, name='newName###', hierarchyMode=False, *args ):
		
		try:# if in UI mode, get number of joints from UI
			name = pm.textField( self.nameTF,q=True,text=True)
		except:
			pass		
		
		if not objs :
			objs = pm.ls (sl=True)
		
		if not objs:
			pm.error('ehm_tools...Renamer: No object to rename!')

		
		# LIST OF OBJECTS TO RENAME IF IN "HIERARCHY MODE" =========================    
		if hierarchyMode :
			pm.select (objs[0] , hierarchy = True )
			objs = pm.ls ( sl = True , long = True )  
			
		# FIND THE PREFIX, SUFFIX AND NUMBER OF PADS ===================
		
		# name = "d5d_##_233d_##_tttr_ee"
		
		nameSplitted = name.split ("#")
		
		# find prefix
		prefix = nameSplitted[0]
		
		# find suffix
		suffix = nameSplitted[ len (nameSplitted)-1]
		
		if suffix == prefix :
			suffix = ""
		
		# finding pad
		pad = 0
		
		for i in name:
			if i == "#" :
				pad += 1
		
		# RENAME ===================
		
		zeros = ""
		
		for p in range (1 , len(objs ) + 1 ):
			#objs = pm.ls ( sl = True , long = True) # updates the path to the object in everyloop
			zeros = ""
			
			if len (objs) < 1 :
				error( "No object is selected!" )

			else :
				for n in range(1 , pad):
					if ( p  < pow (10 , n) ):
						zeros += "0"
					
				if ( suffix != "" ):
					self.newJnts.append( pm.rename ( ( objs[p-1] ) , ( prefix +  zeros + str(p) + suffix ) ) )
				
				else:
					self.newJnts.append( pm.rename ( ( objs[p-1] ) , ( prefix +  zeros + str(p)  ) ) )
