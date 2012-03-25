#include "beastmanagerScript.h"
#include "beastapitypesScript.h"
#include <boost/python.hpp>
namespace bp = boost::python;

ILBStatus ILBCreateManager_WrapperFn(ILBConstString cacheDirectory, 
									 ILBCacheScope cacheScope,
									 ILBManagerHandleWrapper& _managerHandleWrapper)
{
	return ILBCreateManager(cacheDirectory, cacheScope, &(_managerHandleWrapper.getHandle()));
}

ILBStatus ILBSetBeastPath_WrapperFn(ILBManagerHandleWrapper& _managerHandleWrapper,
									 ILBConstString beastPath)
{
	return ILBSetBeastPath(_managerHandleWrapper.getHandle(), beastPath);
}

ILBStatus ILBClearCache_WrapperFn(ILBManagerHandleWrapper& _managerHandleWrapper)
{
	return ILBClearCache(_managerHandleWrapper.getHandle());
}
ILBStatus ILBSetLogTarget_WrapperFn(ILBLogType _type, ILBLogSink _sink, ILBConstString _filename)
{
	return ILBSetLogTarget(_type, _sink, _filename);
}

void BeastManagerInterface::registerInterface(boost::python::object& nspace) 
{
	bp::enum_< ILBLogType>("ILBLogType")
		.value("ILB_LT_ERROR", ILB_LT_ERROR)
		.value("ILB_LT_INFO", ILB_LT_INFO)
		.export_values()
		;
	bp::enum_< ILBLogSink>("ILBLogSink")
		.value("ILB_LS_NULL", ILB_LS_NULL)
		.value("ILB_LS_STDOUT", ILB_LS_STDOUT)
		.value("ILB_LS_STDERR", ILB_LS_STDERR)
		.value("ILB_LS_FILE", ILB_LS_FILE)
		.value("ILB_LS_DEBUG_OUTPUT", ILB_LS_DEBUG_OUTPUT)
		.export_values()
		;

	bp::enum_< ILBCacheScope>("ILBCacheScope")
		.value("ILB_CS_GLOBAL", ILB_CS_GLOBAL)
		.value("ILB_CS_LOCAL", ILB_CS_LOCAL)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBCreateManager)
	DECLARE_METHOD_BINDING(ILBSetBeastPath)
	DECLARE_METHOD_BINDING(ILBClearCache)
	DECLARE_METHOD_BINDING(ILBSetLogTarget)
}
