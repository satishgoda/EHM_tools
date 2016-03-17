# interpolate2Jnts

import pymel.core as pm
import pymel.core.datatypes as dt

def Interpolate2Jnts( firstJnt=None, secondJnt=None, numOfNewJnts=4 ):

	if firstJnt==None or secondJnt==None:
		firstJnt,secondJnt = pm.ls(sl=True)

	newJnts = []
	
	if numOfNewJnts <= 0:
		pm.warning("number of new joints must be bigger than zero.")
		return newJnts
	
	else:
		if (pm.objectType(firstJnt) == 'joint' and pm.objectType(secondJnt) == 'joint' ):
			firstChildJnt = firstJnt.getChildren()[0]
			secondChildJnt = secondJnt.getChildren()[0]             
			# find start and end pose of 2 curves
			crv1CV1Pos = dt.Vector( pm.xform(firstJnt,q=True, ws=True, t=True) )
			crv1CV2Pos = dt.Vector( pm.xform(firstChildJnt,q=True, ws=True, t=True) )
			crv2CV1Pos = dt.Vector( pm.xform(secondJnt,q=True, ws=True, t=True) )
			crv2CV2Pos = dt.Vector( pm.xform(secondChildJnt,q=True, ws=True, t=True) )

			# create a vector representing each curve
			crv1Vec = crv1CV2Pos - crv1CV1Pos
			crv2Vec = crv2CV2Pos - crv2CV1Pos
			start1ToStart2 = crv2CV1Pos - crv1CV1Pos
			end1ToEnd1 = crv2CV2Pos - crv1CV2Pos
			# find segment's length
			startSegLen = start1ToStart2.length() / (numOfNewJnts+1)
			endSegLen = end1ToEnd1.length() / (numOfNewJnts+1)

			# find start and end points for new curves and creating them
			for i in range(1 ,numOfNewJnts+1):
				tmpStart = crv1CV1Pos + ( start1ToStart2.normal() * startSegLen * i )
				tmpEnd = crv1CV2Pos + ( end1ToEnd1.normal() * endSegLen * i)
				pm.select(clear=True)
				newJnts.append( pm.joint( p = tmpStart ) )
				newJnts.append( pm.joint( p = tmpEnd ) )
				pm.joint(newJnts , e  = True , zso = True , oj = "xzy" , sao = "yup" , ch = True )  
			return newJnts
		
		else:
			pm.error ( "interpolate2Jnts command needs 2 sets of joints."  )
