'''
What does this do: copies set driven keys to object in the other side

Notes: finds other object by replacing 'L_' and 'R_', so be careful with the names

How to use: 
select driven object and run this

copySetDrivenKeys()


'''


import pymel.core as pm


def CopySetDrivenKeys( objs=None ):
	if not objs:
		objs = pm.ls( sl=True )
	else:
		objs = pm.ls( objs )

	def getMirror( obj ):
		objName = obj.name()
		if objName[:2]==('L_'):
			otherName = obj.name().replace('L_','R_')
		elif objName[:2]==('R_'):
			otherName = obj.name().replace('R_','L_')
		else:
			otherName = obj.name()
		if pm.objExists( otherName ):
			otherObj = pm.PyNode( otherName )
		else:
			otherObj = None
		return otherObj

	for obj in objs:		
		otherObj = getMirror( obj )
			
		# for each blend weight that is connected to our object, find all blend weights and it's inputs all the way to driver object
		blendWeightInputs = pm.listConnections( obj, type='blendWeighted', skipConversionNodes=True )

		for BWinput in blendWeightInputs:

			# duplicate BWinput
			otherBWinput = pm.duplicate( BWinput )[0]		

			# finds destAttr even if unit conversion exists
			destAttr = pm.listConnections( BWinput.output, destination=True, source=False, plugs=False )[0]
			if destAttr.type()=='unitConversion':
				destAttr = pm.listConnections( destAttr.output, destination=True, source=False, plugs=True)[0].split('.')[-1]
			else:
				destAttr = pm.listConnections( BWinput.output, destination=True, source=False, plugs=True)[0].split('.')[-1]

			# finds animCurves
			animCurves = pm.listConnections( BWinput, source=True, destination=False, skipConversionNodes=True, plugs=False )			

			i = 0
			for animCurve in animCurves:


				# duplicate anim curve
				otherAnimCurve = pm.duplicate( animCurve )[0]
				
				try: # in case anim curve doesn't have any inputs, no error will occur
					driverObj = pm.listConnections( animCurve.input, source=True, destination=False, skipConversionNodes=True )[0]
				except:
					pm.warning( 'Driver object for "%s" not found!'%animCurve )
					pass
				
				try: # in case anim curve doesn't have any inputs, no error will occur
					driverAttrName = (pm.listConnections( animCurve.input, source=True, destination=False, plugs=True, skipConversionNodes=True )[0]).split('.')[-1]	
				except:
					pm.warning( 'Driver Attribute for "%s" not found!'%animCurve  )
					pass
				
				otherDriver = getMirror( driverObj )	
				
				# connect input to anim curve
				otherDriver.attr(driverAttrName) >> otherAnimCurve.input	
				# connect anim to other blend weight node
				otherAnimCurve.output >> otherBWinput.input[i]
						
				i += 1

				
			# connect  blend weight node to final attribute		
			otherBWinput.output  >> otherObj.attr( destAttr )
			


		# for each animCurve that is connected to our object, find driver attributes
		animCurveInputs = pm.listConnections( obj, type='animCurve', skipConversionNodes=True )
		for animCurve in animCurveInputs:
			# duplicate anim curve
			otherAnimCurve = pm.duplicate( animCurve )[0]
			
			# finds destAttr even if unit conversion exists
			destAttr = pm.listConnections( animCurve.output, destination=True, source=False, plugs=False )[0]
			if destAttr.type()=='unitConversion':
				destAttr = pm.listConnections( destAttr.output, destination=True, source=False, plugs=True)[0].split('.')[-1]
			else:
				destAttr = pm.listConnections( animCurve.output, destination=True, source=False, plugs=True)[0].split('.')[-1]

			try: # in case anim curve doesn't have any inputs, no error will occur
				driverObj = pm.listConnections( animCurve.input, source=True, destination=False, skipConversionNodes=True )[0]
			except:
				pm.warning( 'Driven object not found!' )
				pass
			
			try: # in case anim curve doesn't have any inputs, no error will occur
				driverAttrName = (pm.listConnections( animCurve.input, source=True, destination=False, plugs=True, skipConversionNodes=True )[0]).split('.')[-1]	
			except:
				pm.warning( 'Driven attribute not found!' )
				pass			
			
			otherDriver = getMirror( driverObj )	

			# connect input to anim curve
			otherDriver.attr(driverAttrName) >> otherAnimCurve.input	
			# connect anim to final attribute
			otherAnimCurve.output >> otherObj.attr( destAttr )

