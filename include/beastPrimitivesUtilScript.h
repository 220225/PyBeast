#ifndef BEAST_PRIMITVIES_UTIL_SCRIPT_H
#define BEAST_PRIMITVIES_UTIL_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastPrimitivesUtilInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastPrimitivesUtilInterface> BeastPrimitivesUtilInterfacePtr;

#endif // end of BEAST_PRIMITVIES_UTIL_SCRIPT_H
