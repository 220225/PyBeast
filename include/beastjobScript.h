#ifndef BEAST_JOB_SCRIPT_H
#define BEAST_JOB_SCRIPT_H
#include "scriptBase.h"
#include "beastapitypesScript.h"

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
