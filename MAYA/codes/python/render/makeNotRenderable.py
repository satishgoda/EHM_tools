import pymel.core as pm
objs = pm.ls(sl=True)

renderAttrs = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","visibleInReflections","visibleInRefractions", "aiVisibleInDiffuse", "aiVisibleInGlossy"]
for obj in objs:
	for attr in renderAttrs:
		obj.attr(attr).set(0)