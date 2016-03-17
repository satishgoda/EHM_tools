import pymel.core as pm

def GetShapeOfType( obj, type ):
    if obj.type() == type:
        return obj
    else:
        shape = obj.getShape()
        if not shape:
            pm.warning( "given object doesn't have a shape of type '{}'".format( type ))
            return None
    if shape.type() == type:
        return shape
    else:
        pm.warning( "given object is not or doesn't have a shape of type '{}'".format( type ))
        return None