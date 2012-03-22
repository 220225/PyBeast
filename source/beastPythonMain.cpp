#include <beastapi/beastmanager.h>

#include <boost/shared_ptr.hpp>
#include <boost/python.hpp>
#include <boost/python/call_method.hpp>
#include <boost/python/handle.hpp>

#include "beastmanagerScript.h"
#include "beastapitypesScript.h"
#include "beastsceneScript.h"
#include "beastinstanceScript.h"
#include "beastmaterialScript.h"
#include "beastpointcloudScript.h"
#include "beastlightsourceScript.h"
#include "beastcameraScript.h"
#include "beastJobScript.h"
#include "beastTargetScript.h"
#include "beastRenderPassScript.h"
#include "beastMeshScript.h"
#include "beastUtilScript.h"
#include "beasttextureScript.h"
#include "beasttargetentityScript.h"
#include "beastFramebufferScript.h"

#include "beastPrimitivesUtilScript.h"
#include "beastVecMathUtilScript.h"
#include "beastTextureUtilScript.h"
using namespace boost::python;
namespace bp = boost::python;

BOOST_PYTHON_MODULE(beastPython)
{
	boost::python::object defaultNamespace;

	BeastManagerInterfacePtr(new BeastManagerInterface)->registerInterface(defaultNamespace);
	BeastAPITypesInterfacePtr(new BeastAPITypesInterface)->registerInterface(defaultNamespace);
	BeastSceneInterfacePtr(new BeastSceneInterface)->registerInterface(defaultNamespace);
	BeastInstanceInterfacePtr(new BeastInstanceInterface)->registerInterface(defaultNamespace);
	BeastMaterialInterfacePtr(new BeastMaterialInterface)->registerInterface(defaultNamespace);
	BeastLightSourceInterfacePtr(new BeastLightSourceInterface)->registerInterface(defaultNamespace);
	BeastCameraInterfacePtr(new BeastCameraInterface)->registerInterface(defaultNamespace);
	BeastJobInterfacePtr(new BeastJobInterface)->registerInterface(defaultNamespace);
	BeastTargetInterfacePtr(new BeastTargetInterface)->registerInterface(defaultNamespace);
	BeastRenderPassInterfacePtr(new BeastRenderPassInterface)->registerInterface(defaultNamespace);
	BeastUtilInterfacePtr(new BeastUtilInterface)->registerInterface(defaultNamespace);
	BeastMeshInterfacePtr(new BeastMeshInterface)->registerInterface(defaultNamespace);
	BeastTextureInterfacePtr(new BeastTextureInterface)->registerInterface(defaultNamespace);
	BeastTargetEntityInterfacePtr(new BeastTargetEntityInterface)->registerInterface(defaultNamespace);
	BeastFrameBufferInterfacePtr(new BeastFrameBufferInterface)->registerInterface(defaultNamespace);
	BeastPointCloudInterfacePtr(new BeastPointCloudInterface)->registerInterface(defaultNamespace);

	BeastPrimitivesUtilInterfacePtr(new BeastPrimitivesUtilInterface)->registerInterface(defaultNamespace);
	BeastVecMathUtilInterfacePtr(new BeastVecMathUtilInterface)->registerInterface(defaultNamespace);
	BeastTextureUtilInterfacePtr(new BeastTextureUtilInterface)->registerInterface(defaultNamespace);
}
