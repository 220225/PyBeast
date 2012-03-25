#include "beastpointcloudScript.h"
#include "beastapitypesScript.h"
#include "common/vecmath.h"
#include "beastapi/beastpointcloud.h"
#include <boost/python.hpp>

namespace bp = boost::python;
using boost::shared_ptr;

ILBStatus ILBCreatePointCloud_WrapperFn(ILBSceneHandleWrapper& _scene, 
											   ILBConstString _name, 
											   ILBPointCloudHandleWrapper& _pointCloud)
{
	return ILBCreatePointCloud(_scene.getHandle(), _name, &(_pointCloud.getHandle()));
}
ILBStatus ILBEndPointCloud_WrapperFn(ILBPointCloudHandleWrapper& _pointCloud)
{
	return ILBEndPointCloud(_pointCloud.getHandle());
}
ILBStatus ILBAddPointCloudData_WrapperFn(ILBPointCloudHandleWrapper& _pointCloud, 
										 std::vector<bex::Vec3>& _pointData, 
										 std::vector<bex::Vec3>& _normalData, 
										 int32 _pointCount)
{
	return ILBAddPointCloudData(_pointCloud.getHandle(), &(_pointData[0]), &(_normalData[0]), _pointCount);
}

void BeastPointCloudInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_METHOD_BINDING(ILBCreatePointCloud)
	DECLARE_METHOD_BINDING(ILBEndPointCloud)
	DECLARE_METHOD_BINDING(ILBAddPointCloudData)
}
