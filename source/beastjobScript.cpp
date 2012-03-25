#include "beastjobScript.h"
#include "beastUtilScript.h"
#include <boost/python.hpp>
#include "beastapi/beastjob.h"

namespace bp = boost::python;
ILBStatus ILBCreateJob_WrapperFn(ILBManagerHandleWrapper& _manager, 
							  	 ILBConstString _uniqueName,
							  	 ILBSceneHandleWrapper& _scene,
								 ILBConstString _jobXML,
								 ILBJobHandleWrapper& _job)
{
	return ILBCreateJob( _manager.getHandle(), _uniqueName, _scene.getHandle(), _jobXML, &(_job.getHandle()) );
}
ILBStatus ILBDestroyJob_WrapperFn( ILBJobHandleWrapper& _job)
{
	return ILBDestroyJob( _job.getHandle() );
}
ILBStatus ILBStartJob_WrapperFn(ILBJobHandleWrapper& _job, ILBShowResults _showResults, ILBDistributionType _distribution)
{
	return ILBStartJob(_job.getHandle(), _showResults, _distribution);
}

ILBStatus ILBWaitJobDone_WrapperFn(ILBJobHandleWrapper& _job, int32 _timeout)
{
	return ILBWaitJobDone(_job.getHandle(), _timeout);
}

ILBStatus ILBIsJobCompleted_WrapperFn(ILBJobHandleWrapper& _job, ILBBoolWrapper& _result)
{
	int32 localResult;
	ILBStatus status = ILBIsJobCompleted(_job.getHandle(), &localResult);
	_result.m_value = localResult>0 ? true : false;

	return status;
}
ILBStatus ILBIsJobRunning_WrapperFn(ILBJobHandleWrapper& _job, ILBBoolWrapper& _result)
{
	int32 localResult;
	ILBStatus status = ILBIsJobRunning(_job.getHandle(), &localResult);
	_result.m_value = localResult>0 ? true : false;
	return status;
}


ILBStatus ILBJobHasNewProgress_WrapperFn(ILBJobHandleWrapper& _job, ILBBoolWrapper& _newActivity, ILBBoolWrapper& _newProgress)
{
	ILBBool newActivityResult, newProgressResult;
	ILBStatus status = ILBJobHasNewProgress(_job.getHandle(), &newActivityResult, &newProgressResult);
	_newActivity.m_value = newActivityResult > 0 ? true : false;
	_newProgress.m_value = newProgressResult > 0 ? true : false;
	return status;
}

ILBStatus ILBGetJobProgress_WrapperFn(ILBJobHandleWrapper& _job, ILBStringHandleWrapper& _jobName, ILBInt32Wrapper& _progress)
{
	return ILBGetJobProgress(_job.getHandle(), &(_jobName.getHandle()), &_progress.m_value);
}
ILBStatus ILBGetJobResult_WrapperFn(ILBJobHandleWrapper& _job, ILBJobStatusWrapper& _status)
{
	return ILBGetJobResult(_job.getHandle(), &(_status.m_value));
}
ILBStatus ILBGetJobUpdateType_WrapperFn(ILBJobUpdateHandleWrapper& _update,
											   ILBUpdateTypeWrapper& _updateType)
{
	return ILBGetJobUpdateType(_update.getHandle(), &(_updateType.m_value));
}
ILBStatus ILBGetJobUpdate_WrapperFn(ILBJobHandleWrapper& _job, 
										   ILBBoolWrapper& _hasUpdate, 
										   ILBJobUpdateHandleWrapper& _updateHandle)
{
	ILBBool localHasUpdate;

	ILBStatus status = ILBGetJobUpdate(_job.getHandle(), &localHasUpdate, &(_updateHandle.getHandle()));
	_hasUpdate.m_value = localHasUpdate> 0 ? true : false;;
	return status;
}

ILBStatus ILBExecuteBeast_WrapperFn(ILBManagerHandleWrapper& _bm, 
										   ILBJobHandleWrapper& _job,
										   ILBShowResults _showResults,
										   ILBDistributionType _distribution, 
										   ILBJobStatusWrapper& _status)
{
	return ILBExecuteBeast(_bm.getHandle(), _job.getHandle(), _showResults, _distribution, &(_status.m_value));
}


ILBStatus ILBGetUpdateLightSource_WrapperFn(ILBJobUpdateHandleWrapper& _update, 
												   ILBLightHandleWrapper& _light)
{
	return ILBGetUpdateLightSource(_update.getHandle(), &(_light.getHandle()));
}

ILBStatus ILBCreateErnstJob_WrapperFn(ILBManagerHandleWrapper& _beastManager, 
											 ILBConstString _uniqueName, 
											 ILBSceneHandleWrapper& _scene, 
											 ILBConstString _jobXML, 
											 ILBJobHandleWrapper& _job)
{
	return ILBCreateErnstJob(_beastManager.getHandle(), _uniqueName, _scene.getHandle(), _jobXML, &(_job.getHandle()));
}
ILBStatus ILBDestroyUpdate_WrapperFn(ILBJobUpdateHandleWrapper& _update)
{
	return ILBDestroyUpdate(_update.getHandle());
}

ILBStatus ILBGetUpdateSceneInfo_WrapperFn(ILBJobUpdateHandleWrapper& _update, 
												 ILBSceneInfoHandleWrapper& _sceneInfo)
{
	return ILBGetUpdateSceneInfo(_update.getHandle(), &(_sceneInfo.getHandle()));
}

ILBStatus ILBGetUpdateCamera_WrapperFn(ILBJobUpdateHandleWrapper& _update, 
											  ILBCameraHandleWrapper& _camera)
{
	return ILBGetUpdateCamera(_update.getHandle(), &(_camera.getHandle()));
}

ILBStatus ILBGetUpdateTargetEntity_WrapperFn(ILBJobUpdateHandleWrapper& _update,
													ILBTargetEntityHandleWrapper& _targetEntity)
{
	return ILBGetUpdateTargetEntity(_update.getHandle(), &(_targetEntity.getHandle()));
}


void BeastJobInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_DATATYPE_BINDING(ILBJobStatus, createNewJobStatus)
	DECLARE_DATATYPE_BINDING(ILBUpdateType, createNewUpdateType)

	bp::enum_< ILBUpdateType>("ILBUpdateType")
		.value("ILB_UT_NEW_LIGHTSOURCE", ILB_UT_NEW_LIGHTSOURCE)
		.value("ILB_UT_UPDATE_LIGHTSOURCE", ILB_UT_UPDATE_LIGHTSOURCE)
		.value("ILB_UT_DELETE_LIGHTSOURCE", ILB_UT_DELETE_LIGHTSOURCE)
		.value("ILB_UT_SCENE_INFO", ILB_UT_SCENE_INFO)
		.value("ILB_UT_UPDATE_CAMERA", ILB_UT_UPDATE_CAMERA)
		.value("ILB_UT_UPDATE_TARGET", ILB_UT_UPDATE_TARGET)
		.export_values()
		;

	bp::enum_< ILBShowResults>("ILBShowResults")
		.value("ILB_SR_NO_DISPLAY", ILB_SR_NO_DISPLAY)
		.value("ILB_SR_CLOSE_WHEN_DONE", ILB_SR_CLOSE_WHEN_DONE)
		.value("ILB_SR_KEEP_OPEN", ILB_SR_KEEP_OPEN)
		.export_values()
		;

	bp::enum_< ILBDistributionType>("ILBDistributionType")
		.value("ILB_RD_FORCE_LOCAL", ILB_RD_FORCE_LOCAL)
		.value("ILB_RD_AUTODETECT", ILB_RD_AUTODETECT)
		.value("ILB_RD_FORCE_DISTRIBUTED", ILB_RD_FORCE_DISTRIBUTED)
		.export_values()
		;

	bp::enum_< ILBJobStatus>("ILBJobStatus")
		.value("ILB_JS_SUCCESS", ILB_JS_SUCCESS)
		.value("ILB_JS_CANCELLED", ILB_JS_CANCELLED)
		.value("ILB_JS_INVALID_LICENSE", ILB_JS_INVALID_LICENSE)
		.value("ILB_JS_CMDLINE_ERROR", ILB_JS_CMDLINE_ERROR)
		.value("ILB_JS_CONFIG_ERROR", ILB_JS_CONFIG_ERROR)
		.value("ILB_JS_CRASH", ILB_JS_CRASH)
		.value("ILB_JS_OTHER_ERROR", ILB_JS_OTHER_ERROR)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBExecuteBeast)
	DECLARE_METHOD_BINDING(ILBCreateJob)
	DECLARE_METHOD_BINDING(ILBCreateErnstJob)
	DECLARE_METHOD_BINDING(ILBDestroyJob)
	DECLARE_METHOD_BINDING(ILBDestroyUpdate)
	DECLARE_METHOD_BINDING(ILBStartJob)
	DECLARE_METHOD_BINDING(ILBWaitJobDone)
	DECLARE_METHOD_BINDING(ILBIsJobCompleted)
	DECLARE_METHOD_BINDING(ILBJobHasNewProgress)
	DECLARE_METHOD_BINDING(ILBGetJobProgress)
	DECLARE_METHOD_BINDING(ILBGetJobResult)
	DECLARE_METHOD_BINDING(ILBIsJobRunning)
	DECLARE_METHOD_BINDING(ILBGetJobUpdateType)
	DECLARE_METHOD_BINDING(ILBGetJobUpdate)
	DECLARE_METHOD_BINDING(ILBGetUpdateLightSource)
	DECLARE_METHOD_BINDING(ILBGetUpdateSceneInfo)
	DECLARE_METHOD_BINDING(ILBGetUpdateCamera)
	DECLARE_METHOD_BINDING(ILBGetUpdateTargetEntity)

}
