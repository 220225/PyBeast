#ifndef BEAST_TEXTURE_UTIL_SCRIPT_H
#define BEAST_TEXTURE_UTIL_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastTextureUtilInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastTextureUtilInterface> BeastTextureUtilInterfacePtr;

#endif // end of BEAST_TEXTURE_UTIL_SCRIPT_H
