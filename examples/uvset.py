#Beast API Sample: UVSet

#The purpose of this sample is to demonstrate how to use the API to:
#1. Create a mesh with several UV sets
#2. Create a material which uses different uv sets for different channels
#3. Show the different channels in a render with the help of a spot light
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
        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/uvset', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        floorMatName = 'FloorMaterial'
        floorMesh = primitives.createPlaneMultiUV(bmh, 'Floor', floorMatName)
        
        # Create a scene
        scene = createNewSceneHandle()
        apiCall( ILBBeginScene(bmh, 'UvsetScene', scene) )
        
        # Create an instance of the plane that will be a floor
        floorInstance = createNewInstanceHandle()
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), 
                                              Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(scene, floorMesh, 'FloorInstance', floorTrans, floorInstance) )

        # create texture with 4 colors
        floorTex = textures.createTestColorTexutre(bmh, "TestColorTexture") 

        floorMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        apiCall( ILBSetMaterialTexture(floorMat, ILB_CC_DIFFUSE, floorTex) )
        apiCall( ILBSetChannelUVLayer(floorMat, ILB_CC_DIFFUSE, "uv3") )
        apiCall( ILBSetMaterialTexture(floorMat, ILB_CC_EMISSIVE, floorTex) )
        apiCall( ILBSetChannelUVLayer(floorMat, ILB_CC_EMISSIVE, "uv4") )

        light = createNewLightHandle()
        pos = Vec3(0.0, 1.0, 0.0)
        lookAt = Vec3(0.0, 0.0, 0.0)

        spotMatrix = vecmath.setSpotlightMatrix(pos, lookAt - pos )

        apiCall( ILBCreateSpotLight(scene, "Light", spotMatrix, ColorRGB(1.0, 1.0, 1.0), light) )
        apiCall( ILBSetSpotlightCone(light, M_PI/3.0, 0.1, 2.0) )


        camera = createNewCameraHandle()
        apiCall( ILBCreatePerspectiveCamera(scene, 
                                            'Camera',
                                            vecmath.setCameraMatrix(Vec3(0.3, 3.0, 20.0),  
                                            Vec3(0.1, -0.3, -1.0), 
                                            Vec3(0.0,  1.0,  0.0)), 
                                            camera) )

        apiCall( ILBSetFov(camera, M_PI/4.0, 1.0) )

        apiCall( ILBEndScene(scene) )

        beastConfig = beastCacheFolder + "/data/uvset.xml"

        dom = minidom.getDOMImplementation()
        xmlDoc = dom.createDocument(None, "ILConfig", None)
        docRoot = xmlDoc.documentElement

        AASettingsElement = xmlDoc.createElement("AASettings")

        minSampleRateElement = xmlDoc.createElement("minSampleRate")
        minSampleRateElement.appendChild(xmlDoc.createTextNode(str(-1)))
        AASettingsElement.appendChild(minSampleRateElement)

        maxSampleRateElement = xmlDoc.createElement("maxSampleRate")
        maxSampleRateElement.appendChild(xmlDoc.createTextNode(str(1)))
        AASettingsElement.appendChild(maxSampleRateElement)

        docRoot.appendChild(AASettingsElement)

        # write file contents
        xmlFile = open(beastConfig, "w")
        xmlFile.write(xmlDoc.toprettyxml())
        xmlFile.close()

        job = createNewJobHandle()
        apiCall( ILBCreateJob( bmh, 'UVSetJob', scene, beastConfig, job ) )

        fullShadingPass = createNewRenderPassHandle()
        apiCall( ILBCreateFullShadingPass(job, 'fullShading', fullShadingPass) )

        cameraTarget = createNewTargetHandle()
        apiCall( ILBCreateCameraTarget( job, 'cameraTarget', camera, 512, 512, cameraTarget ) )

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
