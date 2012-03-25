#ifndef BEAST_CAMERA_SCRIPT_H
#define BEAST_CAMERA_SCRIPT_H
#include "scriptBase.h"

class BeastCameraInterface :
	public IScriptInterface
{
public:
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastCameraInterface> BeastCameraInterfacePtr;

#endif // end of BEAST_CAMERA_SCRIPT_H
