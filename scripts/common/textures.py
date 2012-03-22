from BeastPython.beastPython import *
from BeastPython.common.utils import *
import cmath
import math
import random

def copyVertexBuffer(_targetHandle, _passHandle, _entityHandle, _colorsArray):
    """docstring for copyVertexBuffer"""
    vertexBuffer = createNewFramebufferHandle()
    apiCall( ILBGetVertexbuffer(_targetHandle, _passHandle, _entityHandle, vertexBuffer) )

    channelCount = ILBInt32(0)
    apiCall( ILBGetChannelCount(vertexBuffer, channelCount) )

    width = ILBInt32(0)
    height = ILBInt32(0)
    apiCall( ILBGetResolution(vertexBuffer, width, height) )

    _colorsArray[:] = [rewrap_value_float(0.0)] * ( width.value * height.value * channelCount.value)
    apiCall( ILBReadRegionHDR(vertexBuffer, 0, 0, width.value, 1, ILB_CS_ALL, _colorsArray) )
    apiCall( ILBDestroyFramebuffer(vertexBuffer) )


def copyFrameBuffer(_bmh, _targetHandle, _passHandle, _textureName, _hdr):
    """docstring for copyFrameBuffer"""
    gamma = 2.2

    count = ILBInt32(0)
    apiCall( ILBGetFramebufferCount(_targetHandle, count) )

    frameBuffer = createNewFramebufferHandle()
    apiCall( ILBGetFramebuffer(_targetHandle, _passHandle, 0, frameBuffer) )

    width = ILBInt32(0)
    height = ILBInt32(0)
    apiCall( ILBGetResolution(frameBuffer, width, height) )

    lightMap = createNewTextureHandle()
    if _hdr == True:
        apiCall( ILBBeginTexture(_bmh, _textureName, width.value, height.value, ILB_PF_RGB_FLOAT, lightMap) )
        texture = FloatArray()
        texture[:] = [rewrap_value_float(0.0)] * (width.value * 3)
        for i in range(height.value):
            apiCall(ILBReadRegionHDR(frameBuffer, 0, height.value-i-1, width.value, height.value-i, ILB_CS_RGB, texture))
            apiCall(ILBAddPixelDataHDR(lightMap, texture, width.value))
    else:
        apiCall(ILBBeginTexture(_bmh, _textureName, width.value, height.value, ILB_PF_RGB_BYTE, lightMap))
        apiCall(ILBSetInputGamma(lightMap, ILB_IG_GAMMA, gamma))
        texture = UCharArray()
        texture[:] = [rewrap_value_unsigned_char(0)] * (width.value * 3)
        for i in range(height.value):
            apiCall(ILBReadRegionLDR(frameBuffer, 0, height.value-i-1, width.value, height.value-i, ILB_CS_RGB, gamma, texture))
            apiCall(ILBAddPixelDataLDR(lightMap, texture, width.value))

    apiCall(ILBEndTexture(lightMap))
    apiCall(ILBDestroyFramebuffer(frameBuffer))
    return lightMap


def mandelbort(j0, maxIter):
    """docstring for mandelbort"""
    j = complex(0.0, 0.0)
    for i in range(maxIter):
        j = j*j + j0
        absJ = abs(j)
        if absJ > 2.0:
            res = math.log(math.log(2.0))-math.log((math.log(absJ))) / math.log(2.0)
            return (i+res)/float(maxIter)

    return 1.0


def createMandelbrotTexture( _bm,  _texName, _baseColor, _width, _height):
    """docstring for createMandelbrotTexture"""
    tex = createNewTextureHandle()
    apiCall( ILBBeginTexture(_bm, _texName, _width, _height, ILB_PF_RGBA_FLOAT, tex) )

    componetns = 4
    iterations = 1000
    minU = -2.0
    maxU = 2.0
    minV = -1.0
    maxV = 1.0

    lineData = FloatArray()
    lineData[:] = [rewrap_value_float(0.0)] * (_width * componetns)
    for y in range(_height):
        for x in range(_width):
            localX = x*(maxU-minU)/(_width) + minU
            localY = y*(maxV-minV)/(_width) + minV

            c = complex(localX, localY)
            val = mandelbort(c, iterations)

            lineData[x*componetns] = rewrap_value_float(val * _baseColor.r)
            lineData[x*componetns + 1] = rewrap_value_float(val * _baseColor.g)
            lineData[x*componetns + 2] = rewrap_value_float(val * _baseColor.b)
            lineData[x*componetns + 3] = 1.0

        apiCall( ILBAddPixelDataHDR(tex, lineData, _width) )

    apiCall( ILBEndTexture(tex) )
    return tex

def createXorTexture(_bm, _name, _baseColor):
    """docstring for createXorTexture"""
    tex = createNewTextureHandle()
    width = 256
    height = 256
    checkerSize = 31

    apiCall( ILBBeginTexture(_bm, _name, width, height, ILB_PF_RGBA_BYTE, tex) )
    componetns = 4

    apiCall( ILBSetInputGamma(tex, ILB_IG_GAMMA, 2.2) )
    lineData = UCharArray()
    lineData[:] = [rewrap_value_unsigned_char(0)] * (width * componetns)

    for y in range(height):
        for x in range(width):
            valLdr = ((x^y) & 0xff)
            val = valLdr / 255.0
            checker = ((y&checkerSize) > checkerSize/2) ^ ((x&checkerSize) > checkerSize/2)

            lineData[x*componetns] = rewrap_value_unsigned_char( int(val* 255.0 * _baseColor.r) )
            lineData[x*componetns + 1] = rewrap_value_unsigned_char(int(val* 255.0 * _baseColor.g) )
            lineData[x*componetns + 2] = rewrap_value_unsigned_char(int(val* 255.0 * _baseColor.b) )
            lineData[x*componetns + 3] = rewrap_value_unsigned_char(255 * checker)

        apiCall( ILBAddPixelDataLDR(tex, lineData, width) )

    apiCall( ILBEndTexture(tex) )
    return tex


def createTestColorTexutre(_bm, _name):
    """docstring for createTestColorTexutre"""
    tex = createNewTextureHandle()
    width = 256
    height = 256

    apiCall( ILBBeginTexture(_bm, _name, width, height, ILB_PF_RGBA_BYTE, tex) )
    componetns = 4

    apiCall( ILBSetInputGamma(tex, ILB_IG_GAMMA, 2.2) )
    lineData = UCharArray()
    lineData[:] = [rewrap_value_unsigned_char(0)] * (width * componetns)

    for y in range(height):
        for x in range(width):
            lr = x > (width/2)
            ud = y > (height/2)
            r = g = b = rewrap_value_unsigned_char(0)

            if lr == True:
                if ud == True:
                    r = rewrap_value_unsigned_char(255)
                else:
                    g = rewrap_value_unsigned_char(255)
            else:
                if ud == True:
                    b = rewrap_value_unsigned_char(255)
                else:
                    r = g = rewrap_value_unsigned_char(255)

            lineData[x*componetns] = r
            lineData[x*componetns + 1] = g
            lineData[x*componetns + 2] = b
            lineData[x*componetns + 3] = rewrap_value_unsigned_char(255)

        apiCall( ILBAddPixelDataLDR(tex, lineData, width) )

    apiCall( ILBEndTexture(tex) )
    return tex
