# script name: orientMirroredJnt
#
# Author: Ehsan HM

'''
what does this script do?

    When mirror joints in --behavior-- mode, their orientation gets wierd in some situations,
    Specially if you want to use --twist-- parameter on --splineIK-- handle.
    This scripts make their orientation normal by reversing X and Y axis
'''


import pymel.core as pm

def OrientMirroredJnt( jnts=None ):
    
    if jnts==None:
        jnts = pm.ls( sl=True )
    else:
        jnts = pm.ls( jnts )
    

    # FOR EVERY JOINT
    for jnt in jnts: 
        
        # create temp objects for X and Y axis. 
        # we can use these for aim constraint to find the right orientation
        xTemp = pm.group( em=True )
        xTemp.setParent( jnt )
        xTemp.translate.set( (-1,0,0) )
        xTemp.setParent( world=True )
        
        yTemp = pm.group( em=True )
        yTemp.setParent( jnt )
        yTemp.translate.set( (0,-1,0) )
        yTemp.setParent( world=True )
        
        # if any children, unparent current joint's children
        parentLater = False
        if jnt.getChildren() != [] :
            children = jnt.getChildren()
            pm.parent( children, world=True )
            parentLater = True
        
        # set joint orientation to 0,0,0
        jnt.jointOrient.set( (0,0,0) )
        
        # aim constraint to temp X and Y objects and delete the constraint and X, Y temp objects
        aimCons = pm.aimConstraint( xTemp, jnt, aimVector=(1,0,0), upVector=(0,1,0), worldUpType="object", worldUpObject= yTemp )
        pm.delete( aimCons, xTemp, yTemp )
        
        # freeze transformation on the current joint
        pm.makeIdentity( jnt, apply=True )
        pm.makeIdentity( jnt )
        
        # if any children, reparent it's children
        if parentLater : 
            pm.parent( children, jnt )
