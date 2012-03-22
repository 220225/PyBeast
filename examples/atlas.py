#Beast API Sample: Atlas

#The purpose of this sample is to demonstrate how to:
#1. How to set up a baking with automatic texture packing
#2. How to find where each instance has been placed in the atlas
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

from xml.dom import minidom
import math
import ConfigParser
import os
import random

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
        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/atlas', ILB_CS_LOCAL, bmh) )
        
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
        sceneName = "AtlasScene"
        apiCall( ILBBeginScene(bmh, sceneName, scene) )

        floorInstance = createNewInstanceHandle()
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(scene, floorMesh, "FloorInstance", floorTrans, floorInstance))

        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight(scene, 
                                           "Light", 
                                           vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)),
                                           ColorRGB(1.0, 1.0, 0.8),
                                           light))
        apiCall( ILBSetCastShadows(light, True) )
        apiCall( ILBSetShadowSamples(light, 32) )
        apiCall( ILBSetShadowAngle(light, 0.1) )

        skylight = createNewLightHandle()
        apiCall( ILBCreateSkyLight( scene, 'SkyLight', vecmath.identity(), ColorRGB(1.0, 0.0, 0.0), skylight) )

        apiCall(ILBSetLightStats(skylight, ILB_LS_VISIBLE_FOR_EYE, ILB_LSOP_DISABLE))

        SPHERE_RADIUS = 1
        #SPHERES = 100
        SPHERES = 100
        spherePosRadius = 10.0 - 2.0*SPHERE_RADIUS

        sphereInstances = []

        for i in range(SPHERES):
            x = (random.random()-0.5) * spherePosRadius * 2.0
            z = (random.random()-0.5) * spherePosRadius * 2.0

            trans = vecmath.scaleTranslation(Vec3(SPHERE_RADIUS, SPHERE_RADIUS, SPHERE_RADIUS), Vec3(x, SPHERE_RADIUS-5.0, z))

            tempInstance = createNewInstanceHandle()
            sphereName = "SphereInstance_" + str(i)
            apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance))
            apiCall( ILBSetRenderStats(tempInstance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE))

            sphereInstances.append(tempInstance)

        # create the floor material
        floorMat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        primitives.apiCall( ILBSetMaterialColor(floorMat, ILB_CC_DIFFUSE, ColorRGBA(0.7, 0.7, 0.7, 1.0)) )

        # create sphere material
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
        beastConfig = beastCacheFolder + "/data/atlas.xml"

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

        GISettingsElement = xmlDoc.createElement("GISettings")
        xmlCreateElement(GISettingsElement, "enableGI", "true")
        xmlCreateElement(GISettingsElement, "fgRays", "1000")
        xmlCreateElement(GISettingsElement, "fgContrastThreshold", "0.1")
        xmlCreateElement(GISettingsElement, "fginterpolationPoints", "15")
        xmlCreateElement(GISettingsElement, "primaryIntegrator", "FinalGather")
        xmlCreateElement(GISettingsElement, "secondaryIntegrator", "None")
        docRoot.appendChild(GISettingsElement)


        # write file contents
        xmlFile = open(beastConfig, "w")
        xmlFile.write(xmlDoc.toprettyxml())
        xmlFile.close()


        job = createNewJobHandle()
        jobName = "TestJob"
        apiCall( ILBCreateJob( bmh, jobName, scene, beastConfig, job ) )


        fullShadingPass = createNewRenderPassHandle()
        apiCall( ILBCreateFullShadingPass(job, 'fullShading', fullShadingPass) )

        atlasTarget = createNewTargetHandle()
        atlasEntitys = []
        apiCall( ILBCreateAtlasedTextureTarget(job, "atlasTarget", 512, 512, 0, atlasTarget))

        for i in range(len(sphereInstances)):
            entity = createNewTargetEntityHandle()
            apiCall(ILBAddBakeInstance(atlasTarget, sphereInstances[i], entity))
            x = random.random()
            if x < 0.3:
                apiCall(ILBSetBakeResolution(entity, 128, 64))
            elif x < 0.6:
                apiCall(ILBSetBakeResolution(entity, 64, 128))
            else:
                apiCall(ILBSetBakeResolution(entity, 32, 32))

            atlasEntitys.append(entity)

        floorEntity = createNewTargetEntityHandle()
        apiCall(ILBAddBakeInstance(atlasTarget, floorInstance, floorEntity))
        apiCall(ILBSetBakeResolution(floorEntity, 128, 128))
        atlasEntitys.append(floorEntity)

                
        cameraTarget = createNewTargetHandle()
        apiCall( ILBCreateCameraTarget( job, 'cameraTarget', camera, 640, 480, cameraTarget ) )

        apiCall( ILBAddPassToTarget( atlasTarget, fullShadingPass ) )
        apiCall( ILBAddPassToTarget( cameraTarget, fullShadingPass ) )


        if not renderJob( job, False, False ):
            print "render error occured"

        for i in range(len(atlasEntitys)):
            print atlasEntitys[i]

        for i in range(len(atlasEntitys)):
            frameBufferIndex = ILBInt32(0)
            offset = scale = Vec2()
            ILBGetAtlasInformation(atlasEntitys[i], frameBufferIndex, offset, scale)
            print "Instance " + str(i) + ":Framebuffer " + str(frameBufferIndex.value) + \
                  " , offset( " + str(offset.x) + ", " + str(offset.y) + \
                  ", scale (" + str(scale.x) + ", " + str(scale.y)

        apiCall( ILBDestroyJob(job) )
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
