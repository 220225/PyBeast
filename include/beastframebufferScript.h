#ifndef BEAST_FRAMEBUFFER_SCRIPT_H
#define BEAST_FRAMEBUFFER_SCRIPT_H
#include "scriptBase.h"

class BeastFrameBufferInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastFrameBufferInterface> BeastFrameBufferInterfacePtr;

#endif // end of BEAST_FRAMEBUFFER_SCRIPT_H
