#include "beastInstanceScript.h"
#include <beastapi/beastinstance.h>
#include "common\vecmath.h"

ILBStatus ILBCreateInstance_WrapperFn(ILBSceneHandleWrapper& scene, 
									  ILBMeshHandleWrapper& mesh,
									  ILBConstString name, 
									  const bex::Matrix4x4* transform,
									  ILBInstanceHandleWrapper& instance)
{
	return ILBCreateInstance( scene.getHandle(), 
							  mesh.getHandle(),
							  name,
							  transform,
							  &(instance.getHandle()) );
}
ILBStatus ILBSetMaterialOverrides_WrapperFn(ILBInstanceHandleWrapper& _instance, 
										    ILBMaterialHandleWrapper& _materials,
											int32 _materialCount)
{
	return ILBSetMaterialOverrides( _instance.getHandle(), &(_materials.getHandle()), _materialCount );
}

ILBStatus ILBSetRenderStats_WrapperFn(ILBInstanceHandleWrapper& _instance, 
									  ILBRenderStatsMask _stats,
									  ILBRenderStatOperation _operation)
{
	return ILBSetRenderStats(_instance.getHandle(), _stats, _operation);
}

namespace bp = boost::python;
void BeastInstanceInterface::registerInterface(boost::python::object& nspace) 
{
	bp::enum_< ILBRenderStats>("ILBRenderStats")
		.value("ILB_RS_PRIMARY_VISIBILITY", ILB_RS_PRIMARY_VISIBILITY)
		.value("ILB_RS_CAST_SHADOWS", ILB_RS_CAST_SHADOWS)
		.value("ILB_RS_RECEIVE_SHADOWS", ILB_RS_RECEIVE_SHADOWS)
		.value("ILB_RS_RESERVED_1", ILB_RS_RESERVED_1)
		.value("ILB_RS_RESERVED_2", ILB_RS_RESERVED_2)
		.value("ILB_RS_VISIBLE_IN_REFLECTIONS", ILB_RS_VISIBLE_IN_REFLECTIONS)
		.value("ILB_RS_VISIBLE_IN_REFRACTIONS", ILB_RS_VISIBLE_IN_REFRACTIONS)
		.value("ILB_RS_VISIBLE_IN_FINAL_GATHER", ILB_RS_VISIBLE_IN_FINAL_GATHER)
		.value("ILB_RS_DOUBLE_SIDED", ILB_RS_DOUBLE_SIDED)
		.value("ILB_RS_OPPOSITE", ILB_RS_OPPOSITE)
		.value("ILB_RS_CAST_GI", ILB_RS_CAST_GI)
		.value("ILB_RS_RECEIVE_GI", ILB_RS_RECEIVE_GI)
		.value("ILB_RS_RESERVED_3", ILB_RS_RESERVED_3)
		.value("ILB_RS_RESERVED_4", ILB_RS_RESERVED_4)
		.value("ILB_RS_CAST_OCCLUSION", ILB_RS_CAST_OCCLUSION)
		.value("ILB_RS_RECEIVE_OCCLUSION", ILB_RS_RECEIVE_OCCLUSION)
		.value("ILB_RS_RESERVED_5", ILB_RS_RESERVED_5)
		.value("ILB_RS_RESERVED_6", ILB_RS_RESERVED_6)
		.value("ILB_RS_SELF_OCCLUSION", ILB_RS_SELF_OCCLUSION)
		.value("ILB_RS_SHADOW_BIAS", ILB_RS_SHADOW_BIAS)
		.export_values()
		;

	bp::enum_< ILBRenderStatOperation>("ILBRenderStatOperation")
		.value("ILB_RSOP_ENABLE", ILB_RSOP_ENABLE)
		.value("ILB_RSOP_DISABLE", ILB_RSOP_DISABLE)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBCreateInstance)
	DECLARE_METHOD_BINDING(ILBSetMaterialOverrides)
	DECLARE_METHOD_BINDING(ILBSetRenderStats)
}
