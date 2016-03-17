import maya.mel as mel

def PointCache():
	mel.eval( 'loadPlugin "KP_PointCache";' )
	mel.eval( 'source KP_PointCacheManager.mel;' )	
	mel.eval( 'KP_PointCacheManager;' )