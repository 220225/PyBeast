#Beast API Sample: Lightsources

#The purpose of this sample is to demonstrate how to use the API to:
#1. Create the different types of light sources available
#2. Render a demonstration scene for each one of them
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

from xml.dom import minidom
import math
import ConfigParser
import os

def generateLight(_lsType, _scene, _goboTex):
    """docstring for generateLight"""
    lh = createNewLightHandle()
    lookAt = Vec3(0.0, -2.0, 0.0)
    if _lsType == 0:
        apiCall( ILBCreateDirectionalLight(_scene, 
                                           "Light", 
                                           vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)),
                                           ColorRGB(1.0, 1.0, 0.8),
                                           lh))
        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )
        apiCall( ILBSetShadowAngle(lh, 0.1) )

    elif _lsType == 1:
        # point light
        apiCall( ILBCreatePointLight(_scene,
                                     "Light",
                                     vecmath.translation(Vec3(-1.0, 1.0, 1.0)),
                                     ColorRGB(3.0, 3.0, 2.0),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )
        apiCall( ILBSetShadowRadius(lh, 1.0) )

        # set a quadratic falloff
        apiCall( ILBSetFalloff(lh, ILB_FO_EXPONENT, 2.0, 20.0, True))
    elif _lsType == 2:
        # spot light
        pos = Vec3(-1.0, 1.0, 1.0)
        spotMatrix = vecmath.setSpotlightMatrix(pos, lookAt-pos)
        apiCall( ILBCreateSpotLight(_scene,
                                     "Light",
                                     spotMatrix,
                                     ColorRGB(3.0, 3.0, 2.0),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )
        apiCall( ILBSetShadowRadius(lh, 1.0) )

        coneAngle = M_PI/3.0
        apiCall(ILBSetSpotlightCone(lh, coneAngle, 0.1, 2.0))

    elif _lsType == 3:
        # window light
        pos = Vec3(-1.0, 1.0, 1.0)
        matrix = vecmath.setAreaLightMatrix(pos, 
                                            lookAt-pos,
                                            Vec3(0.0, 1.0, 0.0),
                                            Vec2(2.0, 5.0))
        apiCall( ILBCreateWindowLight(_scene,
                                     "Light",
                                     matrix,
                                     ColorRGB(3.0, 3.0, 2.0),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )
        apiCall( ILBSetShadowAngle(lh, 0.1) )

    elif _lsType == 4:
        #area light
        pos = Vec3(-1.0, 1.0, 1.0)
        matrix = vecmath.setAreaLightMatrix(pos, 
                                            lookAt-pos,
                                            Vec3(0.0, 1.0, 0.0),
                                            Vec2(3.0, 1.0))
        apiCall( ILBCreateAreaLight(_scene,
                                     "Light",
                                     matrix,
                                     ColorRGB(0.4, 0.4, 0.3),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )

    elif _lsType == 5:
        # Point light wit ramp
        transform = vecmath.scaleTranslation(Vec3(17.0, 17.0, 17.0), Vec3(-1.0, 1.0, 1.0))
        apiCall( ILBCreatePointLight(_scene,
                                     "Light",
                                     transform,
                                     ColorRGB(1.0, 1.0, 1.0),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )
        apiCall( ILBSetShadowRadius(lh, 1.0) )
        apiCall( ILBSetFalloff(lh, ILB_FO_EXPONENT, 0.0, 20.0, True) )

        # set some random colors in a ramp
        rampColors = 10
        for i in range(rampColors):
            randCol = vecmath.randomRGBA(3.0)
            apiCall( ILBSetLightRampEntry(lh, i/(rampColors-1.0), randCol.toColorRGB()))

    elif _lsType == 6:
        # spot light
        pos = Vec3(-1.0, 1.0, 1.0)
        spotMatrix = vecmath.setSpotlightMatrix(pos, lookAt - pos)
        apiCall( ILBCreateSpotLight(_scene,
                                     "Light",
                                     spotMatrix,
                                     ColorRGB(3.0, 3.0, 2.0),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 32) )
        apiCall( ILBSetShadowRadius(lh, 1.0) )
        apiCall( ILBSetLightProjectedTexture(lh, goboTex) )

        coneAngle = M_PI/3.0
        apiCall( ILBSetSpotlightCone(lh, coneAngle, 0.1, 2.0) )

    return lh


if __name__ == '__main__':
    try:
        M_PI = 3.14159265358979323846

        bmh = createNewManagerHandle()
        
        apiCall( ILBSetLogTarget(ILB_LT_ERROR, ILB_LS_STDERR, None) )
        
        apiCall( ILBSetLogTarget(ILB_LT_INFO, ILB_LS_STDOUT, None) )
        
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        configItems = {}
        for item in config.items('BeastPythonExamples'):
            configItems[item[0]] = item[1]

        # Setup our beast manager
        beastCacheFolder = os.path.normpath(configItems['beast_cache'])
        beastBinFolder = os.path.normpath(configItems['beast_bin'])
        beastDataFolder = os.path.normpath(configItems['beast_data'])
        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/lightsources', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        floorMatName = 'FloorMaterial'
        floorMesh = primitives.createPlaneSimple(bmh, 'Floor', floorMatName)
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 30, 15)
        

        goboTex = textures.createXorTexture(bmh, "xorTex", ColorRGB(1.0, 1.0, 1.0))
        
        lsTypes = 7
        scenes = []
        cameras = []

        for lightType in range(lsTypes):
            scene = createNewSceneHandle()
            sceneName = "SceneInstance_" + str(lightType)
            apiCall( ILBBeginScene(bmh, sceneName, scene) )

            skylight = createNewLightHandle()
            primitives.apiCall( ILBCreateSkyLight( scene, 'SkyLight', vecmath.identity(), ColorRGB(0.21, 0.21, 0.3), skylight) )

            # Create an instance of the plane that will be a floor
            floorInstance = createNewInstanceHandle()
            floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), 
                                          Vec3(0.0, -5.0, 0.0))
            apiCall( ILBCreateInstance(scene, floorMesh, 'FloorInstance', floorTrans, floorInstance) )
            x = 0.0
            z = 0.0
            sphereRad = 2.0

            trans = vecmath.scaleTranslation(Vec3(sphereRad, sphereRad, sphereRad), Vec3(x, -3.0, z))
            tempInstance = createNewInstanceHandle()
            sphereName = 'SphereInstance_' + str(lightType)
            primitives.apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance) )
            apiCall( ILBSetRenderStats(tempInstance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE) )

            # create the floor material
            floorMat = createNewMaterialHandle()
            primitives.apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
            primitives.apiCall( ILBSetMaterialColor(floorMat, ILB_CC_DIFFUSE, ColorRGBA(0.7, 0.7, 0.7, 1.0)) )

            sphereMat = createNewMaterialHandle()
            apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
            apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.3, 0.3, 0.3, 1.0)) )
            apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 1.0, 1.0)) )
            apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_REFLECTION, 0.1) )
            apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_SHININESS, 15.0) )

            # create direction light
            light = generateLight(lightType, scene, goboTex)
            camPos = Vec3(3.0, 3.0, 20.0)
            lookAt = Vec3(0.0, -2.0, 0.0)
            camera = createNewCameraHandle()

            apiCall( ILBCreatePerspectiveCamera(scene, 
                     "Camera", 
                     vecmath.setCameraMatrix(camPos, 
                                             lookAt - camPos, 
                                             Vec3(0.0, 1.0, 0.0)), 
                     camera) )

            # Set a 45 degrees fov
            apiCall( ILBSetFov(camera, (M_PI)/4.0, 1.0) );
            # Finalize the scene
            apiCall(ILBEndScene(scene));

            scenes.append(scene)
            cameras.append(camera)


        for curLightType in range(len(scenes)):
            job = createNewJobHandle()
            beastConfig = beastCacheFolder + "/data/simpleFG.xml"
            jobName = "TestJob_" + str(curLightType)
            apiCall( ILBCreateJob( bmh, jobName, scenes[curLightType], beastConfig, job ) )

            fullShadingPass = createNewRenderPassHandle()
            apiCall( ILBCreateFullShadingPass(job, 'fullShading', fullShadingPass) )

            cameraTarget = createNewTargetHandle()
            apiCall( ILBCreateCameraTarget( job, 'cameraTarget', cameras[curLightType], 640, 480, cameraTarget ) )

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

