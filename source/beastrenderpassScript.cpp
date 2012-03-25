#include "beastapitypesScript.h"
#include "beastrenderpassScript.h"
#include "beastapi/beastrenderpass.h"
#include <boost/python.hpp>

namespace bp = boost::python;

ILBStatus ILBCreateFullShadingPass_WrapperFn(ILBJobHandleWrapper& _job, 
							  	 		 ILBConstString _name,
										 ILBRenderPassHandleWrapper& _pass)
{
	return ILBCreateFullShadingPass( _job.getHandle(), _name, &(_pass.getHandle()) );
}

ILBStatus ILBCreateAmbientOcclusionPass_WrapperFn(ILBJobHandleWrapper& _job, 
																						  ILBConstString _name,
																						  float _maxDistance,
																						  float _coneAngle,
																						  ILBRenderPassHandleWrapper& _pass)
{
	return ILBCreateAmbientOcclusionPass( _job.getHandle(), _name, _maxDistance, _coneAngle, &(_pass.getHandle()) );
}
ILBStatus ILBSetAOAdaptive_WrapperFn(ILBRenderPassHandleWrapper& _pass,
											float _accuracy, 
											float _smooth)
{
	return ILBSetAOAdaptive(_pass.getHandle(), _accuracy, _smooth);
}
ILBStatus ILBSetAONumRays_WrapperFn(ILBRenderPassHandleWrapper& _pass,
										   int32 _minRay, 
										   int32 _maxRay)
{
	return ILBSetAONumRays(_pass.getHandle(), _minRay, _maxRay);
}
ILBStatus ILBSetAOContrast_WrapperFn(ILBRenderPassHandleWrapper& _pass,
											float _contrast, 
											float _scale)
{
	return ILBSetAOContrast(_pass.getHandle(), _contrast, _scale);
}	
ILBStatus ILBSetAOUniformSampling_WrapperFn(ILBRenderPassHandleWrapper& _pass)
{
	return ILBSetAOUniformSampling(_pass.getHandle());
}
ILBStatus ILBSetAOSelfOcclusion_WrapperFn(ILBRenderPassHandleWrapper& _pass,
													  ILBAOSelfOcclusion _selfOcclusion)
{
	return ILBSetAOSelfOcclusion(_pass.getHandle(), _selfOcclusion);
}
ILBStatus ILBCreateLuaPass_WrapperFn(ILBJobHandleWrapper& _job,
											ILBConstString _name,
											ILBConstString _scriptFile,
											ILBRenderPassHandleWrapper& _pass)
{
	return ILBCreateLuaPass(_job.getHandle(), _name, _scriptFile, &(_pass.getHandle()));
}
ILBStatus ILBCreateRNMPass_WrapperFn(ILBJobHandleWrapper& _job, 
																	ILBConstString _name,
																	ILBIlluminationMode _mode,
																	int32 _samples,
																	ILBRNMBasis _basis,
																	ILBRenderPassHandleWrapper& _pass)
{
	return ILBCreateRNMPass(_job.getHandle(), _name, _mode, _samples,  _basis,&(_pass.getHandle()));
}
void BeastRenderPassInterface::registerInterface(boost::python::object& nspace) 
{
	bp::enum_< ILBAOSelfOcclusion>("ILBAOSelfOcclusion")
		.value("ILB_SO_DISABLED", ILB_SO_DISABLED)
		.value("ILB_SO_SET_ENVIRONMENT", ILB_SO_SET_ENVIRONMENT)
		.value("ILB_SO_ENABLED", ILB_SO_ENABLED)
		.export_values()
	;
	bp::enum_< ILBRNMBasis>("ILBRNMBasis")
		.value("ILB_RB_HL2", ILB_RB_HL2)
		.value("ILB_RB_UE3", ILB_RB_UE3)
		.value("ILB_RB_UE3_FLIPPED", ILB_RB_UE3_FLIPPED)
		.value("ILB_RB_CUSTOM", ILB_RB_CUSTOM)
		.export_values()
		;
	bp::enum_< ILBIlluminationMode>("ILBIlluminationMode")
		.value("ILB_IM_DIRECT_ONLY", ILB_IM_DIRECT_ONLY)
		.value("ILB_IM_INDIRECT_ONLY", ILB_IM_INDIRECT_ONLY)
		.value("ILB_IM_FULL", ILB_IM_FULL)
		.value("ILB_IM_FULL_AND_INDIRECT", ILB_IM_FULL_AND_INDIRECT)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBCreateFullShadingPass)
	DECLARE_METHOD_BINDING(ILBCreateAmbientOcclusionPass)
	DECLARE_METHOD_BINDING(ILBCreateLuaPass)
	DECLARE_METHOD_BINDING(ILBCreateRNMPass)
	DECLARE_METHOD_BINDING(ILBSetAOAdaptive)
	DECLARE_METHOD_BINDING(ILBSetAONumRays)
	DECLARE_METHOD_BINDING(ILBSetAOContrast)
	DECLARE_METHOD_BINDING(ILBSetAOUniformSampling)
	DECLARE_METHOD_BINDING(ILBSetAOSelfOcclusion)
}
