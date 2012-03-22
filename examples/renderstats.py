#Beast API Sample: Renderstats

#The purpose of this sample is to demonstrate how to use the API to:
#1. How to set renderstats on instances
#2. Illustrate the effect of different renderstats
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

from xml.dom import minidom
import math
import ConfigParser
import os

if __name__ == '__main__':
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
        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/renderStats', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        floorMatName = 'FloorMaterial'
        floorMesh = primitives.createPlaneSimple(bmh, 'Floor', floorMatName)
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 12, 12)
        
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

        sphereInstances = []
        for i in range(spheres):
            angle = (M_PI * 2.0 * i) / spheres
            x = math.cos(angle) * spherePosRadius
            z = math.sin(angle) * spherePosRadius

            trans = vecmath.scaleTranslation(Vec3(sphereRad, sphereRad, sphereRad), 
                                     Vec3(x, -3.0, z))
            tempInstance = createNewInstanceHandle()
            sphereName = 'SphereInstance_' + str(i)
            primitives.apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance) )

            sphereInstances.append( tempInstance )


        # create the floor material
        floorMat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        primitives.apiCall( ILBSetMaterialColor(floorMat, ILB_CC_DIFFUSE, ColorRGBA(0.8, 0.8, 0.8, 1.0)) )

        # create sphere material
        sphereMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.3, 0.3, 0.3, 1.0)) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 1.0, 1.0)) )
        apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_REFLECTION, 0.5) )
        apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_SHININESS, 15.0) )


        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight( scene, 'Sun', vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)), ColorRGB(1.0, 1.0, 0.8), light) )

        apiCall( ILBSetCastShadows(light, True) )
        apiCall( ILBSetShadowSamples(light, 32) )
        apiCall( ILBSetShadowAngle(light, 0.1) )

        skylight = createNewLightHandle()
        primitives.apiCall( ILBCreateSkyLight( scene, 'SkyLight', vecmath.identity(), ColorRGB(0.21, 0.21, 0.3), skylight) )

        camera = createNewCameraHandle()
        primitives.apiCall( ILBCreatePerspectiveCamera(scene, 
                                                       'Camera',
                                                       vecmath.setCameraMatrix(Vec3(0.3, 15.0, 0.0),  
                                                       Vec3(0.0, -1.0,  0.0), 
                                                       Vec3(0.0,  0.0, -1.0)),
                                                       camera) )


        # Setup renderstats for the spheres
        # Sphere 0 won't cast any shadows
        apiCall( ILBSetRenderStats(sphereInstances[0], ILB_RS_CAST_SHADOWS, ILB_RSOP_DISABLE) )
        
        # Sphere 1 won't be visible (but show up in reflections, cast shadows and gi)
        apiCall( ILBSetRenderStats(sphereInstances[1], ILB_RS_PRIMARY_VISIBILITY, ILB_RSOP_DISABLE) )

        # Sphere 2 won't be visible in reflections
        # Enables shadow bias in order to make the shadows on the low tesselated sphere look descent.
        apiCall( ILBSetRenderStats(sphereInstances[2], ILB_RS_VISIBLE_IN_REFLECTIONS, ILB_RSOP_DISABLE) )
        apiCall( ILBSetRenderStats(sphereInstances[2], ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE) )

        # Sphere 3 is invisible for GI purposes
        # To make it more obvious, disable primary visibility
        apiCall( ILBSetRenderStats(sphereInstances[3], ILB_RS_VISIBLE_IN_FINAL_GATHER, ILB_RSOP_DISABLE) )
        
        # Sphere 4 is single sided showing the inside
        apiCall( ILBSetRenderStats(sphereInstances[4], ILB_RS_DOUBLE_SIDED, ILB_RSOP_DISABLE) )
        apiCall( ILBSetRenderStats(sphereInstances[4], ILB_RS_OPPOSITE, ILB_RSOP_ENABLE) )

        # Create a material for sphere 2 to make it obvious that it's not
        # visible in reflection
        sphere2Mat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "Sphere2Mat", sphere2Mat) )
        apiCall( ILBSetMaterialColor(sphere2Mat, ILB_CC_DIFFUSE, ColorRGBA(1.0, 0.0, 0.0, 1.0)) )
        
        # Override material on sphere 2 
        apiCall( ILBSetMaterialOverrides(sphereInstances[2], sphere2Mat, 1) )

        # Finalize the scene
        apiCall( ILBEndScene(scene) )


        job = createNewJobHandle()
        beastConfig = beastCacheFolder + "/data/simpleFG.xml"
        apiCall( ILBCreateJob( bmh, 'TestJob', scene, beastConfig, job ) )

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

