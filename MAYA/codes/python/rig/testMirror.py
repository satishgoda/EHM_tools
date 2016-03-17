import pymel.core as pm

'''
prepareObjectForMirror()
isMirror()

'''


def isMirror( objs=None ):
    if objs:
        objs = pm.ls( objs )
    else:
        objs = pm.ls( sl=True )
    for obj in objs:
		nameSpaceAndName = obj.name().split(":")
		if len( nameSpaceAndName ) > 1:
			objNameSpace = nameSpaceAndName[0]
			objName = nameSpaceAndName[1]
		else:
			objName = obj.name()			
		if objName[:2]==('L_'):
			otherObj = pm.PyNode( obj.name().replace('L_','R_') )
		elif objName[:2]==('R_'):
			otherObj = pm.PyNode( obj.name().replace('R_','L_') )
		else:
			otherObj = obj	
    
    if pm.objExists( obj.name()+'_UP' ):
        up = obj.name()+'_UP'
    else:
        pm.error("isMirror failed! Use prepareObjectForMirror on your objects before running isMirror!"  )

    if pm.objExists( obj.name()+'_AIM' ):
        aim = obj.name()+'_AIM'    
    else:
        pm.error("isMirror failed! Use prepareObjectForMirror on your objects before running isMirror!"  )
    
    if pm.objExists( otherObj.name()+'_UP' ):
        otherUp = otherObj.name()+'_UP'    
    else:
        pm.error("isMirror failed! Use prepareObjectForMirror on your objects before running isMirror!"  )
      
    if pm.objExists( otherObj.name()+'_AIM' ):
        otherAim = otherObj.name()+'_AIM'    
    else:
        pm.error("isMirror failed! Use prepareObjectForMirror on your objects before running isMirror!"  )
    

    # get aim and up info
    aimPos = pm.xform( aim, q=True, t=True, ws=True )
    aim1Pos = pm.xform( otherAim, q=True, t=True, ws=True )
    upPos = pm.xform( up, q=True, t=True, ws=True )
    up1Pos = pm.xform( otherUp, q=True, t=True, ws=True )
    
    
    
    if  (    ( aimPos[0]-(-aim1Pos[0]) < 0.001 ) and ( aimPos[0]-(-aim1Pos[0]) > -0.001 ) 
        and ( aimPos[1]- (aim1Pos[1]) < 0.001 ) and ( aimPos[1]- (aim1Pos[1]) > -0.001 )
        and ( aimPos[2]- (aim1Pos[2]) < 0.001 ) and ( aimPos[2]- (aim1Pos[2]) > -0.001 )
        
        and ( upPos[0]-(-up1Pos[0]) < 0.001 ) and ( upPos[0]-(-up1Pos[0]) > -0.001 ) 
        and ( upPos[1]- (up1Pos[1]) < 0.001 ) and ( upPos[1]- (up1Pos[1]) > -0.001 )
        and ( upPos[2]- (up1Pos[2]) < 0.001 ) and ( upPos[2]- (up1Pos[2]) > -0.001 ) ):    
        
        return True
    else:
        return False




def prepareObjectForMirror( objs=None ):
    if objs:
        objs = pm.ls( objs )
    else:
        objs = pm.ls( sl=True )
    for obj in objs:
		nameSpaceAndName = obj.name().split(":")
		if len( nameSpaceAndName ) > 1:
			objNameSpace = nameSpaceAndName[0]
			objName = nameSpaceAndName[1]
		else:
			objName = obj.name()			
		if objName[:2]==('L_'):
			otherObj = pm.PyNode( obj.name().replace('L_','R_') )
		elif objName[:2]==('R_'):
			otherObj = pm.PyNode( obj.name().replace('R_','L_') )
		else:
			otherObj = obj.name()	

    if not ( pm.objExists( obj.name()+'_AIM' ) ):
        aim = pm.spaceLocator( name= '%s_AIM'%obj.name() )
        pm.parent( aim, obj )
        aim.translate.set(1,0,0)
        aim.rotate.set(0,0,0)
    
    up = pm.spaceLocator( name= '%s_UP'%obj.name() )
    pm.parent( up, obj )
    up.translate.set(0,1,0)
    up.rotate.set(0,0,0)
    
    aim2 = pm.duplicate( aim )[0]
    pm.parent( aim2, world=True )
    aim2.translateX.set( - aim2.translateX.get() ) 
    pm.parent( aim2, otherObj )
    pm.rename( aim2, '%s_AIM'%otherObj.name() )
    
    up2 = pm.duplicate( up )[0]
    pm.parent( up2, world=True )
    up2.translateX.set( - up2.translateX.get() ) 
    pm.parent( up2, otherObj )
    pm.rename( up2, '%s_UP'%otherObj.name() )    
