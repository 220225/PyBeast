#ifndef BEAST_VECMATH_UTIL_SCRIPT_H
#define BEAST_VECMATH_UTIL_SCRIPT_H

#include "scriptBase.h"

class BeastVecMathUtilInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastVecMathUtilInterface> BeastVecMathUtilInterfacePtr;

#endif // end of BEAST_VECMATH_UTIL_SCRIPT_H
