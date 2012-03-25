#ifndef BEAST_UTIL_SCRIPT_H
#define BEAST_UTIL_SCRIPT_H

#include "scriptBase.h"
#include "beastapitypesScript.h"

DECLARE_BASIC_DATATYPE_WRAPPER(ILBBool, bool, false)
DECLARE_BASIC_DATATYPE_WRAPPER(ILBInt32, int32, 0)
DECLARE_BASIC_DATATYPE_WRAPPER(ILBFloat, float, 0.0f)

class BeastUtilInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastUtilInterface> BeastUtilInterfacePtr;

#endif // end of BEAST_UTIL_SCRIPT_H
