
from Pythons import xsi, c, log


def addCnsCurve( parent, name, centers, closed=False, degree=1 ):

	centers = list( centers )
	points=[]

	if len(centers)<2:
				log('Select 2 or more object to create curve and clusters.', c.siError )
				return
	
	if degree==3:
		
		if len(centers)==2:
			centers.insert( 0, centers[0] )
			centers.append( centers[-1] )
		
		elif len(centers)==3:
			centers.append( centers[-1] )
		

	for center in centers:
		points.append( center.Kinematics.Global.Transform.PosX )
		points.append( center.Kinematics.Global.Transform.PosY )
		points.append( center.Kinematics.Global.Transform.PosZ )
		points.append( 1.0 )


	curve = parent.AddNurbsCurve( points, None , closed, degree, 0 , c.siSINurbs, name )

	
	for i, center in enumerate(centers):
		cls = curve.ActivePrimitive.Geometry.AddCluster( c.siVertexCluster , 'center_%s'%str(i), [i] )
		xsi.ApplyOp( 'ClusterCenter', cls.FullName+';'+center.FullName )


	return curve

