#ifndef BEAST_MESH_SCRIPT_H
#define BEAST_MESH_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastMeshInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastMeshInterface> BeastMeshInterfacePtr;

#endif // end of BEAST_MESH_SCRIPT_H
