#ifndef BEAST_TEXTURE_SCRIPT_H
#define BEAST_TEXTURE_SCRIPT_H

#include "scriptBase.h"

class BeastTextureInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastTextureInterface> BeastTextureInterfacePtr;

#endif // end of BEAST_TEXTURE_SCRIPT_H
