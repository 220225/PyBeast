#Beast API Sample: Readback

#The purpose of this sample is to demonstrate how to use the API to:
 #1. Set up a scene for texure baking and bake lightmaps
 #2. Set up a scene for vertex baking and bake vertex colors
 #3. Read back lightmaps and vertex colors
 #4. Render camera views of the scene with freshly baked lightmaps
     #and vertex colors
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

planeRes = 32
sphereRes = 16
lightmapRes = 128

def xmlCreateElement(_xmlDoc, _parentElm, _newElem, _newElemValue):
    newElement = _xmlDoc.createElement(_newElem)
    newElement.appendChild(_xmlDoc.createTextNode(_newElemValue))
    _parentElm.appendChild(newElement)
    return newElement


class SampleScene:
    def __init__( self, _bmh, _name ):
        self.m_scene = createNewSceneHandle()
        apiCall( ILBBeginScene(_bmh, _name, self.m_scene) )

        self.m_floorInstance = createNewInstanceHandle()
        self.SPHERE_RADIUS = 4.0
        self.m_sphereInstance = createNewInstanceHandle()

        self.m_camera = createNewCameraHandle()



    def createInstances(self, _planeHandle, _sphereHandle):
        """docstring for createInstances"""
        floorTrans = vecmath.scaleTranslation(Vec3(10.0, 1.0, 10.0), Vec3(0.0, -5.0, 0.0))
        apiCall( ILBCreateInstance(self.m_scene, _planeHandle, "FloorInstance", floorTrans, self.m_floorInstance))

        #spherePosRadius = 10.0 - 2.0*self.SPHERE_RADIUS
        trans = vecmath.scaleTranslation(Vec3(self.SPHERE_RADIUS, self.SPHERE_RADIUS, self.SPHERE_RADIUS), Vec3(0.0, self.SPHERE_RADIUS-5.0, 0.0))
        apiCall(ILBCreateInstance(self.m_scene, _sphereHandle, "SphereInstance", trans, self.m_sphereInstance))
        apiCall( ILBSetRenderStats(self.m_sphereInstance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE) )

    def createLight(self):
        """docstring for createLight"""
        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight(self.m_scene,
                                           "Sun",
                                           vecmath.directionalLightOrientation(Vec3(1.0, -1.0, -1.0)),
                                           ColorRGB(1.0, 1.0, 0.8),
                                           light) )
        apiCall( ILBSetCastShadows(light, True) )
        apiCall( ILBSetShadowSamples(light, 32) )
        apiCall( ILBSetShadowAngle(light, 0.1) )
    
        skylight = createNewLightHandle()
        apiCall( ILBCreateSkyLight( self.m_scene, 'SkyLight', vecmath.identity(), ColorRGB(1.0, 0.0, 0.0), skylight) )

    def createDiffuseMaterial(self, _matName, _diffuseCol):
        """docstring for createDiffuseMaterial"""

        mat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(self.m_scene, _matName, mat) )
        primitives.apiCall( ILBSetMaterialColor(mat, ILB_CC_DIFFUSE, _diffuseCol) )

    def createEmissiveMaterial(self, _matName, _textureHandle):
        """docstring for createEmissiveMaterial"""
        mat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(self.m_scene, _matName, mat) )
        primitives.apiCall( ILBSetMaterialTexture(mat, ILB_CC_EMISSIVE, _textureHandle) )

    def createVertexColorMaterial(self, _matName):
        """docstring for createVertexColorMaterial"""
        mat = createNewMaterialHandle()
        primitives.apiCall( ILBCreateMaterial(self.m_scene, _matName, mat) )
        primitives.apiCall( ILBSetMaterialUseVertexColors(mat, ILB_CC_EMISSIVE) )

    def createCamera(self):
        """docstring for createCamera"""
        apiCall( ILBCreatePerspectiveCamera(self.m_scene, 
                 "Camera", 
                 vecmath.translation(Vec3(0.0, 0.0, 10.0)),
                 self.m_camera) )
        #apiCall( ILBCreatePerspectiveCamera(self.m_scene, 
                 #"Camera", 
                 #vecmath.setCameraMatrix(Vec3(0.3, 0.5, 15.0), Vec3(0.1, -0.3, -1.0), Vec3(0.0, 1.0, 0.0)),
                 #self.m_camera) )

    def finalize(self):
        """docstring for finalize"""
        ILBEndScene( self.m_scene)

    def get(self):
        """docstring for get"""
        return self.m_scene
    def getFloorInstance(self):
        """docstring for getFloorInstance"""
        return self.m_floorInstance
    def getSphereInstance(self):
        """docstring for getSphereInstance"""
        return self.m_sphereInstance
    def getCamera(self):
        """docstring for getCamera"""
        return self.m_camera

class SampleJob:
    def __init__( self, _bmh, _name, _scene, _xmlFile ):
        self.m_job = createNewJobHandle()
        apiCall( ILBCreateJob(_bmh, _name, _scene.get(), _xmlFile, self.m_job))

        self.m_bmh = _bmh
        self.m_targets = []
        self.m_textureTargets = {}
        self.m_vertexTargets = {}

        self.m_pass = createNewRenderPassHandle()
        self.createFullShadingPass()


    def createCameraTarget(self, _scene, _xRes, _yRes):
        """docstring for createCameraTarget"""
        target = createNewTargetHandle()
        apiCall(ILBCreateCameraTarget(self.m_job, "cameraTarget", _scene.getCamera(), _xRes, _yRes, target))
        self.m_targets.append(target)

    def createTextureTarget(self, _texName, _xRes, _yRes, _instanceHandle):
        """docstring for createTextureTarget"""
        target = createNewTargetHandle()
        apiCall( ILBCreateTextureTarget(self.m_job, _texName, _xRes, _yRes, target) )
        entitty = createNewTargetEntityHandle()
        apiCall( ILBAddBakeInstance(target, _instanceHandle, entitty) )

        self.m_targets.append(target)
        self.m_textureTargets[_texName] = target

    def createVertexTarget(self, _name, _instanceHandle):
        """docstring for createVertexTarget"""
        target = createNewTargetHandle()
        apiCall( ILBCreateVertexTarget(self.m_job, _name, target) )
        entity = createNewTargetEntityHandle()
        apiCall( ILBAddBakeInstance(target, _instanceHandle, entity) )

        self.m_targets.append(target)
        self.m_vertexTargets[_name] = (target, entity)

    def run(self, _returnWhenComplete, _destroyJob):
        """docstring for run"""
        self.addPassToTargets()
        if not renderJob(self.m_job, _returnWhenComplete, _destroyJob):
            return True
        return False

    def createTextureFromTarget(self, _name):
        """docstring for createTextureFromTarget"""
        if _name not in self.m_textureTargets:
            print "Could not find target " + str(_name) 
            return False

        return textures.copyFrameBuffer(self.m_bmh, self.m_textureTargets[_name], self.m_pass, _name, True)

    def readVertexColors(self, _name, _colors):
        """docstring for readVertexColors"""
        if _name not in self.m_vertexTargets:
            print "Could not find target " + str(_name)
            return False
        textures.copyVertexBuffer(self.m_vertexTargets[_name][0], self.m_pass, self.m_vertexTargets[_name][1], _colors)


    def addPassToTargets(self):
        """docstring for addPassToTargets"""
        for i in range(len(self.m_targets)):
            apiCall(ILBAddPassToTarget(self.m_targets[i], self.m_pass))

    def createFullShadingPass(self):
        """docstring for createFullShadingPass"""
        apiCall(ILBCreateFullShadingPass(self.m_job, "fullShading", self.m_pass))

def createXML(_filename, _gi):
    """docstring for createXML"""
    #beastConfig = beastCacheFolder + "/data/baking.xml"

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
    docRoot.appendChild(FrameSettingsElement)


    if _gi == True:
        GISettingsElement = xmlDoc.createElement("GISettings")
        xmlCreateElement(xmlDoc, GISettingsElement, "enableGI", "true")
        xmlCreateElement(xmlDoc, GISettingsElement, "fgRays", "1000")
        xmlCreateElement(xmlDoc, GISettingsElement, "fgContrastThreshold", "0.1")
        xmlCreateElement(xmlDoc, GISettingsElement, "fginterpolationPoints", "15")
        xmlCreateElement(xmlDoc, GISettingsElement, "primaryIntegrator", "FinalGather")
        xmlCreateElement(xmlDoc, GISettingsElement, "secondaryIntegrator", "None")

        docRoot.appendChild(GISettingsElement)

    #write file contents
    xmlFile = open(_filename, "w")
    xmlFile.write(xmlDoc.toprettyxml())
    xmlFile.close()

def displayResults(_bmh, _floorMesh, _floorMatName, _floorLightmap, _sphereMesh, _sphereMatName, _sphereLightmap, _xmlFile, _lightmaps):
    """docstring for displayResults"""
    suffix = "Lightmap" if _lightmaps == True else "Vertexcolors"
    scene = SampleScene(_bmh, "RenderScnee" + suffix)
    scene.createInstances(_floorMesh, _sphereMesh)
    scene.createCamera()

    if _lightmaps == True:
        scene.createEmissiveMaterial(_floorMatName, _floorLightmap)
        scene.createEmissiveMaterial(_sphereMatName, _sphereLightmap)
    else:
        scene.createVertexColorMaterial(_floorMatName)
        scene.createVertexColorMaterial(_sphereMatName)

    scene.finalize()
    job = SampleJob(_bmh, "RenderJob"+suffix, scene, _xmlFile)
    job.createCameraTarget(scene, 640, 480)
    job.run(False, True)


def main(argv):
    """docstring for main"""
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
        dir = beastCacheFolder + r'/temp/readback'

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
        floorMesh = primitives.createPlane(bmh, 'Floor', floorMatName, planeRes, planeRes)
        sphereMesh = primitives.createSphere(bmh, 'Sphere', sphereMatName, sphereRes, sphereRes)

        bakingScene = SampleScene(bmh, "BakingScene")
        bakingScene.createInstances(floorMesh, sphereMesh)
        bakingScene.createLight()
        bakingScene.createCamera()

        bakingScene.createDiffuseMaterial(floorMatName, ColorRGBA(0.7, 0.7, 0.7, 1.0))
        bakingScene.createDiffuseMaterial(sphereMatName, ColorRGBA(0.9, 0.9, 0.9, 1.0))
        bakingScene.finalize()

        beastConfig = beastCacheFolder + "/data/baking.xml"
        createXML(beastConfig, True)

        bakeJob = SampleJob(bmh, "BakeJob", bakingScene, beastConfig)
        bakeJob.createTextureTarget("floorTextureTarget", lightmapRes, lightmapRes, bakingScene.getFloorInstance())
        bakeJob.createTextureTarget("sphereTextureTarget", lightmapRes, lightmapRes, bakingScene.getSphereInstance())
        bakeJob.createVertexTarget("floorVertexTarget", bakingScene.getFloorInstance())
        bakeJob.createVertexTarget("sphereVertexTarget", bakingScene.getSphereInstance())

        if bakeJob.run(True, False):
            return True

        # read back the lightmaps as textures
        lightmapFloor = bakeJob.createTextureFromTarget("floorTextureTarget")
        lightmapSphere = bakeJob.createTextureFromTarget("sphereTextureTarget")

        floorVertexColors = FloatArray()
        bakeJob.readVertexColors("floorVertexTarget", floorVertexColors)

        sphereVertexColors = FloatArray()
        bakeJob.readVertexColors("sphereVertexTarget", sphereVertexColors)

        floorMeshColors = primitives.createPlane(bmh, "FloorColor", floorMatName, planeRes, planeRes, floorVertexColors)
        sphereMeshColors = primitives.createSphere(bmh, "SphereColor", sphereMatName, sphereRes, sphereRes, sphereVertexColors)

        noGIConfig = beastCacheFolder + "/data/bakingNoGI.xml"
        createXML(noGIConfig, False)

        displayResults(bmh, floorMeshColors, floorMatName, lightmapFloor, sphereMeshColors, sphereMatName, lightmapSphere, noGIConfig, True)

        displayResults(bmh, floorMeshColors, floorMatName, lightmapFloor, sphereMeshColors, sphereMatName, lightmapSphere, noGIConfig, False)

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

