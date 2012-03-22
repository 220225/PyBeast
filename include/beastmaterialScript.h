#ifndef BEAST_MATERIAL_SCRIPT_H
#define BEAST_MATERIAL_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastMaterialInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastMaterialInterface> BeastMaterialInterfacePtr;

#endif // end of BEAST_MATERIAL_SCRIPT_H
