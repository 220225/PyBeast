from BeastPython.beastPython import *
from BeastPython.common import vecmath
from BeastPython.common.utils import *

import math

def createPointCloudGrid(_scene, _name, _minCorner, _maxCorner, _count):
    """docstring for createPointCloudGrid"""

    if _count < 2:
        return 0

    pch = createNewPointCloudHandle()
    apiCall( ILBCreatePointCloud(_scene, _name, pch) )

    normals = Vec3Array()
    normals[:] = [Vec3(1, 0, 0)] * _count

    sideLength = Vec3(_maxCorner.x-_minCorner.x, _maxCorner.y-_minCorner.y, _maxCorner.z-_minCorner.z)

    for z in range(_count):
        for y in range(_count):
            points = Vec3Array()
            points[:] = [Vec3()]*_count
            for x in range(_count):
                xx = _minCorner.x + sideLength.x * (x/(_count-1.0))
                yy = _minCorner.y + sideLength.y * (y/(_count-1.0))
                zz = _minCorner.z + sideLength.z * (z/(_count-1.0))
                points.append(Vec3(xx, yy, zz))
            apiCall( ILBAddPointCloudData(pch, points, normals, _count) )

    apiCall( ILBEndPointCloud(pch) )
    return pch



def createCornellBox(_bmh, _name, _materialName):
    """docstring for createCornellBox"""
    mesh = createNewMeshHandle()
    apiCall( ILBBeginMesh(_bmh, _name, mesh) )

    A = Vec3(-1, -1, -1)
    B = Vec3(-1, -1,  1)
    C = Vec3( 1, -1,  1)
    D = Vec3( 1, -1, -1)
    E = Vec3(-1,  1, -1)
    F = Vec3( 1,  1, -1)
    G = Vec3( 1,  1,  1)
    H = Vec3(-1,  1,  1)

    UVD = Vec2(0.0, 0.0)
    UVC = Vec2(1.0/3.0, 0.0)
    UVB = Vec2(2.0/3.0, 0.0)
    UVA = Vec2(1.0, 0.0)

    UVH = Vec2(0.0, 1.0/3.0)
    UVG = Vec2(1.0/3.0, 1.0/3.0)
    UVF = Vec2(2.0/3.0, 1.0/3.0)
    UVE = Vec2(1.0, 1.0/3.0)

    UVL = Vec2(0.0, 2.0/3.0)
    UVK = Vec2(1.0/3.0, 2.0/3.0)
    UVJ = Vec2(2.0/3.0, 2.0/3.0)
    UVI = Vec2(1.0, 2.0/3.0)

    red = ColorRGBA(0.7, 0.0, 0.0, 1.0)
    blue = ColorRGBA(0.0, 0.0, 0.7, 1.0)
    white = ColorRGBA(0.7, 0.7, 0.7, 1.0)

    vertexCount = 20

    positions = Vec3Array()
    normals = Vec3Array()
    colors = ColorRGBAArray()
    uv = Vec2Array()
    tangents = Vec3Array()
    bitangents = Vec3Array()

    positions.append(A)
    positions.append(B)
    positions.append(C)
    positions.append(D)

    uv.append(UVA)
    uv.append(UVB)
    uv.append(UVF)
    uv.append(UVE)

    for i in range(4):
        normal = Vec3(0.0, 1.0, 0.0)
        normals.append(normal)
    for i in range(4):
        colors.append(white)
    for i in range(4):
        tangent = Vec3(1.0, 0.0, 0.0)
        tangents.append(tangent)
    for i in range(4):
        bitangent = Vec3(0, 0, -1)
        bitangents.append(bitangent)

    # Face 2, ceiling
    positions.append(E)
    positions.append(F)
    positions.append(G)
    positions.append(H)
    uv.append(UVB)
    uv.append(UVC)
    uv.append(UVG)
    uv.append(UVF)

    for i in range(4):
        normal = Vec3(0.0, -1.0, 0.0)
        normals.append(normal)
    for i in range(4):
        colors.append(white)
    for i in range(4):
        tangent = Vec3(1.0, 0.0, 0.0)
        tangents.append(tangent)
    for i in range(4):
        bitangent = Vec3(0, 0, 1)
        bitangents.append(bitangent)


    # Face 3, back wall
    positions.append(H)
    positions.append(G)
    positions.append(C)
    positions.append(B)
    uv.append(UVC)
    uv.append(UVD)
    uv.append(UVH)
    uv.append(UVG)

    for i in range(4):
        normal = Vec3(0.0, 0.0, -1.0)
        normals.append(normal)
    for i in range(4):
        colors.append(white)
    for i in range(4):
        tangent = Vec3(1.0, 0.0, 0.0)
        tangents.append(tangent)
    for i in range(4):
        bitangent = Vec3(0.0, -1.0, 0.0)
        bitangents.append(bitangent)


    # Face 4, left wall
    positions.append(E)
    positions.append(H)
    positions.append(B)
    positions.append(A)
    uv.append(UVE)
    uv.append(UVF)
    uv.append(UVJ)
    uv.append(UVI)

    for i in range(4):
        normal = Vec3(1.0, 0.0, 0.0)
        normals.append(normal)
    for i in range(4):
        colors.append(red)
    for i in range(4):
        tangent = Vec3(0.0, 0.0, 1.0)
        tangents.append(tangent)
    for i in range(4):
        bitangent = Vec3(0.0, -1.0, 0.0)
        bitangents.append(bitangent)


    # Face 5, right wall
    positions.append(G)
    positions.append(F)
    positions.append(D)
    positions.append(C)
    uv.append(UVF)
    uv.append(UVG)
    uv.append(UVK)
    uv.append(UVJ)

    for i in range(4):
        normal = Vec3(-1.0, 0.0, 0.0)
        normals.append(normal)
    for i in range(4):
        colors.append(blue)
    for i in range(4):
        tangent = Vec3(0.0, 0.0, -1.0)
        tangents.append(tangent)
    for i in range(4):
        bitangent = Vec3(0.0, -1.0, 0.0)
        bitangents.append(bitangent)

    tris = Int32Array()
    for i in range(5):
        base = i * 4
        tris.append(base+0)
        tris.append(base+1)
        tris.append(base+2)

        tris.append(base+2)
        tris.append(base+3)
        tris.append(base+0)
    apiCall( ILBAddVertexData(mesh, positions, normals, vertexCount) )

    
    apiCall( ILBBeginMaterialGroup(mesh, _materialName) )
    apiCall( ILBAddTriangleData(mesh, tris, len(tris)) )
    apiCall( ILBEndMaterialGroup(mesh) )

    # Add uv layer
    apiCall( ILBBeginUVLayer(mesh, "uv1") )
    apiCall( ILBAddUVData(mesh, uv, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    apiCall( ILBBeginColorLayer(mesh, "colors") )
    apiCall( ILBAddColorData(mesh, colors, vertexCount) )
    apiCall( ILBEndColorLayer(mesh) )

    # Add tangent layer
    apiCall( ILBBeginTangents(mesh) )
    apiCall( ILBAddTangentData(mesh, tangents, bitangents, vertexCount) )
    apiCall( ILBEndTangents(mesh) )

    apiCall( ILBEndMesh(mesh) )
    return mesh

def createPlaneVertices(_xres, _yres):
    """docstring for createPlaneVertices"""
    vertexCount = _xres * _yres
    vertices = Vec3Array()
    vertices[:] = [Vec3()] * vertexCount
    vertexIndex = 0

    x_rcp = 2.0/(_xres-1.0)
    y_rcp = 2.0/(_yres-1.0)
    for y in range(_yres):
        yp = y * y_rcp-1.0
        for x in range(_xres):
            xp = x * x_rcp - 1.0
            vertices[vertexIndex] = Vec3(xp, 0.0, yp)
            vertexIndex += 1
    return vertices

def createPlane( _bm, _name, _materialName, _xres, _yres, _colors = None ):
    """docstring for createPlane"""
    mesh = createNewMeshHandle()
    apiCall( ILBBeginMesh( _bm, _name, mesh ) )

    vertexCount = _xres * _yres
    triangleCount = (_xres-1) * (_yres-1) * 2

    normal = Vec3(0.0, 1.0, 0.0)
    tangent = Vec3(1.0, 0.0, 0.0)
    bitangent = Vec3(0.0, 0.0, -1.0)

    normals = Vec3Array()
    normals[:] = [normal] * vertexCount
    tris = Int32Array()
    tris[:] = [0] * triangleCount * 3

    uvData = Vec2Array()
    uvData[:] = [Vec2()] * vertexCount
    tangents = Vec3Array()
    tangents[:] = [tangent] * vertexCount
    bitangents = Vec3Array()
    bitangents[:] = [bitangent] * vertexCount

    vertexIndex = 0
    triangleIndex = 0

    positions = createPlaneVertices(_xres, _yres)

    for y in range(_yres):
        for x in range(_xres):
            uvData[vertexIndex] = Vec2(positions[vertexIndex].x*0.5+0.5, positions[vertexIndex].z*0.5+0.5)
            vertexIndex += 1
            if x != _xres-1 and y != _yres-1:
                indexV1 = y*_xres + x
                indexV2 = y*_xres + x + 1
                indexV3 = y*_xres + x + _xres
                indexV4 = y*_xres + x + _xres + 1
                tris[triangleIndex] = indexV1
                triangleIndex += 1
                tris[triangleIndex] = indexV4
                triangleIndex += 1
                tris[triangleIndex] = indexV2
                triangleIndex += 1

                tris[triangleIndex] = indexV1
                triangleIndex += 1
                tris[triangleIndex] = indexV3
                triangleIndex += 1
                tris[triangleIndex] = indexV4
                triangleIndex += 1


    apiCall( ILBAddVertexData(mesh, positions, normals, vertexCount) )

    apiCall( ILBBeginMaterialGroup(mesh, _materialName) )
    apiCall( ILBAddTriangleData(mesh, tris, len(tris)) )
    apiCall( ILBEndMaterialGroup(mesh) )

    # Add uv layer
    apiCall( ILBBeginUVLayer(mesh, "uv1") )
    apiCall( ILBAddUVData(mesh, uvData, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    # Add tangent layer
    apiCall( ILBBeginTangents(mesh) )
    apiCall( ILBAddTangentData(mesh, tangents, bitangents, vertexCount) )
    apiCall( ILBEndTangents(mesh) )

    # Add colors
    if (_colors != None and len(_colors) == vertexCount*4):
        colors = convertFloatArrayToColorRGBArray(_colors)

        apiCall( ILBBeginColorLayer(mesh, "colors") )
        apiCall( ILBAddColorData(mesh, colors, vertexCount) )
        apiCall( ILBEndColorLayer(mesh) )

    apiCall( ILBEndMesh(mesh) )
    return mesh

def createPlaneMultiUV(_bm, _name, _materialName):
    """docstring for createPlaneMultiUV"""
    mesh = createNewMeshHandle()
    apiCall( ILBBeginMesh( _bm, _name, mesh ) )

    vertexCount = 4

    normal = Vec3(0.0, 1.0, 0.0)
    positions = Vec3Array()
    positions[:] = [Vec3()]*vertexCount
    normals = Vec3Array()
    normals[:] = [normal] * vertexCount
    for i in range(vertexCount):
        x = -1.0 if i<2 else 1.0
        z = 1.0 if i==1 or i == 2 else -1.0
        positions[i] = Vec3(x, 0.0, z)

    apiCall( ILBAddVertexData(mesh, positions, normals, vertexCount) )

    apiCall( ILBBeginMaterialGroup(mesh, _materialName) )
    tris = Int32Array()
    tris[:] = [0, 1, 2, 0, 2, 3]
    apiCall( ILBAddTriangleData(mesh, tris, len(tris)) ) 

    apiCall( ILBEndMaterialGroup(mesh) )

    uvData1 = Vec2Array()
    uvData1[:] = [Vec2()] * vertexCount
    uvData2 = Vec2Array()
    uvData2[:] = [Vec2()] * vertexCount
    uvData3 = Vec2Array()
    uvData3[:] = [Vec2()] * vertexCount
    uvData4 = Vec2Array()
    uvData4[:] = [Vec2()] * vertexCount

    tangents = Vec3Array()
    tangents[:] = [Vec3()] * vertexCount
    bitangents = Vec3Array()
    bitangents[:] = [Vec3()] * vertexCount

    for i in range(vertexCount):
        idx = i & 3
        u = 0.0 if idx<2 else 0.5
        v = 0.0 if idx==1 or idx==2 else 0.5
        uvData1[i] = Vec2(u, v)
        uvData2[i] = Vec2(u+0.5, v)
        uvData3[i] = Vec2(u, v+0.5)
        uvData4[i] = Vec2(u+0.5, v+0.5)

        tangents[i] = Vec3(1.0, 0.0, 0.0)
        bitangents[i] = Vec3(0.0, 0.0, -1.0)

    # Add first UV layer and data
    apiCall( ILBBeginUVLayer(mesh, 'uv1') )
    apiCall( ILBAddUVData(mesh, uvData1, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    # Add second UV layer and data
    apiCall( ILBBeginUVLayer(mesh, 'uv2') )
    apiCall( ILBAddUVData(mesh, uvData2, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    # Add third UV layer and data
    apiCall( ILBBeginUVLayer(mesh, 'uv3') )
    apiCall( ILBAddUVData(mesh, uvData3, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    # Add fourth UV layer and data
    apiCall( ILBBeginUVLayer(mesh, 'uv4') )
    apiCall( ILBAddUVData(mesh, uvData4, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    # Add tangent layer
    apiCall( ILBBeginTangents(mesh) )
    # Add tangent data
    apiCall( ILBAddTangentData(mesh, tangents, bitangents, vertexCount) )
    apiCall( ILBEndTangents(mesh) )

    apiCall( ILBEndMesh(mesh) )
    return mesh

    pass
def createPlaneSimple( _bm, _name, _materialName ):
    """docstring for createPlaneSimple"""
    mesh = createNewMeshHandle()
    apiCall( ILBBeginMesh( _bm, _name, mesh ) )

    vertexCount = 4

    normal = Vec3(0.0, 1.0, 0.0)
    positions = Vec3Array()
    positions[:] = [Vec3()]*vertexCount
    normals = Vec3Array()
    normals[:] = [normal] * vertexCount
    for i in range(vertexCount):
        x = -1.0 if i<2 else 1.0
        z = 1.0 if i==1 or i == 2 else -1.0
        positions[i] = Vec3(x, 0.0, z)
        #positions.append( Vec3(x, 0.0, z) )

    apiCall( ILBAddVertexData(mesh, positions, normals, vertexCount) )

    apiCall( ILBBeginMaterialGroup(mesh, _materialName) )
    tris = Int32Array()
    tris[:] = [0, 1, 2, 0, 2, 3]
    apiCall( ILBAddTriangleData(mesh, tris, len(tris)) ) 

    apiCall( ILBEndMaterialGroup(mesh) )

    uvData = Vec2Array()
    uvData[:] = [Vec2()] * vertexCount
    tangents = Vec3Array()
    tangents[:] = [Vec3()] * vertexCount
    bitangents = Vec3Array()
    bitangents[:] = [Vec3()] * vertexCount

    for i in range(vertexCount):
        idx = i & 3
        u = 0.0 if idx<2 else 1.0
        v = 1.0 if idx==1 or idx==2 else 0.0
        uvData[i] = Vec2(u, v)
        tangents[i] = Vec3(1.0, 0.0, 0.0)
        bitangents[i] = Vec3(0.0, 0.0, -1.0)

    # Add UV layer and data
    apiCall( ILBBeginUVLayer(mesh, 'uv1') )
    apiCall( ILBAddUVData(mesh, uvData, vertexCount) )
    apiCall( ILBEndUVLayer(mesh) )

    # Add tangent layer
    apiCall( ILBBeginTangents(mesh) )
    # Add tangent data
    apiCall( ILBAddTangentData(mesh, tangents, bitangents, vertexCount) )
    apiCall( ILBEndTangents(mesh) )

    apiCall( ILBEndMesh(mesh) )
    return mesh


def createSphere( _bm, _name, _materialName, _segmentsU, _segmentsV, _colors = None ):
    mesh = createNewMeshHandle()
    apiCall( ILBBeginMesh(_bm, _name, mesh) )

    PI = 3.141592
    if _segmentsV < 3 or _segmentsU < 3 :
        raise Exception, "Invalid segment setup"

    for v in range(_segmentsV):
        angleTh = (v/(_segmentsV - 1.0)) * PI
        positions = Vec3Array()
        normals = Vec3Array()
        for u in range(_segmentsU):
            anglePh = (u*2.0*PI/_segmentsU)
            x = math.cos(anglePh) * math.sin(angleTh)
            y = math.cos(angleTh)
            z = math.sin(anglePh) * math.sin(angleTh)

            positions.append(Vec3(x,y,z))
            normals.append(vecmath.normalize(Vec3(x,y,z)))

        apiCall( ILBAddVertexData(mesh, positions, normals, len(positions)) )

    
    apiCall( ILBBeginMaterialGroup(mesh, _materialName) )
    for v in range(_segmentsV-1):
        indices = Int32Array()

        for u in range(_segmentsU):
            lineStride = _segmentsV - 1
            a = u + v * _segmentsU
            b = (u + 1) % _segmentsU + v * _segmentsU
            c = (u + 1) % _segmentsU + (v + 1) * _segmentsU
            d = u + (v + 1) * _segmentsU
            indices.append(a)
            indices.append(b)
            indices.append(c)

            indices.append(a)
            indices.append(c)
            indices.append(d)

        apiCall( ILBAddTriangleData(mesh, indices, len(indices)) )

    apiCall( ILBEndMaterialGroup(mesh) )

    # Add uv's
    apiCall( ILBBeginUVLayer(mesh, 'uv1') )
    for v in range(_segmentsV):
        uvs = Vec2Array()
        for u in range(_segmentsU):
            uvs.append(Vec2( u/float(_segmentsU), v/float(_segmentsV)))
        apiCall( ILBAddUVData(mesh, uvs, len(uvs)) )

    apiCall( ILBEndUVLayer(mesh) )

    # Add vertex colors
    apiCall( ILBBeginColorLayer(mesh, 'color1') )
    if _colors != None and len(_colors) == (_segmentsU * _segmentsV * 4) :
        colors = convertFloatArrayToColorRGBArray(_colors)
        apiCall( ILBAddColorData(mesh, colors, _segmentsU * _segmentsV) )
    else:
        randomColors = ColorRGBAArray()
        for v in range(_segmentsU * _segmentsV):
            randomColors.append(vecmath.randomRGBA(1.0))
        apiCall( ILBAddColorData(mesh, randomColors, _segmentsU * _segmentsV) )
        
    apiCall( ILBEndColorLayer(mesh) )
    apiCall( ILBEndMesh(mesh) )
    return mesh

class SHData:
    def __init__( self, _r, _g, _b ):
        self.r = _r
        self.g = _g
        self.b = _b

def convertFloatArrayToSHDataArray(_floatArray):
    if len(_floatArray) % 12 != 0:
        print "Error: array size must be able divide by 12 to convert to SHData array!!"
        return None

    SHDataArray = []
    for i in range(0, len(_floatArray), 12):
        r = (_floatArray[i], _floatArray[i+1], _floatArray[i+2], _floatArray[i+3])
        g = (_floatArray[i+4], _floatArray[i+5], _floatArray[i+6], _floatArray[i+7])
        b = (_floatArray[i+8], _floatArray[i+9], _floatArray[i+10], _floatArray[i+11])
        SHDataArray.append(SHData(r, g, b))

    return SHDataArray


def convertFloatArrayToColorRGBArray(_floatArray):
    if len(_floatArray) % 4 != 0:
        print "Error: array size must be able divide by 4!!"
        return []

    colorArray = ColorRGBAArray()
    for i in range(0, len(_floatArray), 4):
        r = _floatArray[i]
        g = _floatArray[i+1]
        b = _floatArray[i+2]
        a = _floatArray[i+3]
        colorArray.append(ColorRGBA(r, g, b, a))

    return colorArray

def convertFloatArrayToLDRColorRGBArray(_floatArray):
    if len(_floatArray) % 4 != 0:
        print "Error: array size must be able divide by 4!!"
        return []

    colorArray = ColorRGBAArray()
    maxValue = 0
    # pass 1, find the max value
    for i in range(0, len(_floatArray), 4):
        r = int(_floatArray[i] * 255)
        if r > 255 and r > maxValue:
            maxValue = r
        g = int(_floatArray[i+1] * 255)
        if g > 255 and g > maxValue:
            maxValue = g
        b = int(_floatArray[i+2] * 255)
        if b > 255 and b > maxValue:
            maxValue = b
        a = int(_floatArray[i+3] * 255)
        if a > 255 and a > maxValue:
            maxValue = a

    # pass 2, get the color array
    if maxValue > 255:
        multiplier = 255.0/maxValue
        for i in range(0, len(_floatArray), 4):
            r = int(_floatArray[i] * 255 * multiplier)
            g = int(_floatArray[i+1] * 255 * multiplier)
            b = int(_floatArray[i+2] * 255 * multiplier)
            a = int(_floatArray[i+3] * 255 * multiplier)

            colorArray.append(ColorRGBA(r, g, b, a))
    else:
        for i in range(0, len(_floatArray), 4):
            r = int(_floatArray[i] * 255)
            g = int(_floatArray[i+1] * 255)
            b = int(_floatArray[i+2] * 255)
            a = int(_floatArray[i+3] * 255)

            colorArray.append(ColorRGBA(r, g, b, a))

    return colorArray

