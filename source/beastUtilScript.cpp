#include "beastUtilScript.h"
#include "beastapi/beastutils.h"
#include "common/utils.h"
#include <boost/python.hpp>

namespace bp = boost::python;

#ifdef UNICODE
#define tcout std::wcout
#else
#define tcout std::cout
#endif

std::basic_string<TCHAR> convertStringHandle_WrapperFn(ILBStringHandleWrapper& h)
{
	int32 len;
	ILBGetLength(h.getHandle(), &len);
	// len -1 since basic_string allocates the null character
	std::basic_string<TCHAR> result(len - 1, '\0');
	ILBCopy(h.getHandle(), &result[0], static_cast<int32>(len));
	ILBReleaseString(h.getHandle());
	return result;
}

ILBStatus ILBErrorToString_WrapperFn(ILBStatus _error, 
											ILBStringHandleWrapper& _targetString)
{
	return ILBErrorToString(_error, &(_targetString.getHandle()));
}
ILBStatus ILBGetExtendErrorInformation_WrapperFn(ILBStringHandleWrapper& _targetString)
{
	return ILBGetExtendErrorInformation(&(_targetString.getHandle()));
}

void BeastUtilInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_BASIC_DATATYPE_BINDING(ILBBool, ILBBool, bool)
	DECLARE_BASIC_DATATYPE_BINDING(ILBInt32, ILBInt32, int32)
	DECLARE_BASIC_DATATYPE_BINDING(ILBFloat, ILBFloat, float)

	DECLARE_METHOD_BINDING(convertStringHandle)
	DECLARE_METHOD_BINDING(ILBErrorToString)
	DECLARE_METHOD_BINDING(ILBGetExtendErrorInformation)
}
