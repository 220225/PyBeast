#ifndef BEAST_POINTCLOUD_SCRIPT_H
#define BEAST_POINTCLOUD_SCRIPT_H

namespace boost { namespace python { class object; } }

#include <boost/python.hpp>
#include "scriptBase.h"

class BeastPointCloudInterface :
	public IScriptInterface
{
public:
	// IScriptInterface implementation
	void registerInterface(boost::python::object& nspace);
};
typedef boost::shared_ptr<BeastPointCloudInterface> BeastPointCloudInterfacePtr;

#endif // end of BEAST_POINTCLOUD_SCRIPT_H
