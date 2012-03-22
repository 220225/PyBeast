#Beast API Sample: Baking

#The purpose of this sample is to demonstrate how to:
#1. Create a simple XML file for GI and baking
#2. Setup a scene suitable for baking
#3. Run a texture baking job
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

def xmlCreateElement(_xmlDoc, _parentElm, _newElem, _newElemValue):
    newElement = _xmlDoc.createElement(_newElem)
    newElement.appendChild(_xmlDoc.createTextNode(_newElemValue))
    _parentElm.appendChild(newElement)
    
    return newElement

def main(argv):
    """docstring for main"""
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

        dir = beastCacheFolder + r'/temp/baking'
        apiCall( ILBCreateManager(dir, ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )

        sphereName = "Sphere"
        floorName = "Floor"
        sphereMatName = "SphereMaterial"
        floorMatName = "FloorMaterial"

        sphereMesh = createNewMeshHandle()
        floorMesh = createNewMeshHandle()
        floorMesh = primitives.createPlaneSimple(bmh, 'Floor', floorMatName)
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, 30, 15)

        scene = createNewSceneHandle()
        sceneName = "BakingScene"
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
            apiCall( ILBSetRenderStats(tempInstance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE) )


        # create the floor material
        floorMat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(scene, floorMatName, floorMat) )
        primitives.apiCall( ILBSetMaterialColor(floorMat, ILB_CC_DIFFUSE, ColorRGBA(0.7, 0.7, 0.7, 1.0)) )

        # create sphere material
        sphereMat = createNewMaterialHandle()
        apiCall( ILBCreateMaterial(scene, sphereMatName, sphereMat) )
        apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_DIFFUSE, ColorRGBA(0.9, 0.9, 0.9, 1.0)) )
        #apiCall( ILBSetMaterialColor(sphereMat, ILB_CC_SPECULAR, ColorRGBA(1.0, 1.0, 1.0, 1.0)) )
        #apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_REFLECTION, 0.1) )
        #apiCall( ILBSetMaterialScale(sphereMat, ILB_CC_SHININESS, 15.0) )

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


        beastConfig = beastCacheFolder + "/data/baking.xml"

        dom = minidom.getDOMImplementation()
        xmlDoc = dom.createDocument(None, "ILConfig", None)
        docRoot = xmlDoc.documentElement

        AASettingsElement = xmlDoc.createElement("AASettings")
        xmlCreateElement(xmlDoc, AASettingsElement, "minSampleRate", "0")
        xmlCreateElement(xmlDoc, AASettingsElement, "maxSampleRate", "2")
        docRoot.appendChild(AASettingsElement)


        RenderSettingsElement = xmlDoc.createElement("RenderSettings")
        xmlCreateElement(xmlDoc, RenderSettingsElement, "bias", "0.00001")
        docRoot.appendChild(RenderSettingsElement)

        FrameSettingsElement = xmlDoc.createElement("FrameSettings")
        xmlCreateElement(xmlDoc, FrameSettingsElement, "inputGamma", "0.45")
        outputCorrectionElement = xmlDoc.createElement("outputCorrection")
        xmlCreateElement(xmlDoc, outputCorrectionElement, "colorCorrection", "Gamma")
        xmlCreateElement(xmlDoc, outputCorrectionElement, "gamma", "2.2")
        FrameSettingsElement.appendChild(outputCorrectionElement)



        GISettingsElement = xmlDoc.createElement("GISettings")
        xmlCreateElement(xmlDoc, GISettingsElement, "enableGI", "true")
        xmlCreateElement(xmlDoc, GISettingsElement, "fgRays", "1000")
        xmlCreateElement(xmlDoc, GISettingsElement, "fgContrastThreshold", "0.1")
        xmlCreateElement(xmlDoc, GISettingsElement, "fginterpolationPoints", "15")
        xmlCreateElement(xmlDoc, GISettingsElement, "primaryIntegrator", "FinalGather")
        xmlCreateElement(xmlDoc, GISettingsElement, "secondaryIntegrator", "None")

        docRoot.appendChild(FrameSettingsElement)

        #write file contents
        xmlFile = open(beastConfig, "w")
        xmlFile.write(xmlDoc.toprettyxml())
        xmlFile.close()


        job = createNewJobHandle()
        apiCall( ILBCreateJob( bmh, 'TestJob', scene, beastConfig, job ) )

        fullShadingPass = createNewRenderPassHandle()
        apiCall( ILBCreateFullShadingPass(job, 'fullShading', fullShadingPass) )


        textureTarget = createNewTargetHandle()
        apiCall( ILBCreateTextureTarget(job, "textureTarget", 512, 512, textureTarget))
        entity = createNewTargetEntityHandle()

        # Add the floor instance twice in different parts of the UV space
        apiCall( ILBAddBakeInstance(textureTarget, floorInstance, entity) )
        apiCall( ILBSetUVTransform(entity, Vec2(0.0, 0.0), Vec2(0.5, 1.0)) )

        apiCall( ILBAddBakeInstance(textureTarget, floorInstance, entity) )

        apiCall( ILBSetUVTransform(entity, Vec2(0.5, 0.0), Vec2(0.5, 1.0)) )

        cameraTarget = createNewTargetHandle()
        apiCall( ILBCreateCameraTarget( job, 'cameraTarget', camera, 640, 480, cameraTarget ) )


        apiCall( ILBAddPassToTarget( textureTarget, fullShadingPass ) )
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

