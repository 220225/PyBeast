#Beast API Sample: Simple

#The purpose of this sample is to demonstrate how to use the API to:
#1. Create a simple scene with meshes, textures, lights, materials and a camera
#2. Render it 
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

import math
import ConfigParser
import os

if __name__ == '__main__':

    try:
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
        apiCall( ILBCreateManager( os.path.join(beastCacheFolder, r'temp/simpleCache'), ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        floorMatName = 'FloorMaterial'
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 30, 15, None)
        floorMesh = primitives.createPlaneSimple(bmh, 'Floor', floorMatName)

        
        # Create a scene
        scene = createNewSceneHandle()
        apiCall( ILBBeginScene(bmh, 'SimpleScene', scene) )
        
        # Create an instance of the plane that will be a floor
        floorInstance = createNewInstanceHandle()
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), 
                                              Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(scene, floorMesh, 'FloorInstance', floorTrans, floorInstance) )

        # Create 5 instances of the sphere on the plane
        spheres = 5
        sphereRad = 2.0
        spherePosRadius = 5.0
        M_PI = 3.14159265358979323846
        for i in range(spheres):
            angle = (M_PI * 2.0 * i) / spheres
            x = math.cos(angle) * spherePosRadius
            z = math.sin(angle) * spherePosRadius

            trans = vecmath.scaleTranslation(Vec3(sphereRad, sphereRad, sphereRad), 
                                             Vec3(x, -3.0, z))
            tempInstance = createNewInstanceHandle()
            sphereName = 'SphereInstance_' + str(i)
            apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance) )

        # Create a texture for the floor
        floorTex = textures.createXorTexture(bmh, 'xorTexture', ColorRGB(0.9, 0.7, 0.7))

        floorMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        apiCall( ILBSetMaterialTexture(floorMat, ILB_CC_DIFFUSE, floorTex) )

        sphereMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.3, 0.3, 0.3, 1.0)) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 1.0, 1.0)) )
        apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_REFLECTION, 0.1) )
        apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_SHININESS, 15.0) )


        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight( scene, 'Sun', vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)), ColorRGB(1.0, 1.0, 0.8), light) )

        apiCall( ILBSetCastShadows(light, True) )
        apiCall( ILBSetShadowSamples(light, 32) )
        apiCall( ILBSetShadowAngle(light, 0.1) )

        skylight = createNewLightHandle()
        apiCall( ILBCreateSkyLight( scene, 'SkyLight', vecmath.identity(), ColorRGB(0.21, 0.21, 0.3), skylight) )

        camera = createNewCameraHandle()
        apiCall( ILBCreatePerspectiveCamera(scene, 
                                                    'Camera',
                                                    vecmath.setCameraMatrix(Vec3(0.3, 3.0, 20.0),  
                                                                            Vec3(0.1, -0.3, -1.0), 
                                                                            Vec3(0.0,  1.0,  0.0)), 
                                                    camera) )

        apiCall( ILBSetFov(camera, M_PI/4.0, 1.0) )

        apiCall( ILBEndScene(scene) )

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
