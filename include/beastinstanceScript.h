#ifndef BEAST_INSTANCE_SCRIPT_H
#define BEAST_INSTANCE_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastInstanceInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastInstanceInterface> BeastInstanceInterfacePtr;

#endif // end of BEAST_INSTANCE_SCRIPT_H
