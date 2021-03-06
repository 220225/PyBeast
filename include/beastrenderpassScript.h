#ifndef BEAST_RENDER_PASS_SCRIPT_H
#define BEAST_RENDER_PASS_SCRIPT_H

#include "scriptBase.h"

class BeastRenderPassInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastRenderPassInterface> BeastRenderPassInterfacePtr;

#endif // end of BEAST_RENDER_PASS_SCRIPT_H
