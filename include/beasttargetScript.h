#ifndef BEAST_TARGET_SCRIPT_H
#define BEAST_TARGET_SCRIPT_H

#include "scriptBase.h"

class BeastTargetInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastTargetInterface> BeastTargetInterfacePtr;

#endif // end of BEAST_TARGET_SCRIPT_H
