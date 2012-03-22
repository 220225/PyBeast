#ifndef BEAST_SCENE_SCRIPT_H
#define BEAST_SCENE_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include <beastapi/beastscene.h>
#include "scriptBase.h"

DECLARE_DATATYPE_WRAPPER(ILBSceneUpVector, ILB_UP_POS_Y)

class BeastSceneInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastSceneInterface> BeastSceneInterfacePtr;

#endif // end of BEAST_SCENE_SCRIPT_H
