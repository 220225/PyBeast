#include "beastapitypesScript.h"
#include "beastmaterialScript.h"
#include "common/vecmath.h"
#include <beastapi/beastmaterial.h>
#include <boost/python.hpp>
namespace bp = boost::python;

ILBStatus ILBCreateMaterial_WrapperFn(ILBSceneHandleWrapper& _scene,
								  	  ILBConstString name,
								  	  ILBMaterialHandleWrapper& _material)
{
	return ILBCreateMaterial(_scene.getHandle(), name, &(_material.getHandle()));
}

ILBStatus ILBSetMaterialTexture_WrapperFn(ILBMaterialHandleWrapper& _material,
								  	  	  ILBMaterialChannel _channel,
								  	  	  ILBTextureHandleWrapper& _texture)
{
	return ILBSetMaterialTexture(_material.getHandle(), _channel, _texture.getHandle());
}
ILBStatus ILBSetMaterialColor_WrapperFn(ILBMaterialHandleWrapper& _material,
										  ILBMaterialChannel _channel,
										  const bex::ColorRGBA* _color)
{
	return ILBSetMaterialColor(_material.getHandle(), _channel, _color);
}
ILBStatus ILBSetMaterialScale_WrapperFn(ILBMaterialHandleWrapper& _material,
										  ILBMaterialChannel _channel,
										  float _scale)
{
	return ILBSetMaterialScale(_material.getHandle(), _channel, _scale);
}

ILBStatus ILBSetChannelUVLayer_WrapperFn(ILBMaterialHandleWrapper& _material,
										 ILBMaterialChannel _channel,
										 ILBConstString _uvLayerName)
{
	return ILBSetChannelUVLayer(_material.getHandle(), _channel, _uvLayerName);
}

ILBStatus ILBSetMaterialUseVertexColors_WrapperFn(ILBMaterialHandleWrapper& _material, 
											      ILBMaterialChannel _channel)
{
	return ILBSetMaterialUseVertexColors(_material.getHandle(), _channel);
}

ILBStatus ILBSetAlphaAsTransparency_WrapperFn(ILBMaterialHandleWrapper& _material, 
											  ILBBool _alphaAsTransparency)
{
	return ILBSetAlphaAsTransparency(_material.getHandle(), _alphaAsTransparency);
}

void BeastMaterialInterface::registerInterface(boost::python::object& nspace) 
{
	bp::enum_< ILBMaterialChannel>("ILBMaterialChannel")
		.value("ILB_CC_DIFFUSE", ILB_CC_DIFFUSE)
		.value("ILB_CC_SPECULAR", ILB_CC_SPECULAR)
		.value("ILB_CC_EMISSIVE", ILB_CC_EMISSIVE)
		.value("ILB_CC_TRANSPARENCY", ILB_CC_TRANSPARENCY)
		.value("ILB_CC_SHININESS", ILB_CC_SHININESS)
		.value("ILB_CC_REFLECTION", ILB_CC_REFLECTION)
		.value("ILB_CC_TOTAL_CHANNELS", ILB_CC_TOTAL_CHANNELS)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBCreateMaterial)
	DECLARE_METHOD_BINDING(ILBSetMaterialTexture)
	DECLARE_METHOD_BINDING(ILBSetMaterialColor)
	DECLARE_METHOD_BINDING(ILBSetMaterialScale)
	DECLARE_METHOD_BINDING(ILBSetChannelUVLayer)
	DECLARE_METHOD_BINDING(ILBSetMaterialUseVertexColors)
	DECLARE_METHOD_BINDING(ILBSetAlphaAsTransparency)

}
