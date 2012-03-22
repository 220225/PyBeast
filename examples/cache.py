#Beast API Sample: Cache

#The purpose of this sample is to demonstrate how to use the API to:
#1. Create a global cache
#2. Create a resource in the cache
#3. Reuse the resource in subsequent renderings.
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

from xml.dom import minidom
import math
import random
import getopt
import ConfigParser
import os

RM_CLEAR, RM_GLOBAL, RM_LOCAL = range(3)

def xmlCreateElement(_parentElm, _newElem, _newElemValue):
    newElement = xmlDoc.createElement(_newElem)
    newElement.appendChild(xmlDoc.createTextNode(_newElemValue))
    _parentElm.appendChild(newElement)
    
    return newElement

def getRunMode(_rm):
    """docstring for getRunMode"""
    if _rm == "clear":
        return RM_CLEAR
    elif _rm == "global":
        return RM_GLOBAL
    elif _rm == "local":
        return RM_LOCAL

    raise Exception, "Invalid runmode"

def main(argv):
    """docstring for main"""
    optlist, args = getopt.getopt(argv, "", ['runningmode='])

    runningmode = "global"
    for o, a in optlist:
        if o == "--runningmode":
            runningmode = a

    runmode = getRunMode(runningmode)
    print runmode

    try:
        M_PI = 3.14159265358979323846

        bmh = createNewManagerHandle()
        
        apiCall( ILBSetLogTarget(ILB_LT_ERROR, ILB_LS_STDERR, None) )
        
        apiCall( ILBSetLogTarget(ILB_LT_INFO, ILB_LS_DEBUG_OUTPUT, None) )
        
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        configItems = {}
        for item in config.items('BeastPythonExamples'):
            configItems[item[0]] = item[1]

        # Setup our beast manager
        beastCacheFolder = os.path.normpath(configItems['beast_cache'])
        beastBinFolder = os.path.normpath(configItems['beast_bin'])
        beastDataFolder = os.path.normpath(configItems['beast_data'])


        dir = beastCacheFolder + r'/temp/cache'

        if runmode == RM_CLEAR:
            print "Clearing cache..."
            apiCall( ILBCreateManager(dir, ILB_CS_GLOBAL, bmh) )
            apiCall( ILBClearCache(bmh) )
            print "Done!"
        elif runmode == RM_GLOBAL:
            print "Creating a global cache!"
            apiCall( ILBCreateManager(dir, ILB_CS_GLOBAL, bmh) )
        elif runmode == RM_LOCAL:
            print "createing a local cache!"
            apiCall( ILBCreateManager(dir, ILB_CS_LOCAL, bmh) )
        else:
            print "Invalid runmode"
        
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        sphereName = "Sphere"
        floorName = "Floor"
        sphereMatName = "SphereMaterial"
        floorMatName = "FloorMaterial"

        sphereMesh = createNewMeshHandle()
        if not findCachedMesh(bmh, sphereName, sphereMesh):
           sphereMesh = primitives.createSphere(bmh, sphereName, sphereMatName, 600, 400, None) 

        floorMesh = createNewMeshHandle()
        if not findCachedMesh(bmh, floorName, floorMesh):
           floorMesh = primitives.createPlaneSimple(bmh, floorName, floorMatName) 

        texName = "Mandelbrot"
        texture = createNewTextureHandle()
        if not findCachedTexture(bmh, texName, texture):
            texture = textures.createMandelbrotTexture(bmh, texName, ColorRGB(1.0, 0.7, 0.7), 1000, 1000)


        scene = createNewSceneHandle()
        sceneName = "SimpleScene"
        apiCall( ILBBeginScene(bmh, sceneName, scene) )

        floorInstance = createNewInstanceHandle()
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(scene, floorMesh, "FloorInstance", floorTrans, floorInstance))


        SPHERES = 5
        spherePosRadius = 5.0
        sphereRad = 2.0
        sphereInstances = []

        for i in range(SPHERES):
            angle = (M_PI * 2.0 * i) / SPHERES
            x = math.cos(angle) * spherePosRadius
            z = math.sin(angle) * spherePosRadius

            trans = vecmath.scaleTranslation(Vec3(sphereRad, sphereRad, sphereRad), 
                                     Vec3(x, -3.0, z))
            tempInstance = createNewInstanceHandle()
            sphereName = 'SphereInstance_' + str(i)
            apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance) )


        # create the floor material
        floorMat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        primitives.apiCall( ILBSetMaterialTexture(floorMat, ILB_CC_DIFFUSE, texture) )

        # create sphere material
        sphereMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.3, 0.3, 0.3, 1.0)) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 1.0, 1.0)) )
        apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_REFLECTION, 0.1) )
        apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_SHININESS, 15.0) )

        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight(scene, 
                                           "Sun", 
                                           vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)),
                                           ColorRGB(1.0, 1.0, 0.8),
                                           light))
        apiCall( ILBSetCastShadows(light, True) )
        apiCall( ILBSetShadowSamples(light, 32) )
        apiCall( ILBSetShadowAngle(light, 0.1) )


        skylight = createNewLightHandle()
        apiCall( ILBCreateSkyLight( scene, 'SkyLight', vecmath.identity(), ColorRGB(0.21, 0.21, 0.3), skylight) )


        camera = createNewCameraHandle()
        apiCall( ILBCreatePerspectiveCamera(scene, 
                 "Camera", 
                 vecmath.setCameraMatrix(Vec3(0.3, 0.5, 15.0), Vec3(0.1, -0.3, -1.0), Vec3(0.0, 1.0, 0.0)),
                 camera) )

        # Finalize the scene
        apiCall(ILBEndScene(scene));

        job = createNewJobHandle()
        apiCall( ILBCreateJob( bmh, 'TestJob', scene, beastDataFolder + r'/data/simpleFG.xml', job ) )

        fullShadingPass = createNewRenderPassHandle()
        apiCall( ILBCreateFullShadingPass(job, 'fullShading', fullShadingPass) )

        cameraTarget = createNewTargetHandle()
        apiCall( ILBCreateCameraTarget( job, 'cameraTarget', camera, 640, 480, cameraTarget ) )

        apiCall( ILBAddPassToTarget( cameraTarget, fullShadingPass ) )

        if not renderJob( job ):
            print "render error occured"

    except BeastPythonException, (instance):
        print "exception: " + str(instance.parameter)
        ex = instance.parameter
        errorString = createNewStringHandle()
        extendedError = createNewStringHandle()
        ILBErrorToString(ex, errorString)
        ILBGetExtendErrorInformation(extendedError)
        print "Beast API error"
        print "Error: " + convertStringHandle(errorString)
        print "Info: " + convertStringHandle(extendedError)

    except Exception, err:
        import traceback
        print "Caught an exception: " + str(err)
        print "===== Traceback ====="
        print ""
        traceback.print_exc()
        print ""
        print "===== End of Traceback ====="

        
if __name__ == '__main__':
    main(sys.argv[1:])

