#include "beastapitypesScript.h"
#include "beastUtilScript.h"
#include "beastcameraScript.h"
#include "beastapi\beastcamera.h"
#include "common\vecmath.h"
namespace bp = boost::python;

ILBStatus ILBCreatePerspectiveCamera_WrapperFn(ILBSceneHandleWrapper& _scene, 
		ILBConstString _name, 
		const bex::Matrix4x4* _transform,
		ILBCameraHandleWrapper& _camera)
{
	return ILBCreatePerspectiveCamera( _scene.getHandle(), _name, _transform, &(_camera.getHandle()) );
}
ILBStatus ILBSetFov_WrapperFn(ILBCameraHandleWrapper& _camera, 
							  float _horizontalFovRadians,
							  float _pixelAspectRatio)
{
	return ILBSetFov( _camera.getHandle(), _horizontalFovRadians, _pixelAspectRatio );
}

ILBStatus ILBGetCameraTransform_WrapperFn(ILBCameraHandleWrapper& _camera,
												 bex::Matrix4x4* _transform)
{
	return ILBGetCameraTransform(_camera.getHandle(), _transform);
}

ILBStatus ILBGetCameraName_WrapperFn(ILBCameraHandleWrapper& _camera,
											ILBStringHandleWrapper& _name)
{
	return ILBGetCameraName(_camera.getHandle(), &(_name.getHandle()));
}

ILBStatus ILBGetCameraFov_WrapperFn(ILBCameraHandleWrapper& _camera, 
										   ILBFloatWrapper& _horizontalFovRadians,
										   ILBFloatWrapper& _pixelAspectRatio)
{
	return ILBGetCameraFov(_camera.getHandle(), &(_horizontalFovRadians.m_value), &(_pixelAspectRatio.m_value));
}


void BeastCameraInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_METHOD_BINDING(ILBCreatePerspectiveCamera)
	DECLARE_METHOD_BINDING(ILBSetFov)
	DECLARE_METHOD_BINDING(ILBGetCameraTransform)
	DECLARE_METHOD_BINDING(ILBGetCameraName)
	DECLARE_METHOD_BINDING(ILBGetCameraFov)

}
