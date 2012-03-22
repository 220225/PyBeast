#Beast API Sample: RNM

#The purpose of this sample is to demonstrate how to:
 #- Create an RNM pass and bake a texture with it.
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
        bmh = createNewManagerHandle()
        
        apiCall( ILBSetLogTarget(ILB_LT_ERROR, ILB_LS_STDERR, None) )
        
        apiCall( ILBSetLogTarget(ILB_LT_INFO, ILB_LS_DEBUG_OUTPUT, None) )
        
        # Setup our beast manager
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        configItems = {}
        for item in config.items('BeastPythonExamples'):
            configItems[item[0]] = item[1]

        # Setup our beast manager
        beastCacheFolder = os.path.normpath(configItems['beast_cache'])
        beastBinFolder = os.path.normpath(configItems['beast_bin'])
        beastDataFolder = os.path.normpath(configItems['beast_data'])
        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/rnm', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        # Create ball and a plane meshes
        sphereMatName = 'SphereMaterial'
        boxMatName = 'boxMaterial'
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 32, 32)
        cornellMesh = primitives.createCornellBox(bmh, "Cornell", boxMatName)
        
        # Create a scene
        scene = createNewSceneHandle()
        apiCall( ILBBeginScene(bmh, 'BakingScene', scene) )
        

        # create an instance of the Cornell Box
        cornellInstance = createNewInstanceHandle()
        cornellTrans = vecmath.scaleTranslation(Vec3(10.0, 10.0, 10.0), Vec3(0.0, 0.0, 0.0))

        apiCall( ILBCreateInstance(scene, cornellMesh, "CornellInstance", cornellTrans, cornellInstance))


        # create area light
        lh = createNewLightHandle()
        pos = Vec3(0.0, 9.0, 0.0)
        lookAt = Vec3(0.0, 0.0, 0.0)
        matrix = vecmath.setAreaLightMatrix(pos, 
                                            lookAt-pos,
                                            Vec3(1.0, 0.0, 0.0),
                                            Vec2(2.0, 2.0))
        apiCall( ILBCreateAreaLight(scene,
                                     "Light",
                                     matrix,
                                     ColorRGB(1.0, 1.0, 1.0),
                                     lh))

        apiCall( ILBSetCastShadows(lh, True) )
        apiCall( ILBSetShadowSamples(lh, 48) )

        spheres = 4
        sphereRad = 3.0
        spherePosRadius = 10.0 - 2.0*sphereRad

        for i in range(spheres):
            x = (random.random() - 0.5) * spherePosRadius * 2.0
            z = (random.random() - 0.5) * spherePosRadius * 2.0

            trans = vecmath.scaleTranslation(Vec3(sphereRad, sphereRad, sphereRad), 
                                     Vec3(x, sphereRad-10, z))
            tempInstance = createNewInstanceHandle()
            sphereName = 'SphereInstance_' + str(i)
            apiCall( ILBCreateInstance(scene, sphereMesh, sphereName, trans, tempInstance) )
            apiCall( ILBSetRenderStats(tempInstance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE) )


        # create the floor material
        boxMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, boxMatName, boxMat) )
        apiCall( ILBSetMaterialUseVertexColors(boxMat, ILB_CC_DIFFUSE) )

        # create sphere material
        sphereMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.9, 0.9, 0.9, 1.0)) )

        camera = createNewCameraHandle()
        camPos = Vec3(0.0, 0.0, -20.0)
        camLookAt = Vec3(0.0, -3.0, 0.0)
        primitives.apiCall( ILBCreatePerspectiveCamera(scene, 
                                                       'Camera',
                                                       vecmath.setCameraMatrix(camPos,
                                                       camLookAt - camPos,
                                                       Vec3(0.0,  1.0, 0.0)),
                                                       camera) )

        apiCall( ILBEndScene(scene) )


        # create config
        beastConfig = beastCacheFolder + "/data/rnm.xml"

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
        xmlCreateElement(GISettingsElement, "fgRays", "300")
        xmlCreateElement(GISettingsElement, "fgContrastThreshold", "0.1")
        xmlCreateElement(GISettingsElement, "fginterpolationPoints", "15")
        xmlCreateElement(GISettingsElement, "primaryIntegrator", "FinalGather")
        xmlCreateElement(GISettingsElement, "secondaryIntegrator", "PathTracer")
        docRoot.appendChild(GISettingsElement)

        # write file contents
        xmlFile = open(beastConfig, "w")
        xmlFile.write(xmlDoc.toprettyxml())
        xmlFile.close()


        job = createNewJobHandle()
        apiCall( ILBCreateJob( bmh, 'TestJob', scene, beastConfig, job ) )

        fullShadingPass = createNewRenderPassHandle()
        apiCall( ILBCreateFullShadingPass(job, 'fullShading', fullShadingPass) )

        rnmPass1 = createNewRenderPassHandle()
        apiCall( ILBCreateRNMPass(job, "RNM1", ILB_IM_INDIRECT_ONLY, 0, ILB_RB_UE3, rnmPass1) )
        rnmPass2 = createNewRenderPassHandle()
        apiCall( ILBCreateRNMPass(job, "RNM2", ILB_IM_DIRECT_ONLY, 0, ILB_RB_UE3, rnmPass2) )
        rnmPass3 = createNewRenderPassHandle()
        apiCall( ILBCreateRNMPass(job, "RNM3", ILB_IM_FULL, 0, ILB_RB_UE3, rnmPass3) )
        
        textureTarget = createNewTargetHandle()
        apiCall( ILBCreateTextureTarget(job, "textureTarget", 256, 256, textureTarget) )
        entity = createNewTargetEntityHandle()
        apiCall( ILBAddBakeInstance(textureTarget, cornellInstance, entity) )

        cameraTarget = createNewTargetHandle()
        apiCall( ILBCreateCameraTarget( job, 'cameraTarget', camera, 640, 480, cameraTarget ) )

        apiCall( ILBAddPassToTarget(cameraTarget, fullShadingPass) )
        apiCall( ILBAddPassToTarget(textureTarget, rnmPass3) )
        apiCall( ILBAddPassToTarget(textureTarget, rnmPass2) )
        apiCall( ILBAddPassToTarget(textureTarget, rnmPass1) )

        st = createNewJobStatus()
        apiCall( ILBExecuteBeast(bmh, job, ILB_SR_KEEP_OPEN, ILB_RD_FORCE_LOCAL, st) )

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

