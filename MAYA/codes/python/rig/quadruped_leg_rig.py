# find the best place for stifle and hock joints in a quadruped

'''
import pymel.core as pm
dt = pm.datatypes
objs = pm.ls(sl=True)
'''

hipPnt = dt.Vector ( pm.xform( objs[0], q=True, ws=True, t=True ) )
stiflePnt = dt.Vector ( pm.xform( objs[1], q=True, ws=True, t=True ) )
hockPnt = dt.Vector ( pm.xform( objs[2], q=True, ws=True, t=True ) )
anklePnt = dt.Vector ( pm.xform( objs[3], q=True, ws=True, t=True ) )


legRevVec = hipPnt-anklePnt
legVec = anklePnt-hipPnt
hipVec = stiflePnt-hipPnt
stifleVec = hockPnt-stiflePnt
hockVec = hockPnt-anklePnt


legLen = hipVec.length() + stifleVec.length() + hockVec.length()
limbLen = legLen / 4.0
legLineLen =  legVec.length() / 4.0
distFromLegLine = dt.sqrt( dt.pow(limbLen,2) - dt.pow(legLineLen,2) )

# find new stifle position
stifleStraighten = -legVec.normal() * (legLineLen)  # new stifle projected on leg
vecPerpToLegAndStifle = stifleStraighten.cross( hipVec ).normal()
legLineToStifle = vecPerpToLegAndStifle.cross( stifleStraighten ).normal()
stiflePos = (legLineToStifle * distFromLegLine) + hipPnt - stifleStraighten 

# find new hock position
hockPos = -(legLineToStifle * distFromLegLine) + anklePnt + stifleStraighten 


loc = pm.spaceLocator()
loc.translate.set( stiflePos )

loc = pm.spaceLocator()
loc.translate.set( hockPos )
