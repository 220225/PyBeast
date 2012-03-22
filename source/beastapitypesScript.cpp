#include "beastapitypesScript.h"
#include "common\vecmath.h"

namespace bp = boost::python;
using boost::shared_ptr;

template <class T>
struct by_value
{
	static T rewrap(T x)
	{
		return x;
	}
	static int size(void)
	{
		return sizeof(T);
	}
};

void BeastAPITypesInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_ARRAY_BINDING(unsigned char, UCharArray)
	DECLARE_ARRAY_BINDING(float, FloatArray)
	DECLARE_ARRAY_BINDING(bex::Vec2, Vec2Array)
	DECLARE_ARRAY_BINDING(bex::Vec3, Vec3Array)
	DECLARE_ARRAY_BINDING(int32, Int32Array)
	DECLARE_ARRAY_BINDING(bex::ColorRGBA, ColorRGBAArray)

	bp::enum_< ILBStatus>("ILBStatus")
		.value("ILB_ST_SUCCESS", ILB_ST_SUCCESS)
		.value("ILB_ST_INVALID_PARAMETER", ILB_ST_INVALID_PARAMETER)
		.value("ILB_ST_MEMORY_ALLOC_ERROR", ILB_ST_MEMORY_ALLOC_ERROR)
		.value("ILB_ST_DUPLICATE_NAME_ERROR", ILB_ST_DUPLICATE_NAME_ERROR)
		.value("ILB_ST_FUNCTION_NOT_IMPLEMENTED", ILB_ST_FUNCTION_NOT_IMPLEMENTED)
		.value("ILB_ST_INVALID_OBJECT_STATE", ILB_ST_INVALID_OBJECT_STATE)
		.value("ILB_ST_INVALID_HANDLE", ILB_ST_INVALID_HANDLE)
		.value("ILB_ST_FILE_IO_ERROR", ILB_ST_FILE_IO_ERROR)
		.value("ILB_ST_UNKNOWN_OBJECT", ILB_ST_UNKNOWN_OBJECT)
		.value("ILB_ST_NOT_SUPPORTED", ILB_ST_NOT_SUPPORTED)
		.value("ILB_ST_UNHANDLED_EXCEPTION", ILB_ST_UNHANDLED_EXCEPTION)
		.value("ILB_ST_JOB_EXECUTION_FAILURE", ILB_ST_JOB_EXECUTION_FAILURE)
		.value("ILB_ST_ATLAS_EXECUTION_FAILURE", ILB_ST_ATLAS_EXECUTION_FAILURE)
		.value("ILB_ST_LAST_ERROR", ILB_ST_LAST_ERROR)
		.export_values()
		;

	DECLARE_HANDLE_BINDING(ILBManagerHandle, createNewManagerHandle)
	DECLARE_HANDLE_BINDING(ILBMeshHandle, createNewMeshHandle)
	DECLARE_HANDLE_BINDING(ILBSceneHandle, createNewSceneHandle)
	DECLARE_HANDLE_BINDING(ILBSceneInfoHandle, createNewSceneInfoHandle)
	DECLARE_HANDLE_BINDING(ILBInstanceHandle, createNewInstanceHandle)
	DECLARE_HANDLE_BINDING(ILBTextureHandle, createNewTextureHandle)
	DECLARE_HANDLE_BINDING(ILBLightHandle, createNewLightHandle)
	DECLARE_HANDLE_BINDING(ILBMaterialHandle, createNewMaterialHandle)
	DECLARE_HANDLE_BINDING(ILBCameraHandle, createNewCameraHandle)
	DECLARE_HANDLE_BINDING(ILBJobHandle, createNewJobHandle)
	DECLARE_HANDLE_BINDING(ILBTargetHandle, createNewTargetHandle)
	DECLARE_HANDLE_BINDING(ILBRenderPassHandle, createNewRenderPassHandle)
	DECLARE_HANDLE_BINDING(ILBTargetEntityHandle, createNewTargetEntityHandle)
	DECLARE_HANDLE_BINDING(ILBStringHandle, createNewStringHandle)
	DECLARE_HANDLE_BINDING(ILBFramebufferHandle, createNewFramebufferHandle)
	DECLARE_HANDLE_BINDING(ILBPointCloudHandle, createNewPointCloudHandle)
	DECLARE_HANDLE_BINDING(ILBJobUpdateHandle, createNewJobUpdateHandle)

	// register a to-python converter for shared_ptr<ILBMeshHandleWrapper>.
	objects::class_value_wrapper<
		shared_ptr<ILBMeshHandleWrapper>
		, objects::make_ptr_instance<ILBMeshHandleWrapper, objects::pointer_holder<shared_ptr<ILBMeshHandleWrapper>,ILBMeshHandleWrapper> >
	>();


	// register a to-python converter for shared_ptr<ILBTextureHandleWrapper>.
	objects::class_value_wrapper<
		shared_ptr<ILBTextureHandleWrapper>
		, objects::make_ptr_instance<ILBTextureHandleWrapper, objects::pointer_holder<shared_ptr<ILBTextureHandleWrapper>,ILBTextureHandleWrapper> >
	>();

	def("rewrap_value_unsigned_char", by_value<unsigned char>::rewrap);
	def("rewrap_value_float", by_value<float>::rewrap);
	def("rewrap_value_int", by_value<int>::rewrap);
}
