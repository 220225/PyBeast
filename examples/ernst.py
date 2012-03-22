#Beast API Sample: eRnsT light setup session

#The purpose of this sample is to demonstrate how to:
#1. Start a session in eRnsT
#2. Edit the lighting in a scene
#3. Use the lighting changes made in eRnsT
from BeastPython.beastPython import *
from BeastPython.common.utils import *
from BeastPython.common import primitives
from BeastPython.common import textures
from BeastPython.common import vecmath

from xml.dom import minidom
import ConfigParser
import os
import math
import random

SPHERES = 50
SPHERE_RADIUS = 1.0
EXPONENT_FALLOFF, MAXRANGE_FALLOFF, POLYNOMIAL_FALLOFF = range(3)

def constructMesh(_name, _vertices, _normals, _uvs, _matName, _mangerHandle):
    """docstring for contstructMesh"""
    mesh = createNewMeshHandle()
    apiCall( ILBBeginMesh(_mangerHandle, _name, mesh) )
    apiCall( ILBAddVertexData(mesh, _vertices, _normals, len(_vertices)) )

    apiCall( ILBBeginMaterialGroup(mesh, _matName) )
    indices = Int32Array()

    for idx in range(len(_vertices)):
        indices.append(idx)

    apiCall( ILBAddTriangleData(mesh, indices, len(indices)) )
    apiCall( ILBEndMaterialGroup(mesh) )

    apiCall( ILBBeginUVLayer(mesh, "uv1") )
    apiCall( ILBAddUVData(mesh, _uvs, len(_uvs)) )
    apiCall( ILBEndUVLayer(mesh) )

    apiCall( ILBEndMesh(mesh) )
    return mesh

class Material:
    def __init__( self ):
        self.diffuse = ColorRGBA()
        self.emissive = ColorRGBA()
        self.specular = ColorRGBA()
        self.shininess = 0.0
class Group:
    def __init__(self):
        """docstring for __init__"""
        self.material = Material()
        self.materialName = ''
        self.vertexIndexList = []
        self.normalIndexList = []
        self.uvIndexList = []

class OBJReader:
    def __init__( self ):
        self.m_vertices = []
        self.m_vertexNormals = []
        self.m_UVs = []

        self.m_materialMap = {}
        self.m_dummyMaterial = Material()
        self.m_dummyMaterial.diffuse = ColorRGBA(0.9, 0.9, 0.9, 1.0)
        self.m_materialMap['dummy'] = self.m_dummyMaterial
        self.m_currentMaterial = self.m_dummyMaterial
        self.m_currentMaterialName = 'dummy'

        self.m_groupMap = {}
        self.m_path = ''
        self.m_currentGroup = None


    def loadObjFile(self, _file):
        """docstring for loadObjFile"""
        self.m_path = os.path.dirname(os.path.normpath(_file))
        self.loadFile(_file)

    def getMeshNames(self, _meshNames):
        """docstring for getMeshNames"""
        for meshName in self.m_groupMap.keys():
            _meshNames.append(meshName)

    def getMaterials(self):
        """docstring for getMaterials"""
        return self.m_materialMap
    
    def getMeshData(self, _meshName, _vertices, _normals, _UVs):
        """docstring for getMeshData"""
        materialName = ""
        if _meshName in self.m_groupMap:
            group = self.m_groupMap[_meshName]
            #print "cur group = " + str(group) + " vertexIndex size = " + str(len(group.vertexIndexList))

            for i in range(len(group.vertexIndexList)):
                _vertices.append( self.m_vertices[group.vertexIndexList[i] - 1 ] )
                _normals.append( self.m_vertexNormals[group.normalIndexList[i] - 1] )
                _UVs.append( self.m_UVs[group.uvIndexList[i] - 1])

            materialName = group.materialName
        
        return materialName


    def tokenizeString(self, _input, _breakChar):
        """docstring for tokenizeString"""
        return _input.split(_breakChar)

    def processTokens(self, _tokens):
        """docstring for processTokens"""
        if len(_tokens) == 0:
            return
        elif _tokens[0] == 'v':
            self.m_vertices.append( Vec3(float(_tokens[1]), float(_tokens[2]), float(_tokens[3])) )
        elif _tokens[0] == 'mtllib':
            self.loadFile( os.path.normpath(self.m_path + "\\" + _tokens[1]))
        elif _tokens[0] == 'vn':
            self.m_vertexNormals.append(  Vec3(float(_tokens[1]), float(_tokens[2]), float(_tokens[3])) )
        elif _tokens[0] == 'vt':
            self.m_UVs.append( Vec2( float(_tokens[1]), float(_tokens[2])) )
        elif _tokens[0] == 'f':
            if self.m_currentGroup != None:
                for i in range(4):
                    faces = self.tokenizeString(_tokens[i], '/')
                    if len(faces) == 3:
                        self.m_currentGroup.vertexIndexList.append( int(faces[0]) )
                        self.m_currentGroup.uvIndexList.append( int(faces[1]) )
                        self.m_currentGroup.normalIndexList.append( int(faces[2]) )
        elif _tokens[0] == 'g':
            groupName = _tokens[1]
            if len(_tokens) > 2:
                for i in rnage(2, len(_tokens)):
                    groupName = groupName + '.' + _tokens[i]

            if groupName not in self.m_groupMap.keys():
                g = Group()
                g.material = self.m_currentMaterial
                g.materialName = self.m_currentMaterialName
                self.m_groupMap[groupName] = g
                self.m_currentGroup = self.m_groupMap[groupName]
            else:
                self.m_currentGroup = self.m_groupMap[groupName]
        elif _tokens[0] == 'usemtl':
            # no gorup, no material name!

            if self.m_currentGroup != None:
                if _tokens[1] not in self.m_materialMap.keys():
                    self.m_currentGroup.material = self.m_dummyMaterial
                    self.m_currentGroup.materialName = 'dummy'
                else:
                    self.m_currentMaterial = self.m_materialMap[_tokens[1]]
                    self.m_currentMaterialName = _tokens[1]
                    self.m_currentGroup.material = self.m_materialMap[_tokens[1]]
                    self.m_currentGroup.materialName = _tokens[1]
                
        elif _tokens[0] == 'newmtl':
            self.m_materialMap[_tokens[1]] = Material()
            self.m_currentMaterial = self.m_materialMap[_tokens[1]]
            self.m_currentMaterialName = _tokens[1]

        elif _tokens[0] == 'Kd':
            if self.m_currentMaterialName in self.m_materialMap:
                self.m_materialMap[self.m_currentMaterialName].diffuse = ColorRGBA(float(_tokens[1]), float(_tokens[2]), float(_tokens[3]), 1.0)
        elif _tokens[0] == 'Ke':
            if self.m_currentMaterialName in self.m_materialMap:
                self.m_materialMap[self.m_currentMaterialName].emissive = ColorRGBA(float(_tokens[1]), float(_tokens[2]), float(_tokens[3]), 1.0)
        elif _tokens[0] == 'Ks':
            if self.m_currentMaterialName in self.m_materialMap:
                self.m_materialMap[self.m_currentMaterialName].specular = ColorRGBA(float(_tokens[1]), float(_tokens[2]), float(_tokens[3]), 1.0)
        elif _tokens[0] == 'Ns':
            if self.m_currentMaterialName in self.m_materialMap:
                self.m_materialMap[self.m_currentMaterialName].shininess = float(_tokens[1])

    def loadFile(self, _file):
        """docstring for loadFile"""

        print "load -> " + str(_file)

        objFile = open (_file, "r")
        objContent = []
        try:
            while True:
                line = objFile.readline()
                if(len(line) == 0):
                    break
                line = line.strip("\n")
                # Get the list of retargeted motionbuilder scenes
                objContent.append(line)
        finally:
            objFile.close()
        print "done read!"

        for line in objContent:
            input = self.tokenizeString(line, ' ')
            self.processTokens(input)



class TargetEnttiy:
    def __init__( self, _transform, _meshHandle, _name, _width = None, _height = None ):
        self.m_transform = _transform
        self.m_mesh = _meshHandle
        self.m_name = _name
        if _width == None and _height == None:
            self.m_type = ILB_TT_VERTEX
        else:
            self.m_width = _width
            self.m_height = _height
            self.m_type = ILB_TT_TEXTURE

        self.m_instance = createNewInstanceHandle()

    def getName(self):
        """docstring for getName"""
        return self.m_name

    def update(self, _type, _width, _height):
        """docstring for update"""
        self.m_type = _type
        self.m_width = _width
        self.m_height = _height

    def createScene(self, _sceneHandle):
        """docstring for createScene"""
        apiCall( ILBCreateInstance(_sceneHandle, self.m_mesh, self.m_name, self.m_transform, self.m_instance) )
        apiCall( ILBSetRenderStats(self.m_instance, ILB_RS_SHADOW_BIAS, ILB_RSOP_ENABLE) )

    def create(self, _objVertexTargetHandle, _objAtlasTarget):
        """docstring for create"""
        objEntity = createNewTargetEntityHandle()
        if self.m_type == ILB_TT_VERTEX:
            apiCall( ILBAddBakeInstance(_objVertexTargetHandle, self.m_instance, objEntity) )
        elif self.m_type == ILB_TT_TEXTURE:
            apiCall( ILBAddBakeInstance(_objAtlasTarget, self.m_instance, objEntity) )
            apiCall( ILBSetBakeResolution(objEntity, self.m_width, self.m_height) )


class TargetManager:
    def __init__( self ):
        self.m_targets = {}

    def addTarget(self, _target):
        """docstring for addTarget"""
        if _target.getName() in self.m_targets:
            del self.m_targets[_target.getName()]
        self.m_targets[_target.getName()] = _target
        
    def update(self, _name, _type, _width, _height):
        """docstring for update"""
        if _name in self.m_targets:
            self.m_targets[_name].update(_type, _width, _height)

    def createScene(self, _sceneHandle):
        """docstring for createScene"""
        for target in self.m_targets.values():
            target.createScene(_sceneHandle)

    def create(self, _jobHandle):
        """docstring for create"""
        objVertexTarget = createNewTargetHandle()
        objAtlasTarget = createNewTargetHandle()

        apiCall( ILBCreateVertexTarget(_jobHandle, "objVertexTarget", objVertexTarget) )
        apiCall( ILBCreateAtlasedTextureTarget(_jobHandle, "objAtlasTarget", 1024, 1024, 0, objAtlasTarget) )

        for target in self.m_targets.values():
            target.create(objVertexTarget, objAtlasTarget)


            
class Camera:
    def __init__( self, _name, _transform, _horizontalFov, _pixelAspectRatio ):

        self.m_name = _name
        self.m_transform = _transform
        self.m_horizontalFov = _horizontalFov
        self.m_pixelAspectRatio = _pixelAspectRatio

    def create(self, _sceneHandle):
        """docstring for create"""
        camera = createNewCameraHandle()
        apiCall( ILBCreatePerspectiveCamera(_sceneHandle, self.m_name, self.m_transform, camera) )
        apiCall( ILBSetFov(camera, self.m_horizontalFov, self.m_pixelAspectRatio) )
        return camera

def getCameraFromHandle(_cameraHandle):
    """docstring for getCameraFromHandle"""
    namehandle = createNewStringHandle()
    apiCall( ILBGetCameraName(_cameraHandle, namehandle))
    name = convertStringHandle(namehandle)
    transform = Matrix4x4()
    apiCall( ILBGetCameraTransform(_cameraHandle, transform))

    hfov = par = ILBFloat(0.0)
    apiCall( ILBGetCameraFov(_cameraHandle, hfov, par))
    return Camera(name, transform, hfov.value, par.value)

class LightSource:
    def __init__( self, _name, _transform, _color ):

        self.m_name = _name
        self.m_displayName = _name
        self.m_transform = _transform
        self.m_color = _color
        self.m_intensity = 1.0
        self.m_castShadows = True
        self.m_shadowSamples = 1

        self.m_directScale = 1.0
        self.m_indirectScale = 1.0

        self.m_visibleForEye = True
        self.m_visibleForRefl = True
        self.m_visibleForRefr = True
        self.m_visibleForGI = True

    def setDisplayName(self, _displayName):
        """docstring for setDisplayName"""
        self.m_displayName = _displayName

    def setTransform(self, _transform):
        """docstring for transform"""
        self.m_transform = _transform

    def setColor(self, _color):
        """docstring for setColor"""
        self.m_color = _color

    def setIntensity(self, _intensity):
        """docstring for setIntensity"""
        self.m_intensity = _intensity

    def setCastShadows(self, _castShadows):
        """docstring for setCastShadows"""
        self.m_castShadows = _castShadows

    def setShadowSamples(self, _shadowSamples):
        """docstring for setShadowSamples"""
        self.m_shadowSamples = _shadowSamples

    def setIntenstiyScale(self, _directScale, _indirectScale):
        """docstring for setIntenstiyScale"""
        self.m_directScale = _directScale
        self.m_indirectScale = _indirectScale

    def setVisibleForEye(self, _v):
        """docstring for setVisibleForEye"""
        self.m_visibleForEye = _v

    def setVisibleForRefl(self, _v):
        """docstring for setVisibleForRefl"""
        self.m_visibleForRefl = _v
    def setVisibleForRefr(self, _v):
        """docstring for setVisibleForRefr"""
        self.m_visibleForRefr = _v
    def setVisibleForGI(self, _v):
        """docstring for setVisibleForGI"""
        self.m_visibleForGI = _v

    def getName(self):
        """docstring for getName"""
        return self.m_name

    # python 2.7 +
    #@abstractmethod 
    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        pass
    def setBasicParameters(self, _lightHandle):
        """docstring for setBasicParametes"""
        ILBSetLightDisplayName(_lightHandle, self.m_displayName)
        ILBSetLightIntensity(_lightHandle, self.m_intensity)
        ILBSetCastShadows(_lightHandle, self.m_castShadows)
        ILBSetShadowSamples(_lightHandle, self.m_shadowSamples)
        ILBSetIntensityScale(_lightHandle, self.m_directScale, self.m_indirectScale)
        ILBSetLightStats(_lightHandle, ILB_LS_VISIBLE_FOR_EYE, ILB_LSOP_ENABLE if self.m_visibleForEye == True else ILB_LSOP_DISABLE)
        ILBSetLightStats(_lightHandle, ILB_LS_VISIBLE_FOR_REFLECTIONS, ILB_LSOP_ENABLE if self.m_visibleForRefl == True else ILB_LSOP_DISABLE)
        ILBSetLightStats(_lightHandle, ILB_LS_VISIBLE_FOR_REFRACTIONS, ILB_LSOP_ENABLE if self.m_visibleForRefr == True else ILB_LSOP_DISABLE)
        ILBSetLightStats(_lightHandle, ILB_LS_VISIBLE_FOR_GI, ILB_LSOP_ENABLE if self.m_visibleForGI == True else ILB_LSOP_DISABLE)


class FalloffLightSource(LightSource):
    def __init__( self, _name, _transform, _color ):
        LightSource.__init__( self, _name, _transform, _color )

        self.m_falloffType = EXPONENT_FALLOFF
        self.m_exponent = 0.0
        self.m_constnat = 0.0
        self.m_linear = 0.0
        self.m_quadratic = 1.0
        self.m_cutoff = sys.float_info.max
        self.m_clamp = True
    

    def setExponentFalloff(self, _cutoff, _exponent, _clamp):
        """docstring for setExponentFalloff"""
        self.m_falloffType = EXPONENT_FALLOFF
        self.m_cutoff = _cutoff
        self.m_exponent = _exponent
        self.m_clamp = _clamp

    def setMaxRangeFalloff(self, _cutoff, _exponent):
        """docstring for setMaxRangeFalloff"""
        self.m_falloffType = MAXRANGE_FALLOFF
        self.m_cutoff = _cutoff
        self.m_exponent = _exponent

    def setPolynomialFalloff(self, _cutoff, _constant, _linear, _quadratic, _clamp):
        """docstring for setPolynomialFalloff"""
        self.m_falloffType = POLYNOMIAL_FALLOFF
        self.m_cutoff = _cutoff
        self.m_constant = _constant
        self.m_linear = _linear
        self.m_quadratic = _quadratic
        self.m_clamp = _clamp

    def setBasicParameters(self, _lightHandle):
        """docstring for setBasicParameters"""
        LightSource.setBasicParameters(self, _lightHandle)

        if self.m_falloffType == EXPONENT_FALLOFF:
            apiCall( ILBSetLightExponentFalloff(_lightHandle, self.m_cutoff, self.m_exponent, self.m_clamp))
        elif self.m_falloffType == MAXRANGE_FALLOFF:
            apiCall( ILBSetLightMaxRangeFalloff(_lightHandle, self.m_cutoff, self.m_exponent))
        elif self.m_falloffType == POLYNOMIAL_FALLOFF:
            apiCall( ILBSetLightPolynomialFalloff(_lightHandle, self.m_cutoff, self.m_constant, self.m_linear, self.m_quadratic, self.m_clamp) )


class PointLightSource(FalloffLightSource):
    def __init__( self, _name, _transform, _color ):
        FalloffLightSource.__init__( self, _name, _transform, _color )

        self.m_shadowRadius = 0.0
    
    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        light = createNewLightHandle()
        apiCall( ILBCreatePointLight(_sceneHandle, self.m_name, self.m_transform, self.m_color, light) )
        self.setBasicParameters(light)
        return light

    def setShadowRadius(self, _shadowRadius):
        """docstring for setShadowRadius"""
        self.m_shadowRadius = _shadowRadius

    def setBasicParameters(self, _lightHandle):
        """docstring for setBasicParameters"""
        FalloffLightSource.setBasicParameters(self, _lightHandle)
        apiCall(ILBSetShadowRadius(_lightHandle, self.m_shadowRadius))
        

class SpotLightSource(PointLightSource):
    def __init__( self, _name, _transform, _color ):
        PointLightSource.__init__( self, _name, _transform, _color )

        self.m_angle = math.pi/2.0
        self.m_penumbraAngle = 0.0
        self.m_penumbraExponent = 1.0
    
    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        light = createNewLightHandle()
        apiCall( ILBCreateSpotLight(_sceneHandle, self.m_name, self.m_transform, self.m_color, light) )
        self.setBasicParameters(light)
        return light

    def setCone(self, _angle, _penumbraAngle, _penumbraExponent):
        """docstring for setCone"""
        self.m_angle = _angle
        self.m_penumbraAngle = _penumbraAngle
        self.m_penumbraExponent = _penumbraExponent

    def setBasicParameters(self, _lightHandle):
        """docstring for setBasicParameters"""
        PointLightSource.setBasicParameters(self,_lightHandle)
        apiCall(ILBSetSpotlightCone(_lightHandle, self.m_angle, self.m_penumbraAngle, self.m_penumbraExponent))


class AreaLightSource(FalloffLightSource):
    def __init__( self, _name, _transform, _color ):
        FalloffLightSource.__init__( self, _name, _transform, _color )
    
    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        light = createNewLightHandle()
        apiCall( ILBCreateAreaLight(_sceneHandle, self.m_name, self.m_transform, self.m_color, light) )
        self.setBasicParameters(light)
        return light

class DirectionalLightSource(LightSource):
    def __init__( self, _name, _transform, _color ):
        LightSource.__init__( self, _name, _transform, _color )

        self.m_shadowAngle = 0.0

    def setShadowAngle(self, _shadowAngle):
        """docstring for setShadowAngle"""
        self.m_shadowAngle = _shadowAngle
    
    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        light = createNewLightHandle()
        apiCall( ILBCreateDirectionalLight(_sceneHandle, self.m_name, self.m_transform, self.m_color, light) )
        self.setBasicParameters(light)
        return light

    def setBasicParameters(self, _lightHandle):
        """docstring for setBasicParameters"""
        LightSource.setBasicParameters(self, _lightHandle)
        apiCall(ILBSetShadowAngle(_lightHandle, self.m_shadowAngle))


class SkyLightSource(LightSource):
    def __init__( self, _name, _transform, _color ):
        LightSource.__init__( self, _name, _transform, _color )

        self.m_volumeType = ILB_LVT_INFINITY
        self.m_texture = None
    
    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        light = createNewLightHandle()
        apiCall( ILBCreateSkyLight(_sceneHandle, self.m_name, self.m_transform, self.m_color, light) )
        self.setBasicParameters(light)

        if self.m_texture != None:
            tex = createNewTextureHandle()
            if ILBFindTexture(_managerHandle, self.m_texture, tex) != ILB_ST_SUCCESS:
                apiCall(ILBReferenceTexture(_managerHandle, self.m_texture, self.m_texture, tex))

            apiCall(ILBSetSkyTexture(light, tex))

        return light

    def setVolumeType(self, _volumeTyp):
        """docstring for setVolumeType"""
        self.m_volumeType = _volumeTyp

    def setTexture(self, _texture):
        """docstring for setVolumeType"""
        self.m_texture = _texture

    def setBasicParameters(self, _lightHandle):
        """docstring for setBasicParameters"""
        LightSource.setBasicParameters(self, _lightHandle)
        apiCall(ILBSetSkyLightVolumeType(_lightHandle, self.m_volumeType))


class LightManager:
    def __init__(self):
        self.m_lights = {}

    def addLight(self, _lightSource):
        """docstring for addLight"""
        if _lightSource.getName() in self.m_lights.keys():
            del self.m_lights[_lightSource.getName()]

        self.m_lights[_lightSource.getName()] = _lightSource

    def deleteLight(self, _name):
        """docstring for deleteLight"""
        if _name in self.m_lights:
            del self.m_lights[_name]

    def create(self, _managerHandle, _sceneHandle):
        """docstring for create"""
        for lightSource in self.m_lights.values():
            lightSource.create(_managerHandle, _sceneHandle)

def getLightFromHandle(_h):
    """docstring for getLightFromHandle"""
    nameHandle = createNewStringHandle()
    apiCall( ILBGetLightName(_h, nameHandle) )
    name = convertStringHandle(nameHandle)

    color = ColorRGB(0, 0, 0)
    apiCall( ILBGetLightColor(_h, color) )

    transform = Matrix4x4()
    apiCall( ILBGetLightTransform(_h, transform) )
    
    #type = ILB_LST_SPOT
    type = createNewLightType()
    apiCall( ILBGetLightType(_h, type) )

    light = falloffLight = None

    if type.value == ILB_LST_SPOT:
        spotLight = SpotLightSource(name, transform, color)
        shadowRadius = ILBFloat(0.0)
        apiCall( ILBGetShadowRadius(_h, shadowRadius))
        spotLight.setShadowRadius(shadowRadius.value)

        angleRadians = penumbraAngleRadians = penumbraExponent = ILBFloat(0.0)
        apiCall( ILBGetSpotlightCone(_h, angleRadians, penumbraAngleRadians, penumbraExponent) )
        spotLight.setCone(angleRadians.value, penumbraAngleRadians.value, penumbraExponent.value)
        light = falloffLight = spotLight

    elif type.value == ILB_LST_POINT:
        pointLight = PointLightSource(name, transform, color)
        shadowRadius = ILBFloat(0.0)
        apiCall( ILBGetShadowRadius(_h, shadowRadius))
        pointLight.setShadowRadius(shadowRadius.value)
        light = falloffLight = pointLight

    elif type.value == ILB_LST_AREA:
        areaLight = AreaLightSource(name, transform, color)
        light = falloffLight = areaLight

    elif type.value == ILB_LST_DIRECTIONAL:
        dirLight = DirectionalLightSource(name, transform, color)
        shadowAngle = ILBFloat()
        apiCall( ILBGetShadowAngle(_h, shadowAngle))
        dirLight.setShadowAngle(shadowAngle.value)
        light = dirLight

    elif type.value == ILB_LST_SKY:
        skyLight = SkyLightSource(name, transform, color)
        volumeType = createNewLightVolumeType()#ILBLightVolumeType()
        apiCall( ILBGetSkyLightVolumeType(_h, volumeType))
        skyLight.setVolumeType(volumeType.value)
        light = skyLight

    #elif type == ILB_LST_WINDOW:
    else:
        return 0


    displayNameHandle = createNewStringHandle()
    apiCall(ILBGetLightDisplayName(_h, displayNameHandle))
    displayName = convertStringHandle(displayNameHandle)
    light.setDisplayName(displayName)

    intensity = ILBFloat(0.0)
    apiCall(ILBGetLightIntensity(_h, intensity))
    light.setIntensity(intensity.value)

    directScale = ILBFloat(0.0)
    indirectScale = ILBFloat(0.0)
    apiCall(ILBGetLightIntensityScale(_h, directScale, indirectScale))
    light.setIntenstiyScale(directScale.value, indirectScale.value)

    #ILBLightStatsMask statsResult
    statsResult = createNewLightStatsMask()
    apiCall(ILBGetLightStats(_h, ILB_LS_VISIBLE_FOR_EYE, statsResult))
    light.setVisibleForEye(statsResult.value != 0)

    apiCall(ILBGetLightStats(_h, ILB_LS_VISIBLE_FOR_REFLECTIONS, statsResult))
    light.setVisibleForRefl(statsResult.value != 0)

    apiCall(ILBGetLightStats(_h, ILB_LS_VISIBLE_FOR_REFRACTIONS, statsResult))
    light.setVisibleForRefr(statsResult.value != 0)
    apiCall(ILBGetLightStats(_h, ILB_LS_VISIBLE_FOR_GI, statsResult))
    light.setVisibleForGI(statsResult.value != 0)

    #ILBBool castShadows;
    castShadows = ILBBool()
    apiCall(ILBGetLightCastShadows(_h, castShadows))
    light.setCastShadows(castShadows.value!=False)

    #int32 shadowSamples;
    shadowSamples = ILBInt32(0)
    apiCall(ILBGetLightShadowSamples(_h, shadowSamples))
    light.setShadowSamples(shadowSamples.value)

    if falloffLight != None:
        #ILBFalloffType ft;
        #ft = ILB_FO_EXPONENT
        ft = createNewFalloffType()
        apiCall(ILBGetLightFalloffType(_h, ft))

        if ft.value == ILB_FO_EXPONENT: 
            cutoff = ILBFloat(0.0)
            exponent = ILBFloat(0.0)
            clamp = ILBBool()
            apiCall(ILBGetLightExponentFalloff(_h, cutoff, exponent, clamp))
            falloffLight.setExponentFalloff(cutoff.value, exponent.value, clamp.value !=0)

        elif ft.value == ILB_FO_MAX_RANGE: 
            cutoff = ILBFloat(0.0)
            exponent = ILBFloat(0.0)
            apiCall(ILBGetLightMaxRangeFalloff(_h, cutoff, exponent))
            falloffLight.setMaxRangeFalloff(cutoff.value, exponent.value)
        elif ft.value == ILB_FO_POLYNOMIAL:
            cutoff = ILBFloat(0.0)
            linear = ILBFloat(0.0)
            constant = ILBFloat(0.0)
            quadratic = ILBFloat(0.0)
            clamp = ILBBool()
            apiCall(ILBGetLightPolynomialFalloff(_h, cutoff, constant, linear, quadratic, clamp))
            falloffLight.setPolynomialFalloff(cutoff.value, constant.value, linear.value, quadratic.value, clamp.value!=0)

    return light;



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

        apiCall( ILBCreateManager( beastCacheFolder + r'/temp/ernst', ILB_CS_LOCAL, bmh) )
        
        # Set the path to the Beast binaries
        apiCall( ILBSetBeastPath(bmh, beastBinFolder) )

        # Waste the cache from previous runs if present
        apiCall( ILBClearCache(bmh) )


        objReader = OBJReader()
        objFileName = beastCacheFolder + r'/data/hangar.obj'
        objReader.loadObjFile(objFileName)

        meshNames = []
        meshHandles = {}
        objReader.getMeshNames(meshNames)
        for i in range(len(meshNames)):

            vertices = Vec3Array()
            normals = Vec3Array()
            uvs = Vec2Array()
            materialName = None
            materialName = objReader.getMeshData(meshNames[i], vertices, normals, uvs)

            if len(vertices) != 0:
                meshHandles[meshNames[i]] = constructMesh(meshNames[i], vertices, normals, uvs, materialName, bmh)

        lightManager = LightManager()

        sun = DirectionalLightSource( "Sun", 
                                      vecmath.translation(Vec3(0.0, 7.5, -20.0)) * vecmath.directionalLightOrientation(vecmath.normalize(Vec3(-1.0, -1.0, -0.25))), 
            ColorRGB(0.6, 0.6, 0.5))
        sun.setCastShadows(True);
        sun.setShadowSamples(32);
        sun.setShadowAngle(0.025);
        lightManager.addLight(sun);     

        sky = SkyLightSource( "Sky", vecmath.translation(Vec3(0.0, 5.0, -00.0)), ColorRGB(0.25, 0.3, 0.4))
        lightManager.addLight(sky)

        sceneUpVector = ILB_UP_POS_Y
        sceneScale = 1.0
        perspCamera = Camera("Camera", vecmath.translation(Vec3(-5.0, 5.0, -10.0)) * vecmath.cameraOrientation(vecmath.normalize(Vec3(0.25, -0.25, -1.0)), Vec3(0.0, 1.0, 0.0)), math.pi/2.0, 1.0)

        targetManager = TargetManager()
        objTrans = vecmath.scaleTranslation(Vec3(1.0, 1.0, 1.0), Vec3(0.0, 0.0, 0.0))

        for mesh in meshHandles:
            width = 64
            height = 64
            if meshNames[i] == "Ground":
                targetManager.addTarget(TargetEnttiy(objTrans, meshHandles[mesh], mesh))
            else:
                targetManager.addTarget(TargetEnttiy(objTrans, meshHandles[mesh], mesh, width, height))
                

        while True:
            beastConfig = beastCacheFolder + "/data/ernst.xml"

            dom = minidom.getDOMImplementation()
            xmlDoc = dom.createDocument(None, "ILConfig", None)
            docRoot = xmlDoc.documentElement

            AASettingsElement = xmlDoc.createElement("AASettings")
            xmlCreateElement(AASettingsElement, "minSampleRate", "0")
            xmlCreateElement(AASettingsElement, "maxSampleRate", "2")
            docRoot.appendChild(AASettingsElement)


            RenderSettingsElement = xmlDoc.createElement("RenderSettings")
            xmlCreateElement(RenderSettingsElement, "bias", "1e-005")
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
            xmlCreateElement(GISettingsElement, "fgInterpolationPoints", "15")
            xmlCreateElement(GISettingsElement, "primaryIntegrator", "FinalGather")
            xmlCreateElement(GISettingsElement, "secondaryIntegrator", "PathTracer")
            docRoot.appendChild(GISettingsElement)

            # write file contents
            xmlFile = open(beastConfig, "w")
            xmlFile.write(xmlDoc.toprettyxml())
            xmlFile.close()
            
            scene = createNewSceneHandle()
            apiCall(ILBBeginScene(bmh, "ErnstScene", scene))

            ILBSetSceneUpVector(scene, sceneUpVector)
            ILBSetMeterPerWorldUnit(scene, sceneScale)

            lightManager.create(bmh, scene)
            targetManager.createScene(scene)

            materialMap = objReader.getMaterials()
            for material in materialMap:
                mat = createNewMaterialHandle()
                curmat = materialMap[material]

                apiCall(ILBCreateMaterial(scene, material, mat))
                apiCall(ILBSetMaterialColor(mat, ILB_CC_DIFFUSE, materialMap[material].diffuse))
                apiCall(ILBSetMaterialColor(mat, ILB_CC_EMISSIVE, materialMap[material].emissive))
                if materialMap[material].shininess > 0.0:
                    apiCall(ILBSetMaterialColor(mat, ILB_CC_SPECULAR, materialMap[material].specular))
                    apiCall(ILBSetMaterialScale(mat, ILB_CC_SHININESS, materialMap[material].shininess))

            cameraHandle = perspCamera.create(scene)
            apiCall(ILBEndScene(scene))

            # Render the scene from the camera
            job = createNewJobHandle()
            ILBCreateJob(bmh, "RenderJob", scene, beastConfig, job)
            fullShadingPass = createNewRenderPassHandle()
            apiCall(ILBCreateFullShadingPass(job, "fullShading", fullShadingPass))
            cameraTarget = createNewTargetHandle()
            apiCall(ILBCreateCameraTarget(job, "cameraTarget", cameraHandle, 640, 480, cameraTarget))
            apiCall(ILBAddPassToTarget(cameraTarget, fullShadingPass))
            if not renderJob(job):
                print "render error"


            # Create Ernst job
            ernstJob = createNewJobHandle()
            apiCall(ILBCreateErnstJob(bmh, "ErnstJob", scene, beastConfig, ernstJob))
            targetManager.create(ernstJob)

            # Run Ernst
            apiCall(ILBStartJob(ernstJob, ILB_SR_CLOSE_WHEN_DONE, ILB_RD_AUTODETECT))

            isRunning = ILBBool(True)
            while isRunning.value:
                apiCall(ILBWaitJobDone(ernstJob, sys.maxsize))

                while True:
                    #ILBJobUpdateHandle uh;
                    uh = createNewJobUpdateHandle()
                    #ILBBool hasUpdate;
                    hasUpdate = ILBBool(False)

                    apiCall(ILBGetJobUpdate(ernstJob, hasUpdate, uh))
                    if hasUpdate.value == False:
                        break

                    # Update the scene with changes from Ernst
                    updateType = createNewUpdateType()
                    apiCall(ILBGetJobUpdateType(uh, updateType))
                    print "get job update type = " + str(updateType.value)
                    if updateType.value == ILB_UT_NEW_LIGHTSOURCE:
                        lh = createNewLightHandle()
                        apiCall(ILBGetUpdateLightSource(uh, lh))
                        lightManager.addLight(getLightFromHandle(lh))
                    elif updateType.value == ILB_UT_UPDATE_LIGHTSOURCE:
                        lh = createNewLightHandle()
                        apiCall(ILBGetUpdateLightSource(uh, lh))
                        lightManager.addLight(getLightFromHandle(lh))
                    elif updateType.value == ILB_UT_DELETE_LIGHTSOURCE:
                        lh = createNewLightHandle()
                        apiCall(ILBGetUpdateLightSource(uh, lh))
                        sh = createNewStringHandle()
                        apiCall(ILBGetLightName(lh, sh))
                        lightManager.deleteLight(convertStringHandle(sh))
                    elif updateType.value == ILB_UT_UPDATE_CAMERA:
                        ch = createNewCameraHandle()
                        apiCall(ILBGetUpdateCamera(uh, ch))
                        perspCamera = getCameraFromHandle(ch)
                    elif updateType.value == ILB_UT_SCENE_INFO:
                        sceneInfo = createNewSceneInfoHandle()
                        apiCall(ILBGetUpdateSceneInfo(uh, sceneInfo))
                        ss = ILBFloat()
                        apiCall(ILBGetMeterPerWorldUnit(sceneInfo, ss))
                        uv = createNewSceneUpVector()
                        apiCall(ILBGetSceneUpVector(sceneInfo, uv))
                        sceneScale = ss.value
                        sceneUpVector = uv.value
                    elif updateType.value == ILB_UT_UPDATE_TARGET:
                        te = createNewTargetEntityHandle()
                        apiCall(ILBGetUpdateTargetEntity(uh, te))
                        tt = createNewTargetEntityType()
                        apiCall(ILBGetTargetEntityType(te, tt))

                        sh = createNewStringHandle()
                        apiCall(ILBGetTargetEntityInstance(te, sh))
                        instanceName = convertStringHandle(sh)
                        width = height = ILBInt32()
                        if tt.value == ILB_TT_TEXTURE:
                            apiCall(ILBGetTargetEntityResolution(te, width, height))

                        print "new target entity = " + str(tt.value)
                        print "new width,height = " + str(width.value) + ", " + str(height.value)
                        targetManager.update(instanceName, tt, width.value, height.value)
                        

                    apiCall(ILBDestroyUpdate(uh))
                apiCall(ILBIsJobRunning(ernstJob, isRunning));

            apiCall(ILBDestroyJob(ernstJob));
            apiCall(ILBReleaseScene(scene));
            # end of create sceen loop

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

