# what does this method do ?   
# ---------------------------------------------------------------------------------

import pymel.core as pm

def SearchReplaceNames (  searchString="pasted__", replaceString="",  objs=None ):
    
    if objs==None:
    	objs = pm.ls(sl=True)
    else:
        objs = pm.ls(objs)
    
    returnVal = []
    
    #============================================================================
    # RENAME
    		
    for obj in objs:
    	
    	currentFullName = obj.name()
    	
    	newFullName = currentFullName.replace ( searchString , replaceString )
    	
    	newFullNameSplitted = newFullName.split ("|")
    	
    	newName = newFullNameSplitted [len(newFullNameSplitted)-1]
    	
    	pm.rename (obj , newName )
    
    returnVal = pm.listRelatives(obj,ad=True)
    returnVal.append(obj)
    returnVal.reverse()
    	
    return returnVal