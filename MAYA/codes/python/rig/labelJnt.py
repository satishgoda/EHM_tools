import pymel.core as pm 
 
def LabelJnt( jnts = None ): 
 
    if jnts == None: 
        jnts = pm.ls( sl=True ) 
    else: 
        jnts = pm.ls( jnts ) 
     
    for jnt in jnts: 
        if jnt.type() == 'joint': 
            jntName = jnt.name() 
 
            if ":" in jntName: 
                jntName = jntName.split(":")[-1]
            if "|" in jntName: 
                jntName = jntName.split("|")[-1] 
             
            prefix = jntName[0] 
             
            side = 0 
            if prefix == 'L': 
                side = 1 
            elif prefix == 'R': 
                side = 2 
 
            jnt.side.set( side ) 
            jnt.attr('type').set( 18 ) 
            jnt.otherType.set( jntName.replace( '%s_' %prefix, '' ) )