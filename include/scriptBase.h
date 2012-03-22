#ifndef SCRIPT_BASE_H_
#define SCRIPT_BASE_H_

namespace boost { namespace python { class object; } }

class IScriptInterface
{
public:
    virtual ~IScriptInterface() {}
	virtual void registerInterface(boost::python::object& nspace) = 0;
};
typedef boost::shared_ptr<IScriptInterface> IScriptInterfacePtr;

#endif // end of SCRIPT_BASE_H_
