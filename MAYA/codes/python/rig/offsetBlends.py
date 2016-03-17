# script name : offsetBlends
#
# author : Ehsan H.M
#
# what does this script do ?     applys vertex moves to all blendshapes
#
# How to use:
#          		select blends, source and dest and run this script
#				blends are blendshape targets
#               source is your base geometry
#               dest is the geometry you've tweaked 
#============================================================================


import pymel.core as pm


def UI():
	# find ui files
	ehm_uiPath = pm.internalVar( uad=True ) + 'scripts/ehm_tools/ui/'
	
	# delete window if exists
	if pm.window( 'offsetBlends.ui', q=True,  exists=True ):
		pm.deleteUI( 'offsetBlends.ui' )
	
	# load ui
	uiFile = pm.loadUI( uiFile = ehm_uiPath + 'offsetBlends.ui' )

	# connect base button
	pm.button( "ofb_selectBase_btn", edit=True, command = "offsetBlends.addToTextField('ofb_base_tf')" )

	# connect modified button
	pm.button( "ofb_selectModified_btn", edit=True, command = "offsetBlends.addToTextField('ofb_modified_tf')" )

	# connect  object to change buttons
	pm.button( "ofb_selectGeos_btn", edit=True, command = "offsetBlends.addToTextScroll('ofb_geos_tsl')" )

	# connect  apply change buttons
	pm.button( "ofb_apply_btn", edit=True, command = "offsetBlends.OffsetBlends()" )

	# show ui
	pm.showWindow( uiFile )


#=================================

# def for adding selected object to text field
def addToTextField( textFieldName ):
	geo = pm.ls( sl=True )[0]
	pm.textField( textFieldName, edit=True, text = geo.name() )

# def for adding selected object to text scroll list
def addToTextScroll( textScrollName ):
	geos = pm.ls( sl=True )
	# remove previous items
	pm.textScrollList( textScrollName, edit=True, removeAll=True )
	for geo in geos:
		pm.textScrollList( textScrollName, edit=True, append = geo.name() )


# def that get info from ui and applys changes to final geometries
def OffsetBlends():
	blends = pm.ls( pm.textScrollList( 'ofb_geos_tsl', q=True, allItems=True ) )
	base = pm.ls( pm.textField( 'ofb_base_tf', q=True, text=True ) )[0]
	modified = pm.ls( pm.textField( 'ofb_modified_tf', q=True, text=True ) )[0]

	# calcute offsets
	movedVtxs, vtxOffs = CalcOffsets( base ,  modified )

	# for each geometry, apply offsets	
	currentObj = 1
	for blendObj in blends:
		print ( "Changes are being applied on object No '" , currentObj , "' from '" , len(blends) , "' ----- " , blendObj )
		currentObj+=1
		for movedVtx in range(len(movedVtxs)):
			pm.xform ( blendObj.vtx[movedVtxs[movedVtx]] , relative=True  , objectSpace=True , t =  vtxOffs[movedVtx]  )




def CalcOffsets( source , dest, fTolerance = 0.0001):

	numOfVtxs = pm.polyEvaluate( source , v = True )
	movedVtxs = []
	vtxOffs = []

	for v  in  range( numOfVtxs ) :

		vtxNum = v
		sourceTempPosX , sourceTempPosY , sourceTempPosZ =  pm.xform ( source.vtx[v] , q=True,  objectSpace=True ,t=True )
		destTempPosX , destTempPosY , destTempPosZ =  pm.xform ( dest.vtx[v] , q=True,  objectSpace=True ,t=True )

		if ( abs(sourceTempPosX - destTempPosX) < fTolerance and abs(sourceTempPosY - destTempPosY) < fTolerance and abs(sourceTempPosZ - destTempPosZ) < fTolerance ):
			continue
		else :
			movedVtxs.append ( v )
			pos = ( destTempPosX-sourceTempPosX , destTempPosY-sourceTempPosY , destTempPosZ-sourceTempPosZ )
			vtxOffs.append ( pos )

	return  movedVtxs, vtxOffs