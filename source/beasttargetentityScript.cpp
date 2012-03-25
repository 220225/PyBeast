#include "beasttargetentityScript.h"
#include "beastUtilScript.h"
#include "common/vecmath.h"
#include <boost/python.hpp>
namespace bp = boost::python;

ILBStatus ILBSetBakeResolution_WrapperFn(ILBTargetEntityHandleWrapper& _target, 
												int32 _width, 
												int32 _height)
{
	return ILBSetBakeResolution( _target.getHandle(), _width, _height);
}
ILBStatus ILBGetAtlasInformation_WrapperFn(ILBTargetEntityHandleWrapper& _te,
																		   ILBInt32Wrapper& _framebufferIndex,
																		   bex::Vec2& _offset,
																		   bex::Vec2& _scale)
{
	return ILBGetAtlasInformation(_te.getHandle(), &(_framebufferIndex.m_value), &_offset, &_scale);
}

ILBStatus ILBSetUVTransform_WrapperFn(ILBTargetEntityHandleWrapper& _target,
									  bex::Vec2& _offset,
									  bex::Vec2& _scale)
{
	return ILBSetUVTransform(_target.getHandle(), &_offset, &_scale);
}
ILBStatus ILBGetTargetEntityInstance_WrapperFn(ILBTargetEntityHandleWrapper& _entity,
													  ILBStringHandleWrapper& _name)
{
	return ILBGetTargetEntityInstance(_entity.getHandle(), &(_name.getHandle()));
}
ILBStatus ILBGetTargetEntityResolution_WrapperFn(ILBTargetEntityHandleWrapper& _entity, 
														ILBInt32Wrapper& _width, 
														ILBInt32Wrapper& _height)
{
	return ILBGetTargetEntityResolution(_entity.getHandle(), &(_width.m_value), &(_height.m_value));
}


ILBStatus ILBGetTargetEntityType_WrapperFn(ILBTargetEntityHandleWrapper& _entity, 
												  ILBTargetEntityTypeWrapper& _type)
{
	return ILBGetTargetEntityType(_entity.getHandle(), &(_type.m_value));
}

void BeastTargetEntityInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_DATATYPE_BINDING(ILBTargetEntityType, createNewTargetEntityType)

	bp::enum_< ILBTargetEntityType>("ILBTargetEntityType")
		.value("ILB_TT_TEXTURE", ILB_TT_TEXTURE)
		.value("ILB_TT_VERTEX", ILB_TT_VERTEX)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBSetBakeResolution)
	DECLARE_METHOD_BINDING(ILBGetAtlasInformation)
	DECLARE_METHOD_BINDING(ILBSetUVTransform)
	DECLARE_METHOD_BINDING(ILBGetTargetEntityType)
	DECLARE_METHOD_BINDING(ILBGetTargetEntityResolution)
	DECLARE_METHOD_BINDING(ILBGetTargetEntityInstance)

}
