#ifndef BEAST_LIGHT_SOURCE_SCRIPT_H
#define BEAST_LIGHT_SOURCE_SCRIPT_H

#include <boost/python.hpp>
#include "scriptBase.h"
#include "beastapitypesScript.h"

DECLARE_DATATYPE_WRAPPER(ILBLightType, ILB_LST_DIRECTIONAL)
DECLARE_DATATYPE_WRAPPER(ILBLightStatsMask, 0)
DECLARE_DATATYPE_WRAPPER(ILBLightVolumeType, ILB_LVT_INFINITY)
DECLARE_DATATYPE_WRAPPER(ILBFalloffType, ILB_FO_EXPONENT)

class BeastLightSourceInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastLightSourceInterface> BeastLightSourceInterfacePtr;

#endif // end of BEAST_LIGHT_SOURCE_SCRIPT_H
