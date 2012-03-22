#Beast API Sample: Occlusion

#The purpose of this sample is to demonstrate how to use the API to:
 #- How to set up and bake ambient occlusion to a texture
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

from xml.dom import minidom
import math
import random
import ConfigParser
import os

def xmlCreateElement(_parentElm, _newElem, _newElemValue):
    newElement = xmlDoc.createElement(_newElem)
    newElement.appendChild(xmlDoc.createTextNode(_newElemValue))
    _parentElm.appendChild(newElement)
    
    return newElement

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

        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/occlusion', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        floorMatName = 'FloorMaterial'
        #floorMesh = primitives.createPlane(bmh, 'Floor', floorMatName, 5, 5)
        floorMesh = primitives.createPlaneSimple(bmh, 'Floor', floorMatName)
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 30, 15)
        
        scene = createNewSceneHandle()
        sceneName = "OcclusionScene"
        apiCall( ILBBeginScene(bmh, sceneName, scene) )

        floorInstance = createNewInstanceHandle()
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(scene, floorMesh, "FloorInstance2", floorTrans, floorInstance))

        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight(scene, 
                                           "Light", 
                                           vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)),
                                           ColorRGB(1.0, 1.0, 0.8),
                                           light))
        apiCall( ILBSetCastShadows(light, True) )
        apiCall( ILBSetShadowSamples(light, 32) )
        apiCall( ILBSetShadowAngle(light, 0.1) )

        SPHERE_RADIUS = 1
        SPHERES = 50


        spherePosRadius = 10.0 - 2.0*SPHERE_RADIUS
        for i in range(SPHERES):
            x = (random.random()-0.5) * spherePosRadius * 2.0
            z = (random.random()-0.5) * spherePosRadius * 2.0
            print 'x = ' + str(x) + ', z = ' + str(z)

            trans = vecmath.scaleTranslation(Vec3(SPHERE_RADIUS, SPHERE_RADIUS, SPHERE_RADIUS), Vec3(x, SPHERE_RADIUS-5.0, z))

            tempInstance = createNewInstanceHandle()
            sphereName = "SphereInstance_" + str(i)
            apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance))
            apiCall( ILBSetRenderStats(tempInstance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE))


        # create the floor material
        floorMat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        primitives.apiCall( ILBSetMaterialColor(floorMat, ILB_CC_DIFFUSE, ColorRGBA(0.7, 0.7, 0.7, 1.0)) )

        sphereMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.9, 0.9, 0.9, 1.0)) )


        camera = createNewCameraHandle()
        apiCall( ILBCreatePerspectiveCamera(scene, 
                 "Camera", 
                 vecmath.translation(Vec3(0.0, 0.0, 10.0)),
                 camera) )

        # Finalize the scene
        apiCall(ILBEndScene(scene));


        # create config
        beastConfig = beastCacheFolder + "/data/occlusion.xml"

        dom = minidom.getDOMImplementation()
        xmlDoc = dom.createDocument(None, "ILConfig", None)
        docRoot = xmlDoc.documentElement

        AASettingsElement = xmlDoc.createElement("AASettings")
        xmlCreateElement(AASettingsElement, "minSampleRate", "0")
        xmlCreateElement(AASettingsElement, "maxSampleRate", "2")
        docRoot.appendChild(AASettingsElement)


        RenderSettingsElement = xmlDoc.createElement("RenderSettings")
        xmlCreateElement(RenderSettingsElement, "bias", "0.00001")
        docRoot.appendChild(RenderSettingsElement)

        FrameSettingsElement = xmlDoc.createElement("FrameSettings")
        xmlCreateElement(FrameSettingsElement, "inputGamma", "0.45")
        outputCorrectionElement = xmlDoc.createElement("outputCorrection")
        xmlCreateElement(outputCorrectionElement, "colorCorrection", "Gamma")
        xmlCreateElement(outputCorrectionElement, "gamma", "2.2")
        FrameSettingsElement.appendChild(outputCorrectionElement)

        docRoot.appendChild(FrameSettingsElement)


        # write file contents
        xmlFile = open(beastConfig, "w")
        xmlFile.write(xmlDoc.toprettyxml())
        xmlFile.close()


        job = createNewJobHandle()
        jobName = "TestJob"
        apiCall( ILBCreateJob( bmh, jobName, scene, beastConfig, job ) )

        # create occlusion pass
        occlusionPass = createNewRenderPassHandle()
        apiCall( ILBCreateAmbientOcclusionPass(job, "occlusion", 0, 180, occlusionPass) )
        apiCall( ILBSetAOAdaptive(occlusionPass, 1, 1) )
        apiCall( ILBSetAONumRays(occlusionPass, 256, 1024) )
        apiCall( ILBSetAOContrast(occlusionPass, 1.1, 1.0) )
        apiCall( ILBSetAOUniformSampling(occlusionPass) )
        apiCall( ILBSetAOSelfOcclusion(occlusionPass, ILB_SO_SET_ENVIRONMENT) )

        textureTarget = createNewTargetHandle()
        apiCall( ILBCreateTextureTarget(job, "textureTarget", 512, 512, textureTarget))

        entity = createNewTargetEntityHandle()
        apiCall( ILBAddBakeInstance(textureTarget, floorInstance, entity))

        apiCall( ILBAddPassToTarget( textureTarget, occlusionPass ) )

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

