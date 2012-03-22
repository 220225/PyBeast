#ifndef BEAST_MANAGER_SCRIPT_H
#define BEAST_MANAGER_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastManagerInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastManagerInterface> BeastManagerInterfacePtr;

#endif // end of BEAST_MANAGER_SCRIPT_H
