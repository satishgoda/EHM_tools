'''
Author: Ehsan HM ( hm.ehsan@yahoo.com )

Script Name: ExportImportAnim()

Version: 1.0

What does this do: exports and imports animation of selected objects.


'''

import pymel.core as pm
import sys
import os

uad = pm.internalVar( uad=True )
import pymel.core as pm
from functools import partial

class ExportImportAnim():
	
	def __init__(self, *args, **kwargs):
	
		if args or kwargs:
			self.importAnim(*args, **kwargs)
		else:
			self.UI()

			
	def UI(self):
		
		# create window
		if pm.window( 'ehm_ImportAnim_UI', exists=True ):
			pm.deleteUI( 'ehm_ImportAnim_UI' )
		pm.window( 'ehm_ImportAnim_UI', title='Export Import Animatom', w=350, h=40, mxb=False, mnb=True, sizeable=False )
		
		# main layout
		#mainLayout = pm.rowColumnLayout()
		formLayout = pm.formLayout(w=350, h=40)
		#frameLayout = pm.frameLayout(borderStyle='etchedIn', labelVisible=False)
		pm.setParent( formLayout )
		

		# buttons
		self.exportButton = pm.button( label='Export',  h=30,  c=self.exportAnim )
		self.importButton = pm.button( label='Import',  h=30,  c=partial( self.importAnim, None ) )

		'''
		# place frame layout
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'left', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'right', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'top', 3) )
		pm.formLayout( formLayout, edit=True, attachForm=(frameLayout,'bottom', 38) )
		'''

		# place buttons
		pm.formLayout( formLayout, edit=True, attachPosition=(self.exportButton,'left', 4, 0) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.exportButton,'right', 2 , 50) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.exportButton,'bottom', 5) )

		pm.formLayout( formLayout, edit=True, attachPosition=(self.importButton,'left', 2, 50) )
		pm.formLayout( formLayout, edit=True, attachPosition=(self.importButton,'right', 4 , 100) )
		pm.formLayout( formLayout, edit=True, attachForm=(self.importButton,'bottom', 5) )

		
		# show window
		pm.showWindow( 'ehm_ImportAnim_UI' )

		
	# get character name from selection and write it in character name text field
	def getCharacterName( self, obj, *args ):
		if not obj:
			objs = pm.ls( sl=True )
			if objs:
				obj = objs[-1]
		else:
			obj = pm.ls( obj )[-1]
		pm.textField( self.exportModeRBG, e=True, text = self.getNameSpace( obj ) )    

		
	# get name spaces
	def getNameSpace( self, obj, *args ):
		if not obj:
			return None
		try:
			objName = obj.name()
		except:
			objName = obj
		if len( objName.split(':') ) > 1 :
			return objName.split(':')[0]
		else:
			None

			
	# check if object's name is unique
	def hasUniqueName( self, obj , *args ):
		try:
			objName = obj.name()
		except:
			objName = obj
		if len( objName.split('|') ) > 1 :
			return False
		else:
			return True

			
	def importAnim( self, nameSpace=None, replaceString=None,   *args ):
		
		successState = True		
	
		#  *.anim file
		filePath = pm.fileDialog2( caption='Read Animation', fileMode=1, startingDirectory=uad , fileFilter="Anim Files (*.anim)" )
		
		if not filePath:
			pm.warning( 'Read animation cancelled.' )
			return None
		
		# read anim info from file
		filePath = filePath[0]
		logfile = open( filePath , 'r' )
		fileContent =  logfile.read() # dictionary containing dictionaries of every object's animations
		logfile.close()
		
		
		# we can replace some parts of file to use animations on other objects. 
		# for example, replace 'L' with 'R' copy animation from left side to right side. 

		#replaceString = ('L','R')
		if replaceString:
			fileContent = fileContent.replace( replaceString[0], replaceString[1] )

		
		
		# convert file content to a animInfos dictionary
		animInfos = eval( fileContent )
		
		objs = animInfos.keys()
		
		try:
			nameSpaceRaw =  pm.ls( sl=True )[0].name().split(':')
			if len(nameSpaceRaw) > 1:
				nameSpace = nameSpaceRaw[0]
		except:
			nameSpace = None		

		
		for obj in objs:
		
			if nameSpace:
				try:
					objNode = pm.PyNode( nameSpace + ':' + obj )
				except:
					successState = False
					pm.warning( 'Could not find object to import anim to, skipped.')
					continue
			
			else:
				try:
					objNode = pm.PyNode( obj )
				except:
					successState = False
					pm.warning( 'Could not find object to import anim to, skipped.' )
					continue
		   
			# print objNode  
			# print '__________________________________________________________'
				
			
			attrs = animInfos[ obj ].keys()
			# print attrs
			
			for attr in attrs:
				#print attr
				#print '=============================' 
				animCurveInfos = animInfos[ obj ][ attr ]
				#print animCurveInfos
				for animCurveAttribute in animCurveInfos:

					animCurveValues =  animInfos[ obj ][ attr ][ animCurveAttribute ] 
					#print animCurveAttribute  # anim curve attrs such as times, values, outWeights, inWeights, inAngles, outAngles               
					#print animCurveValues # anim curve values for times, values, outWeights, inWeights, inAngles, outAngles   
					#print '--------------'
					times = animCurveInfos[ 'times' ]
					values = animCurveInfos[ 'values' ]
					outWeights = animCurveInfos[ 'outWeights' ]
					outAngles = animCurveInfos[ 'outAngles' ]
					inWeights = animCurveInfos[ 'inWeights' ]
					inAngles = animCurveInfos[ 'inAngles' ]
					
					for i in range( len( animCurveInfos[ 'times' ] ) ):
						if nameSpace:
							if pm.objExists(  nameSpace + ':' + attr  ):
								attrNode = pm.PyNode( nameSpace + ':' + attr )
							elif pm.objExists(  attr  ):
									attrNode = pm.PyNode( attr )
							else:
								successState = False
								pm.warning( 'attrtibute was not found on target to apply animation, skipped.' )
								continue
						else:
							if pm.objExists(  attr  ):
								attrNode = pm.PyNode( attr )
							else:
								successState = False
								pm.warning( 'attrtibute was not found on target to apply animation, skipped.' )
								continue

						pm.setKeyframe( attrNode, time= times[i] , value= values[i]  )
						pm.keyTangent( attrNode, e=True, index=(i,i), outWeight=outWeights[i], outAngle=outAngles[i], inWeight=inWeights[i], inAngle=inAngles[i] )
	
		if successState:
			sys.stdout.write( 'Animation was successfully imported.' )
		else:
			pm.warning( 'Animation was imported. Not all objects or their attributes were the same. So, animation was not applied to them.' )	
				
	def exportAnim(self, *args):
		objs = pm.ls( sl=True )
		successState = True
		
		filePath = pm.fileDialog2( caption='Save Animation', startingDirectory=uad , fileFilter="Anim Files (*.anim)" )
		
		if not filePath:
			sys.stdout.write('Save animation cancelled.')
			return None
		
		
		animInfos = {} # dictionary containing dictionaries of every object's animations
		for obj in objs:
			
			if not ( self.hasUniqueName( obj ) ): # if object'n name is not unique, doesn't save animation for it
				successState = False
				pm.warning( "Object %s's name is not unique. skipped"%obj.name() )  
				continue
			
			nameSpace = self.getNameSpace( obj )
			if nameSpace:
				objName = obj.name().split(':')[1]
			else:
				objName = obj.name()
			
			# find all anim curves on the object
			curves = pm.findKeyframe( obj , curve=True )
			
			
			if not curves: # jump to next object if no anim curve found
				continue
				
			animInfo = {} # dictionary containing one object's animations
			
			for curve in curves: # for each curve, find where it's connected to, keys' times, values and tangents
				attr = pm.listConnections( '%s.output'%curve, plugs=True )[0]
				if nameSpace:
					attrName = attr.name().split(':')[1]
				else:
					attrName = attr.name()
				times = pm.keyframe( attr, q=True, timeChange=True )
				values = pm.keyframe( attr, q=True, valueChange=True )
				outWeights = pm.keyTangent( attr, q=True, outWeight=True )
				outAngles = pm.keyTangent( attr, q=True, outAngle=True )
				inWeights = pm.keyTangent( attr, q=True, inWeight=True )
				inAngles = pm.keyTangent( attr, q=True, inAngle=True )
				animInfo[ attrName ] = { 'times':times, 'values':values, 'outWeights':outWeights, 'outAngles':outAngles, 'inWeights':inWeights, 'inAngles':inAngles }
			
			animInfos[ objName ] = animInfo
		
		# write anim info to file
		filePath = filePath[0]
		logfile = open( filePath , 'w')
		logfile.write( str(animInfos) )
		logfile.close()
		
		if successState:
			sys.stdout.write( 'Animation was successfully exported.' )
		else:
			pm.warning( 'Some objects animtions were not saved due to multiple object with the same name, check script editor for more info.' )