#Beast API Sample: Materials

#The purpose of this sample is to demonstrate how to use the API to:
#1. Create the different kinds of materials available
#2. Render a test scene which shows them in action
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

        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/materials', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        floorMatName = 'FloorMaterial'
        floorMesh = primitives.createPlaneSimple(bmh, 'Floor', floorMatName)
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 30, 15)
        
        # Create a scene
        scene = createNewSceneHandle()
        apiCall( ILBBeginScene(bmh, 'SimpleScene', scene) )
        
        # Create an instance of the plane that will be a floor
        floorInstance = createNewInstanceHandle()
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), 
                                              Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(scene, floorMesh, 'FloorInstance', floorTrans, floorInstance) )


        # Create 5 instances of the sphere on the plane
        sphereSideCount = 3
        sphereRad = 2.0
        sphereDist = 5.0
        sphereInstances = []

        for gy in range(sphereSideCount):
            for gx in range(sphereSideCount):
                offset = ((sphereSideCount-1)* sphereDist) / 2.0
                x = gx * sphereDist - offset
                z = gy * sphereDist - offset

                trans = vecmath.scaleTranslation(Vec3(sphereRad, sphereRad, sphereRad), Vec3(x, -3.0, z))
                tempInstance = createNewInstanceHandle()
                sphereName = 'SphereInstance_' + str(gx) + "_" + str(gy)
                primitives.apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance) )

                sphereInstances.append(tempInstance)

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

        # set up camera
        camPos = Vec3(10.0, 20.0, 10.0)
        lookAt = Vec3(0.0, -3.0, 0.0)
        camera = createNewCameraHandle()
        primitives.apiCall( ILBCreatePerspectiveCamera(scene, 
                                                       'Camera',
                                                       vecmath.setCameraMatrix(camPos,  
                                                                       vecmath.normalize(lookAt - camPos),
                                                                       Vec3(0.0,  0.0, -1.0)),
                                                       camera) )

        apiCall( ILBSetFov(camera, M_PI/4.0, 1.0) )


        # Create a textured diffuse material for sphere 0
        sm0 = createNewMaterialHandle()
        tex = textures.createXorTexture( bmh, "Tex1", ColorRGB(0.6, 0.6, 0.3) ) 
        apiCall( ILBCreateMaterial(scene, "Textured", sm0) )

        apiCall( ILBSetMaterialTexture(sm0, ILB_CC_DIFFUSE, tex) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[0], sm0, 1) )


        # Create a textured specular material for sphere 1
        sm1 = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "TexturedSpec", sm1) )
        apiCall( ILBSetMaterialTexture(sm1, ILB_CC_DIFFUSE, tex) )
        apiCall( ILBSetMaterialColor(sm1, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 0.7, 1.0)) )
        apiCall( ILBSetMaterialScale(sm1, ILB_CC_SHININESS, 25.0) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[1], sm1, 1) )


        # Create a semi transparent material for sphere 2
        sm2 = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "Transp", sm2) )
        col2 = ColorRGBA(0.6, 0.9, 0.9, 1.0)
        apiCall( ILBSetMaterialColor(sm2, ILB_CC_DIFFUSE, col2) )
        apiCall( ILBSetMaterialColor(sm2, ILB_CC_TRANSPARENCY, col2) )
        apiCall( ILBSetMaterialOverrides( sphereInstances[2], sm2, 1) )

        # Create a color textured transparent material for sphere 3
        sm3 = createNewMaterialHandle()
        tex2 = textures.createXorTexture(bmh, "Tex2", ColorRGB(1.0, 0.2, 0.2) )
        apiCall( ILBCreateMaterial(scene, "TranspTex", sm3) )
        apiCall( ILBSetMaterialTexture(sm3, ILB_CC_DIFFUSE, tex2) )
        apiCall( ILBSetMaterialTexture(sm3, ILB_CC_TRANSPARENCY, tex2) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[3], sm3, 1) )

        # Create an emissive material for sphere 4
        sm4 = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "Emissive", sm4) )
        apiCall( ILBSetMaterialColor(sm4, ILB_CC_DIFFUSE, ColorRGBA(0.1, 0.1, 0.1, 1.0)) )
        apiCall( ILBSetMaterialColor(sm4, ILB_CC_EMISSIVE, ColorRGBA(1.0, 0.6, 0.3, 1.0)) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[4], sm4, 1) )

        # Create a vertex colored material for sphere 5
        sm5 = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "VertexColor", sm5) )
        apiCall( ILBSetMaterialUseVertexColors(sm5, ILB_CC_DIFFUSE) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[5], sm5, 1) )

        # Create non reflective material with textured specular on sphere 6
        sm6 = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "SpecNoReflectivity", sm6) )
        apiCall( ILBSetMaterialTexture(sm6, ILB_CC_SPECULAR, tex2) )
        apiCall( ILBSetMaterialScale(sm6, ILB_CC_SPECULAR, 2.0) )
        apiCall( ILBSetMaterialScale(sm6, ILB_CC_SHININESS, 4.0) )
        apiCall( ILBSetMaterialColor(sm6, ILB_CC_DIFFUSE, ColorRGBA(0.3, 0.3, 0.3, 1.0)) )
        apiCall( ILBSetMaterialScale(sm6, ILB_CC_REFLECTION, 0.0) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[6], sm6, 1) )

        # Create a textured diffuse material for sphere 0
        sm7 = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, "TexturedCheckerAlpha", sm7) )
        apiCall( ILBSetMaterialColor(sm7, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 0.7, 1.0)) )
        apiCall( ILBSetMaterialTexture(sm7, ILB_CC_DIFFUSE, tex) )
        apiCall( ILBSetMaterialScale(sm7, ILB_CC_SHININESS, 25.0) )
        apiCall( ILBSetAlphaAsTransparency(sm7, True) )
        apiCall( ILBSetMaterialScale(sm7, ILB_CC_REFLECTION, 0.0) )
        apiCall( ILBSetMaterialOverrides(sphereInstances[7], sm7, 1) )



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

