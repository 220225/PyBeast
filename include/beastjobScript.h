#ifndef BEAST_JOB_SCRIPT_H
#define BEAST_JOB_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "beastapi\beastjob.h"
#include "scriptBase.h"

//struct ILBJobStatusWrapper {
//	ILBJobStatus m_value;
//	ILBJobStatusWrapper() : m_value(ILB_JS_SUCCESS) {}
//};
//struct ILBUpdateTypeWrapper {
//	ILBUpdateType m_value;
//	ILBUpdateTypeWrapper() : m_value(ILB_UT_UPDATE_TARGET) {}
//};
DECLARE_DATATYPE_WRAPPER(ILBJobStatus, ILB_JS_SUCCESS)
DECLARE_DATATYPE_WRAPPER(ILBUpdateType, ILB_UT_UPDATE_TARGET)

class BeastJobInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastJobInterface> BeastJobInterfacePtr;

#endif // end of BEAST_JOB_SCRIPT_H
