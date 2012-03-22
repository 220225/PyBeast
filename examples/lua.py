#Beast API Sample: LUA

#The purpose of this sample is to demonstrate how to create a LUA pass, 
#render with it and retrieve the results.
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
        
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        configItems = {}
        for item in config.items('BeastPythonExamples'):
            configItems[item[0]] = item[1]

        # Setup our beast manager
        beastCacheFolder = os.path.normpath(configItems['beast_cache'])
        beastBinFolder = os.path.normpath(configItems['beast_bin'])
        beastDataFolder = os.path.normpath(configItems['beast_data'])
        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/lua', ILB_CS_LOCAL, bmh) )
        
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
        beastConfig = beastCacheFolder + "/data/lua.xml"

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
        apiCall( ILBCreateJob( bmh, 'TestJob', scene, beastConfig, job ) )

        
        luaConfig = beastCacheFolder + r'/data/rnm_3.lua'
        luaPass = createNewRenderPassHandle()
        apiCall( ILBCreateLuaPass(job, "LUA", luaConfig, luaPass))
        apiCall( ILBCreateLuaPass(job, "LUA2", luaConfig, luaPass))


        textureTarget = createNewTargetHandle()
        apiCall( ILBCreateTextureTarget(job, "textureTarget", 256, 256, textureTarget) )
        entity = createNewTargetEntityHandle()
        apiCall( ILBAddBakeInstance(textureTarget, cornellInstance, entity) )

        apiCall( ILBAddPassToTarget(textureTarget, luaPass) )

        if not renderJob( job, False, False, ILB_RD_FORCE_LOCAL ):
            print "render error occured"

        fb = createNewFramebufferHandle()
        apiCall( ILBGetFramebuffer(textureTarget, luaPass, 0, fb) )
        channelCount = ILBInt32(0)
        apiCall( ILBGetChannelCount(fb, channelCount) )
        
        for i in range(channelCount.value):
            sth = createNewStringHandle()
            apiCall( ILBGetChannelName(fb, i, sth) )
            channelName = convertStringHandle(sth)
            print str(i)  + ": " + channelName
                

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

