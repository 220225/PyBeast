#include "beastsceneScript.h"
namespace bp = boost::python;

ILBStatus ILBBeginScene_WrapperFn(ILBManagerHandleWrapper& _managerHandleWrapper,
								  ILBConstString uniqueName,
								  ILBSceneHandleWrapper& _sceneHandleWrapper)
{
	return ILBBeginScene(_managerHandleWrapper.getHandle(), uniqueName, &(_sceneHandleWrapper.getHandle()));
}
ILBStatus ILBEndScene_WrapperFn(ILBSceneHandleWrapper& _scene)
{
	return ILBEndScene(_scene.getHandle());
}
ILBStatus ILBSetSceneUpVector_WrapperFn(ILBSceneHandleWrapper& _scene, ILBSceneUpVector _upVector)
{
	return ILBSetSceneUpVector(_scene.getHandle(), _upVector);
}
ILBStatus ILBSetMeterPerWorldUnit_WrapperFn(ILBSceneHandleWrapper& _scene, float _meterPerWorldUnit)
{
	return ILBSetMeterPerWorldUnit(_scene.getHandle(), _meterPerWorldUnit);
}

ILBStatus ILBReleaseScene_WrapperFn(ILBSceneHandleWrapper& _scene)
{
	return ILBReleaseScene(_scene.getHandle());
}

ILBStatus ILBGetMeterPerWorldUnit_WrapperFn(ILBSceneInfoHandleWrapper& _scene, ILBFloatWrapper& _meterPerWorldUnit)
{
	return ILBGetMeterPerWorldUnit(_scene.getHandle(), &(_meterPerWorldUnit.m_value));
}
ILBStatus ILBGetSceneUpVector_WrapperFn(ILBSceneInfoHandleWrapper& _scene, ILBSceneUpVectorWrapper& _upVector)
{
	return ILBGetSceneUpVector(_scene.getHandle(), &(_upVector.m_value));
}

void BeastSceneInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_DATATYPE_BINDING(ILBSceneUpVector, createNewSceneUpVector)

	bp::enum_< ILBSceneUpVector>("ILBSceneUpVector")
		.value("ILB_UP_POS_X", ILB_UP_POS_X)
		.value("ILB_UP_NEG_X", ILB_UP_NEG_X)
		.value("ILB_UP_POS_Y", ILB_UP_POS_Y)
		.value("ILB_UP_NEG_Y", ILB_UP_NEG_Y)
		.value("ILB_UP_POS_Z", ILB_UP_POS_Z)
		.value("ILB_UP_NEG_Z", ILB_UP_NEG_Z)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBBeginScene)
	DECLARE_METHOD_BINDING(ILBEndScene)
	DECLARE_METHOD_BINDING(ILBReleaseScene)
	DECLARE_METHOD_BINDING(ILBSetSceneUpVector)
	DECLARE_METHOD_BINDING(ILBSetMeterPerWorldUnit)
	DECLARE_METHOD_BINDING(ILBGetMeterPerWorldUnit)
	DECLARE_METHOD_BINDING(ILBGetSceneUpVector)

}
