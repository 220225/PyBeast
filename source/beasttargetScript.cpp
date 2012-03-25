#include "beastapitypesScript.h"
#include "beasttargetScript.h"
#include "beastUtilScript.h"
#include "beastapi/beasttarget.h"
#include <boost/python.hpp>

namespace bp = boost::python;

ILBStatus ILBAddPassToTarget_WrapperFn(ILBTargetHandleWrapper& _target, 
									   ILBRenderPassHandleWrapper& _pass)
{
	return ILBAddPassToTarget( _target.getHandle(), _pass.getHandle() );
}
ILBStatus ILBCreateCameraTarget_WrapperFn(ILBJobHandleWrapper& _job, 
										  ILBConstString _name,
										  ILBCameraHandleWrapper& _camera,
										  int32 _width,
										  int32 _height,
										  ILBTargetHandleWrapper& _target)
{
	return ILBCreateCameraTarget( _job.getHandle(), _name, _camera.getHandle(), _width, _height, &(_target.getHandle()) );
}

ILBStatus ILBCreateTextureTarget_WrapperFn(ILBJobHandleWrapper& _job, 
												  ILBConstString _name,
												  int32 _width,
												  int32 _height,
												  ILBTargetHandleWrapper& _target)
{
	return ILBCreateTextureTarget( _job.getHandle(), _name, _width, _height, &(_target.getHandle()) );
}

ILBStatus ILBAddBakeInstance_WrapperFn(ILBTargetHandleWrapper& _target,
											  ILBInstanceHandleWrapper& _bakeInstance,
											  ILBTargetEntityHandleWrapper& _targetEntity)
{
	return ILBAddBakeInstance(_target.getHandle(), _bakeInstance.getHandle(), &(_targetEntity.getHandle()));
}

ILBStatus ILBCreateAtlasedTextureTarget_WrapperFn(ILBJobHandleWrapper& _job, 
																					   ILBConstString _name,
																					   int32 _maxWidth,
																					   int32 _maxHeight,
																					   int32 _maxTextures,
																				       ILBTargetHandleWrapper& _target)
{
	return ILBCreateAtlasedTextureTarget(_job.getHandle(), _name, _maxWidth, _maxHeight, _maxTextures, &(_target.getHandle()));
}
ILBStatus ILBGetFramebufferCount_WrapperFn(ILBTargetHandleWrapper& _target,
										   ILBInt32Wrapper& _count)
{
	return ILBGetFramebufferCount(_target.getHandle(), &_count.m_value);
}
ILBStatus ILBGetFramebuffer_WrapperFn(ILBTargetHandleWrapper& _target,
									  ILBRenderPassHandleWrapper& _pass,
									  int32 _index,
									  ILBFramebufferHandleWrapper& _fb)
{
	return ILBGetFramebuffer(_target.getHandle(), _pass.getHandle(), _index, &(_fb.getHandle()));
}
ILBStatus ILBCreateVertexTarget_WrapperFn(ILBJobHandleWrapper& _job, 
												 ILBConstString _name,
												 ILBTargetHandleWrapper& _target)
{
	return ILBCreateVertexTarget(_job.getHandle(), _name, &(_target.getHandle()));
}

ILBStatus ILBGetVertexbuffer_WrapperFn(ILBTargetHandleWrapper& _target,
											  ILBRenderPassHandleWrapper& _pass,
											  ILBTargetEntityHandleWrapper& _te,
											  ILBFramebufferHandleWrapper& _fb)
{
	return ILBGetVertexbuffer(_target.getHandle(), _pass.getHandle(), _te.getHandle(), &(_fb.getHandle()));
}
ILBStatus ILBCreatePointCloudTarget_WrapperFn(ILBJobHandleWrapper& _job, 
													 ILBConstString _name,
													 ILBTargetHandleWrapper& _target)
{
	return ILBCreatePointCloudTarget(_job.getHandle(), _name, &(_target.getHandle()));
}
ILBStatus ILBAddBakePointCloud_WrapperFn(ILBTargetHandleWrapper& _target,
												ILBPointCloudHandleWrapper& _pointCloud,
												ILBTargetEntityHandleWrapper& _targetEntity)
{
	return ILBAddBakePointCloud(_target.getHandle(), _pointCloud.getHandle(), &(_targetEntity.getHandle()));
}

void BeastTargetInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_METHOD_BINDING(ILBCreateCameraTarget)
	DECLARE_METHOD_BINDING(ILBCreateAtlasedTextureTarget)
	DECLARE_METHOD_BINDING(ILBCreateTextureTarget)
	DECLARE_METHOD_BINDING(ILBCreatePointCloudTarget)
	DECLARE_METHOD_BINDING(ILBAddPassToTarget)
	DECLARE_METHOD_BINDING(ILBAddBakeInstance)
	DECLARE_METHOD_BINDING(ILBGetFramebufferCount)
	DECLARE_METHOD_BINDING(ILBGetFramebuffer)
	DECLARE_METHOD_BINDING(ILBCreateVertexTarget)
	DECLARE_METHOD_BINDING(ILBGetVertexbuffer)
	DECLARE_METHOD_BINDING(ILBAddBakePointCloud)
}
