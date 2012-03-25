#ifndef BEAST_API_TYPES_SCRIPT_H
#define BEAST_API_TYPES_SCRIPT_H

#include <vector>
#include <boost/python.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "scriptBase.h"
#include <beastapi/beaststring.h>
#include <beastapi/beastutils.h>
#include <beastapi/beastmanager.h>
#include <beastapi/beastscene.h>
#include <beastapi/beastinstance.h>
#include <beastapi/beastlightsource.h>
#include <beastapi/beastcamera.h>
#include <beastapi/beastmaterial.h>
#include <beastapi/beasttarget.h>
#include <beastapi/beastrenderpass.h>
#include "beastapi/beastjob.h"

//using boost::shared_ptr;
#define DECLARE_CREATE_NEW_WRAPPER(name) \
	inline name##Wrapper* createNew_##name() { return new name##Wrapper; }

#define DECLARE_HANDLE_WRAPPER(name) \
	struct name##Wrapper { ##name name##Proxy; \
		##name& getHandle() {return name##Proxy;} \
	}; \
	DECLARE_CREATE_NEW_WRAPPER(name)
	

#define DECLARE_HANDLE_BINDING(name, bindingName) 	\
	boost::python::def(#bindingName, createNew_##name, boost::python::return_value_policy	 <boost::python::manage_new_object>()); \
	boost::python::class_< name##Wrapper >("name##Wrapper", boost::python::no_init);


typedef boost::python::return_value_policy<boost::python::return_by_value> return_by_value_t;
typedef boost::python::return_internal_reference<> return_by_internal_reference_t;
#define DECLARE_DATATYPE_WRAPPER(name, defaultValue) \
	struct name##Wrapper { \
		##name m_value; \
		name##Wrapper() : m_value(##defaultValue) {} \
	}; \
	DECLARE_CREATE_NEW_WRAPPER(name)

#define DECLARE_DATATYPE_BINDING(name, bindingName) \
	boost::python::class_< name##Wrapper>("name##Wrapper", boost::python::no_init) \
		.add_property( "value", \
		make_getter( &name##Wrapper::m_value, return_by_value_t() ), \
		make_setter( &name##Wrapper::m_value, return_by_internal_reference_t() ) ) \
		; \
	boost::python::def(#bindingName, createNew_##name, boost::python::return_value_policy<boost::python::manage_new_object>());


#define DECLARE_BASIC_DATATYPE_WRAPPER(name,  dataType, defaultValue) \
	struct name##Wrapper { \
		##dataType m_value; \
		name##Wrapper() : m_value(##defaultValue) {} \
		name##Wrapper(##dataType _value) : m_value(_value) {} \
	}; 

#define DECLARE_BASIC_DATATYPE_BINDING(name, bindingName, arg_1) \
	boost::python::class_< name##Wrapper>(#bindingName,  boost::python::init<##arg_1>()) \
		.def(boost::python::init<>()) \
		.add_property( "value", \
		make_getter( &name##Wrapper::m_value, return_by_value_t() ), \
		make_setter( &name##Wrapper::m_value, return_by_internal_reference_t() ) ) \
		;


#define DECLARE_METHOD_BINDING(name) 	boost::python::def(#name, name##_WrapperFn);

#define DECLARE_ARRAY_BINDING(name, bindingName) 	\
	boost::python::class_< std::vector<##name> > (#bindingName) \
		.def(boost::python::vector_indexing_suite< std::vector<##name> >()) \
		;

// DECLARE_DATATYPE_BINDING(ILBLightStatsMaskWrapper, ILBLightStatsMask)
// --->
// def("createNewLightStatsMask", createNewLightStatsMask, return_value_policy<boost::python::manage_new_object>());
//
//class_< ILBLightStatsMaskWrapper >("ILBLightStatsMaskWrapper", boost::python::no_init)
//.add_property( "value", 
//			  make_getter( &ILBLightStatsMaskWrapper::m_value, return_by_value_t() ),
//			  make_setter( &ILBLightStatsMaskWrapper::m_value, return_by_internal_reference_t() ) )
//			  ;

DECLARE_HANDLE_WRAPPER(ILBMeshHandle);
DECLARE_HANDLE_WRAPPER(ILBManagerHandle)
DECLARE_HANDLE_WRAPPER(ILBSceneHandle)
DECLARE_HANDLE_WRAPPER(ILBSceneInfoHandle)
DECLARE_HANDLE_WRAPPER(ILBInstanceHandle)
DECLARE_HANDLE_WRAPPER(ILBTextureHandle)
DECLARE_HANDLE_WRAPPER(ILBLightHandle)
DECLARE_HANDLE_WRAPPER(ILBMaterialHandle)
DECLARE_HANDLE_WRAPPER(ILBCameraHandle)
DECLARE_HANDLE_WRAPPER(ILBJobHandle)
DECLARE_HANDLE_WRAPPER(ILBRenderPassHandle)
DECLARE_HANDLE_WRAPPER(ILBTargetHandle)
DECLARE_HANDLE_WRAPPER(ILBTargetEntityHandle)
DECLARE_HANDLE_WRAPPER(ILBStringHandle)
DECLARE_HANDLE_WRAPPER(ILBFramebufferHandle)
DECLARE_HANDLE_WRAPPER(ILBPointCloudHandle)
DECLARE_HANDLE_WRAPPER(ILBJobUpdateHandle)

class BeastAPITypesInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastAPITypesInterface> BeastAPITypesInterfacePtr;

#endif // end of BEAST_API_TYPES_SCRIPT_H
