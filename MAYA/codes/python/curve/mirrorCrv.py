import pymel.core as pm 
 
# after rigging you might want to change the cvs of your control curve 
# this script help to apply your tweaks to curve in the other side as well. 
 
 
 
class MirrorCrv(): 
 
    def __init__(self, *args, **kwargs): 
        self.mirrorCrv(*args, **kwargs) 
 
 
    def mirrorCrv( self, crvs=None, *args ): 
        if not crvs: 
            crvs = pm.ls( sl=True ) 
        else: 
            crvs = pm.ls( crvs ) 
         
         
        for crv in crvs: 
            objs = pm.ls( sl=True ) 
             
        for obj in objs: 
            otherObj = self.findMirror( obj = obj ) 
            if otherObj: 
                # find number of cvs 
                shape = obj.getShape(type="nurbsCurve") 
                if not shape: 
                    return 
                numSpans = shape.spans.get() 
                degree = pm.getAttr( shape.attr('degree') ) 
                form = pm.getAttr( shape.attr('form') ) 
                numCVs   = numSpans + degree 
                # Adjust for periodic curve 
                if ( form == 2 ): 
                    numCVs -= degree 
                 
                otherShape = otherObj.getShape(type="nurbsCurve") 
                for cv in range(0,numCVs): 
                    pos = pm.xform( shape.cv[cv], q=True, t=True, ws=True) 
                    pm.xform( otherShape.cv[cv], t=(-pos[0],pos[1],pos[2]), ws=True) 
 
     
    # find object's mirrored object, if None found, return object itself 
    def findMirror( self, obj=None, *args ): 
        if not obj: 
            return None 
             
        prefixes = { 'L_':'R_', 'Lf':'Rt', 'L':'R' } 
         
        nameSpaceAndName = obj.name().split(":") 
        if len( nameSpaceAndName ) > 1: 
            objNameSpace = nameSpaceAndName[0] 
            objName = nameSpaceAndName[1] 
        else: 
            objName = obj.name() 
         
        name = None 
        for i in prefixes: # If prefix 'L_', finds 'R_'. If prefix 'Lf', finds 'Rt' and so on 
            if i in objName and pm.objExists( obj.name().replace(i,prefixes[ i ]) ) :  
                name = obj.name().replace(i,prefixes[ i ]) 
            elif prefixes[ i ] in objName[:2] and pm.objExists( obj.name().replace(prefixes[ i ],i) ) : 
                name = obj.name().replace(prefixes[ i ],i) 
            if name: 
                break 
        if not name: 
            #name = obj.name() 
            return None 
         
        return pm.PyNode(name)