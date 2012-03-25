#ifndef BEAST_TARGETENTITY_SCRIPT_H
#define BEAST_TARGETENTITY_SCRIPT_H

#include <beastapi/beasttargetentity.h>
#include "scriptBase.h"
#include "beastapitypesScript.h"

DECLARE_DATATYPE_WRAPPER(ILBTargetEntityType, ILB_TT_TEXTURE)

class BeastTargetEntityInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastTargetEntityInterface> BeastTargetEntityInterfacePtr;

#endif // end of BEAST_TARGETENTITY_SCRIPT_H
