#include "beastlightsourceScript.h"
namespace bp = boost::python;

ILBStatus ILBCreateSkyLight_WrapperFn(ILBSceneHandleWrapper& _scene,
								  	  ILBConstString name,
								  	  const bex::Matrix4x4* transform,
									  const bex::ColorRGB* _intensity,
									  ILBLightHandleWrapper& _light)
{
	return ILBCreateSkyLight(_scene.getHandle(), name, transform, _intensity, &(_light.getHandle()));
}
ILBStatus ILBCreateDirectionalLight_WrapperFn(ILBSceneHandleWrapper& _scene,
								  	  ILBConstString name,
								  	  const bex::Matrix4x4* transform,
									  const bex::ColorRGB* _intensity,
									  ILBLightHandleWrapper& _light)
{
	return ILBCreateDirectionalLight(_scene.getHandle(), name, transform, _intensity, &(_light.getHandle()));
}
ILBStatus ILBSetCastShadows_WrapperFn(ILBLightHandleWrapper& _light,
								  									ILBBool _castShadows)
{
	return ILBSetCastShadows(_light.getHandle(), _castShadows);
}
ILBStatus ILBCreatePointLight_WrapperFn(ILBSceneHandleWrapper& _scene, 
																	 ILBConstString _name, 
																	 const bex::Matrix4x4* _transform,
																	 const bex::ColorRGB* _intensity,
																	 ILBLightHandleWrapper& _light)
{
	return ILBCreatePointLight(_scene.getHandle(), _name, _transform, _intensity, &(_light.getHandle()) );
}


ILBStatus ILBSetShadowSamples_WrapperFn(ILBLightHandleWrapper& _light,
								  	    int32 _samples)
{
	return ILBSetShadowSamples(_light.getHandle(), _samples);
}

ILBStatus ILBSetShadowAngle_WrapperFn(ILBLightHandleWrapper& _light,
								  									 float _angleRadians)
{
	return ILBSetShadowAngle(_light.getHandle(), _angleRadians);
}

ILBStatus ILBSetShadowRadius_WrapperFn(ILBLightHandleWrapper& _light,
																	  float _radius)
{
	return ILBSetShadowRadius(_light.getHandle(), _radius);
}
ILBStatus ILBCreateSpotLight_WrapperFn(ILBSceneHandleWrapper& _scene, 
									   ILBConstString _name, 
									   const bex::Matrix4x4* _transform,
									   const bex::ColorRGB* _intensity,
									   ILBLightHandleWrapper& _light)
{
	return ILBCreateSpotLight(_scene.getHandle(), _name, _transform, _intensity, &(_light.getHandle()) );
}
ILBStatus ILBCreateAreaLight_WrapperFn(ILBSceneHandleWrapper& _scene, 
									   ILBConstString _name, 
									   const bex::Matrix4x4* _transform,
									   const bex::ColorRGB* _intensity,
									   ILBLightHandleWrapper& _light)
{
	return ILBCreateAreaLight(_scene.getHandle(), _name, _transform, _intensity, &(_light.getHandle()) );
}
ILBStatus ILBSetSpotlightCone_WrapperFn(ILBLightHandleWrapper& _light, 
										float _angleRadians,
										float _penumbraAngleRadians,
										float _penumbraExponent)
{
	return ILBSetSpotlightCone(_light.getHandle(), _angleRadians, _penumbraAngleRadians, _penumbraExponent);
}
ILBStatus ILBSetFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
														 ILBFalloffType _type, 
														 float _exponent, 
														 float _cutoff,
														 ILBBool _clampToOne)
{
	return ILBSetFalloff(_light.getHandle(), _type, _exponent, _cutoff, _clampToOne);
}

ILBStatus ILBCreateWindowLight_WrapperFn(ILBSceneHandleWrapper& _scene, 
													 					  ILBConstString _name, 
													 					  const bex::Matrix4x4* _transform,
													 					  const bex::ColorRGB* _intensity,
													 					  ILBLightHandleWrapper& _light)
{
	return ILBCreateWindowLight(_scene.getHandle(), _name, _transform, _intensity, &(_light.getHandle()));
}

ILBStatus ILBSetLightRampEntry_WrapperFn(ILBLightHandleWrapper& _light,
																					  float _position,
																					  const bex::ColorRGB* _value)
{
	return ILBSetLightRampEntry(_light.getHandle(), _position, _value);
}

 ILBStatus ILBSetLightProjectedTexture_WrapperFn(ILBLightHandleWrapper& _light,
																ILBTextureHandleWrapper& _texture)
{
	return ILBSetLightProjectedTexture(_light.getHandle(), _texture.getHandle());
}

 ILBStatus ILBSetLightStats_WrapperFn(ILBLightHandleWrapper& _light, 
																ILBLightStatsMask _stats,
																ILBLightStatOperation _operation)
 {
	 return ILBSetLightStats(_light.getHandle(), _stats, _operation);
 }

 ILBStatus ILBSetLightDisplayName_WrapperFn(ILBLightHandleWrapper& _light, 
	 ILBConstString _displayName)
 {
	 return ILBSetLightDisplayName(_light.getHandle(), _displayName);
 }
 ILBStatus ILBSetLightIntensity_WrapperFn(ILBLightHandleWrapper& _light, 
	 float _intensity)
 {
	 return ILBSetLightIntensity(_light.getHandle(), _intensity);
 }
ILBStatus ILBSetIntensityScale_WrapperFn(ILBLightHandleWrapper& _light, 
	 float _directScale,
	 float _indirectScale)
{
	return ILBSetIntensityScale(_light.getHandle(), _directScale, _indirectScale);
}
ILBStatus ILBSetSkyLightVolumeType_WrapperFn(ILBLightHandleWrapper& _light, 
													ILBLightVolumeType _type)
{
	return ILBSetSkyLightVolumeType(_light.getHandle(), _type);
}

ILBStatus ILBGetLightName_WrapperFn(ILBLightHandleWrapper& _light,
									ILBStringHandleWrapper& _name)
{
	return ILBGetLightName(_light.getHandle(), &(_name.getHandle()));
}
ILBStatus ILBGetLightDisplayName_WrapperFn(ILBLightHandleWrapper& _light,
									ILBStringHandleWrapper& _displayName)
{
	return ILBGetLightDisplayName(_light.getHandle(), &(_displayName.getHandle()));
}
ILBStatus ILBGetLightColor_WrapperFn(ILBLightHandleWrapper& _light,
									 bex::ColorRGB* _color)
{
	return ILBGetLightColor(_light.getHandle(), _color);
}
ILBStatus ILBGetLightTransform_WrapperFn(ILBLightHandleWrapper& _light,
												 bex::Matrix4x4* _transform)
{
	return ILBGetLightTransform(_light.getHandle(), _transform);
}
ILBStatus ILBGetLightType_WrapperFn(ILBLightHandleWrapper& _light,
										   ILBLightTypeWrapper& _type)
{

	return ILBGetLightType(_light.getHandle(), &(_type.m_value));
}

ILBStatus ILBGetSpotlightCone_WrapperFn(ILBLightHandleWrapper& _light, 
											   ILBFloatWrapper& _angleRadians,
											   ILBFloatWrapper& _penumbraAngleRadians,
											   ILBFloatWrapper& _penumbraExponent)
{
	return ILBGetSpotlightCone(_light.getHandle(), &(_angleRadians.m_value), &(_penumbraAngleRadians.m_value), &(_penumbraExponent.m_value));
}
ILBStatus ILBGetShadowAngle_WrapperFn(ILBLightHandleWrapper& _light, ILBFloatWrapper& _angleRadians)
{
	return ILBGetShadowAngle(_light.getHandle(), &(_angleRadians.m_value));
}


ILBStatus ILBGetShadowRadius_WrapperFn(ILBLightHandleWrapper& _light, ILBFloatWrapper& _radius)
{
	return ILBGetShadowRadius(_light.getHandle(), &(_radius.m_value));
}
ILBStatus ILBGetSkyLightVolumeType_WrapperFn(ILBLightHandleWrapper& _light, ILBLightVolumeTypeWrapper& _type)
{
	return ILBGetSkyLightVolumeType(_light.getHandle(), &(_type.m_value));
}
ILBStatus ILBGetLightIntensity_WrapperFn(ILBLightHandleWrapper& _light, 
												ILBFloatWrapper& _intensity)
{
	return ILBGetLightIntensity(_light.getHandle(), &(_intensity.m_value));
}

ILBStatus ILBGetLightCastShadows_WrapperFn(ILBLightHandleWrapper& _light,
												  ILBBoolWrapper& _castShadows)
{
	ILBBool localCastShadows;
	ILBStatus status = ILBGetLightCastShadows(_light.getHandle(), &(localCastShadows));
	_castShadows.m_value = localCastShadows>0 ? true : false;

	return status;
}

ILBStatus ILBGetLightShadowSamples_WrapperFn(ILBLightHandleWrapper& _light,
													ILBInt32Wrapper& _shadowSamples)
{
	return ILBGetLightShadowSamples(_light.getHandle(), &(_shadowSamples.m_value));
}

ILBStatus ILBGetLightFalloffType_WrapperFn(ILBLightHandleWrapper& _light,
												  ILBFalloffTypeWrapper& _type)
{
	return ILBGetLightFalloffType(_light.getHandle(), &(_type.m_value));
}

ILBStatus ILBGetLightMaxRangeFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
													  ILBFloatWrapper& _cutoff, 
													  ILBFloatWrapper& _exponent)
{
	return ILBGetLightMaxRangeFalloff(_light.getHandle(), &(_cutoff.m_value), &(_exponent.m_value));
}

ILBStatus ILBGetLightExponentFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
													  ILBFloatWrapper& _cutoff, 
													  ILBFloatWrapper&  _exponent, 
													  ILBBoolWrapper& _clamp)
{
	ILBBool localClamp;
	ILBStatus status = ILBGetLightExponentFalloff(_light.getHandle(), &(_cutoff.m_value), &(_exponent.m_value), &localClamp);

	_clamp.m_value = localClamp > 0 ? true : false;
	return status;
}

ILBStatus ILBGetLightPolynomialFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
														ILBFloatWrapper& _cutoff, 
														ILBFloatWrapper& _constant, 
														ILBFloatWrapper& _linear, 
														ILBFloatWrapper& _quadratic, 
														ILBBoolWrapper& _clamp)
{
	ILBBool localClamp;
	ILBStatus status = ILBGetLightPolynomialFalloff(_light.getHandle(), &(_cutoff.m_value), &(_constant.m_value), &(_linear.m_value), &(_quadratic.m_value), &localClamp);

	_clamp.m_value = localClamp > 0 ? true : false;
	return status;
}
ILBStatus ILBGetLightIntensityScale_WrapperFn(ILBLightHandleWrapper& _light,
													 ILBFloatWrapper& _directScale,
													 ILBFloatWrapper& _indirectScale)
{
	return ILBGetLightIntensityScale(_light.getHandle(), &(_directScale.m_value), &(_indirectScale.m_value));
}

ILBStatus ILBGetLightStats_WrapperFn(ILBLightHandleWrapper& _light,
											ILBLightStatsMask _stats,
											ILBLightStatsMaskWrapper& _result)
{
	return ILBGetLightStats(_light.getHandle(), _stats, &(_result.m_value));
}


ILBStatus ILBGetSkyLightTexture_WrapperFn(ILBLightHandleWrapper& _light, ILBTextureHandleWrapper& _texture)
{
	return ILBGetSkyLightTexture(_light.getHandle(), &(_texture.getHandle()));
}
ILBStatus ILBGetSkyLightTextureFilter_WrapperFn(ILBLightHandleWrapper& _light, ILBFloatWrapper& _filter)
{
	return ILBGetSkyLightTextureFilter(_light.getHandle(), &(_filter.m_value));
}

ILBStatus ILBSetLightExponentFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
													  float _cutoff, 
													  float _exponent, 
													  ILBBool _clampToOne)
{
	return ILBSetLightExponentFalloff(_light.getHandle(), _cutoff, _exponent, _clampToOne);
}
ILBStatus ILBSetLightPolynomialFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
														float _cutoff, 
														float _constant, 
														float _linear, 
														float _quadratic, 
														ILBBool _clampToOne)
{
	return ILBSetLightPolynomialFalloff(_light.getHandle(), _cutoff, _constant, _linear, _quadratic, _clampToOne);
}

ILBStatus ILBSetLightMaxRangeFalloff_WrapperFn(ILBLightHandleWrapper& _light, 
													  float _cutoff, 
													  float _exponent)
{
	return ILBSetLightMaxRangeFalloff(_light.getHandle(), _cutoff, _exponent);
}

void BeastLightSourceInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_DATATYPE_BINDING(ILBLightType, createNewLightType)
	DECLARE_DATATYPE_BINDING(ILBLightVolumeType, createNewLightVolumeType)
	DECLARE_DATATYPE_BINDING(ILBFalloffType, createNewFalloffType)
	DECLARE_DATATYPE_BINDING(ILBLightStatsMask, createNewLightStatsMask)

	bp::enum_< ILBLightType>("ILBLightType")
		.value("ILB_LST_DIRECTIONAL", ILB_LST_DIRECTIONAL)
		.value("ILB_LST_POINT", ILB_LST_POINT)
		.value("ILB_LST_AREA", ILB_LST_AREA)
		.value("ILB_LST_SPOT", ILB_LST_SPOT)
		.value("ILB_LST_WINDOW", ILB_LST_WINDOW)
		.value("ILB_LST_SKY", ILB_LST_SKY)
		.export_values()
		;

	bp::enum_< ILBLightStats>("ILBLightStats")
		.value("ILB_LS_VISIBLE_FOR_EYE", ILB_LS_VISIBLE_FOR_EYE)
		.value("ILB_LS_VISIBLE_FOR_REFLECTIONS", ILB_LS_VISIBLE_FOR_REFLECTIONS)
		.value("ILB_LS_VISIBLE_FOR_REFRACTIONS", ILB_LS_VISIBLE_FOR_REFRACTIONS)
		.value("ILB_LS_VISIBLE_FOR_GI", ILB_LS_VISIBLE_FOR_GI)
		.export_values()
		;
	bp::enum_< ILBLightStatOperation>("ILBLightStatOperation")
		.value("ILB_LSOP_DISABLE", ILB_LSOP_DISABLE)
		.value("ILB_LSOP_ENABLE", ILB_LSOP_ENABLE)
		.export_values()
		;

	bp::enum_< ILBFalloffType>("ILBFalloffType")
		.value("ILB_FO_EXPONENT", ILB_FO_EXPONENT)
		.value("ILB_FO_MAX_RANGE", ILB_FO_MAX_RANGE)
		.value("ILB_FO_POLYNOMIAL", ILB_FO_POLYNOMIAL)
		.export_values()
		;

	bp::enum_< ILBLightVolumeType>("ILBLightVolumeType")
		.value("ILB_LVT_INFINITY", ILB_LVT_INFINITY)
		.value("ILB_LVT_SPHERE", ILB_LVT_SPHERE)
		.value("ILB_LVT_CUBE", ILB_LVT_CUBE)
		.export_values()
		;


	DECLARE_METHOD_BINDING(ILBCreateDirectionalLight)
	DECLARE_METHOD_BINDING(ILBCreateSpotLight)
	DECLARE_METHOD_BINDING(ILBCreateAreaLight)
	DECLARE_METHOD_BINDING(ILBCreatePointLight)
	DECLARE_METHOD_BINDING(ILBCreateWindowLight)
	DECLARE_METHOD_BINDING(ILBSetSpotlightCone)
	DECLARE_METHOD_BINDING(ILBSetLightStats)
	DECLARE_METHOD_BINDING(ILBCreateSkyLight)
	DECLARE_METHOD_BINDING(ILBSetCastShadows)
	DECLARE_METHOD_BINDING(ILBSetShadowSamples)
	DECLARE_METHOD_BINDING(ILBSetShadowAngle)
	DECLARE_METHOD_BINDING(ILBSetShadowRadius)
	DECLARE_METHOD_BINDING(ILBSetFalloff)
	DECLARE_METHOD_BINDING(ILBSetLightRampEntry)
	DECLARE_METHOD_BINDING(ILBSetLightProjectedTexture)
	DECLARE_METHOD_BINDING(ILBSetLightMaxRangeFalloff)
	DECLARE_METHOD_BINDING(ILBSetLightExponentFalloff)
	DECLARE_METHOD_BINDING(ILBSetLightPolynomialFalloff)
	DECLARE_METHOD_BINDING(ILBSetLightDisplayName)
	DECLARE_METHOD_BINDING(ILBSetLightIntensity)
	DECLARE_METHOD_BINDING(ILBSetIntensityScale)
	DECLARE_METHOD_BINDING(ILBSetSkyLightVolumeType)
	DECLARE_METHOD_BINDING(ILBGetLightName)
	DECLARE_METHOD_BINDING(ILBGetLightDisplayName)
	DECLARE_METHOD_BINDING(ILBGetLightColor)
	DECLARE_METHOD_BINDING(ILBGetLightTransform)
	DECLARE_METHOD_BINDING(ILBGetLightType)
	DECLARE_METHOD_BINDING(ILBGetShadowRadius)
	DECLARE_METHOD_BINDING(ILBGetSpotlightCone)
	DECLARE_METHOD_BINDING(ILBGetShadowAngle)
	DECLARE_METHOD_BINDING(ILBGetSkyLightVolumeType)
	DECLARE_METHOD_BINDING(ILBGetLightIntensity)
	DECLARE_METHOD_BINDING(ILBGetLightCastShadows)
	DECLARE_METHOD_BINDING(ILBGetLightShadowSamples)
	DECLARE_METHOD_BINDING(ILBGetLightFalloffType)
	DECLARE_METHOD_BINDING(ILBGetLightMaxRangeFalloff)
	DECLARE_METHOD_BINDING(ILBGetLightExponentFalloff)
	DECLARE_METHOD_BINDING(ILBGetLightPolynomialFalloff)
	DECLARE_METHOD_BINDING(ILBGetLightIntensityScale)
	DECLARE_METHOD_BINDING(ILBGetLightStats)
	DECLARE_METHOD_BINDING(ILBGetSkyLightTexture)
	DECLARE_METHOD_BINDING(ILBGetSkyLightTextureFilter)
}
