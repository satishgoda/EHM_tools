import pymel.core as pm

cacheFolder = "05_ANIMATIONS\shot_260\Selpak_Anim_SH260_v001_s005_cache"


objs = pm.ls( sl=True )


for obj in objs:
	if findCache( obj ):
		replaceCache( cacheNode=findCache( obj ), newCacheFolder=cacheFolder)



def	replaceCache(cacheNode, newCacheFolder):
	pm.setAttr(cacheNode.cachePath, newCacheFolder)



# if object has a cache attached to it return the cache node, returns None if there is no cache
def findCache( obj ):
	historyNodes = pm.PyNode.history( obj )
	for historyNode in historyNodes:
		if historyNode.type() == 'cacheFile':
			return historyNode
	return None




#-----------------------------------


def applyCache( obj, cacheFileAddress )


cacheName

cachePath

sourceStart

sourceEnd

originalStart

originalEnd



for obj in objs:
	if hasCache( obj ):
		replaceCache(obj, cacheFolder)
	else:
		applyCache(obj, cacheFileAddress)










pm.PyNode.history( obj, breadthFirst =True )



mesh = "foo_mesh"
xml = "foo_mesh_cache.xml"
data = "foo_mesh_data.mc"

pm.mel.doImportCacheFile(xml, "", [mesh], list())