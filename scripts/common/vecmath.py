from BeastPython.beastPython import *
import math

def dot(v1, v2):
    """docstring for dot"""
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def normalize(v1):
    """docstring for normalize"""
    lenRec = 1.0 / math.sqrt(dot(v1, v1))
    return Vec3(v1.x * lenRec, v1.y * lenRec, v1.z * lenRec)

def randomRGBA(amp):
    """docstring for randomRGBA"""
    import random
    return ColorRGBA(random.random()*amp, random.random()*amp, random.random()*amp, random.random()*amp)

def identity():
    """docstring for identity"""
    result = Matrix4x4()
    for i in range(16):
        if i&3 == (i/4):
            result.setM(i, 1.0)
        else:
            result.setM(i, 0.0)
    return result

def translation(pos):
    """sets a translation matrix"""
    result = identity()
    result.setM(3, pos.x)
    result.setM(7, pos.y)
    result.setM(11, pos.z)
    return result

def scale(_scale):
    """docstring for scale"""
    result = identity()
    result.setM(0, _scale.x)
    result.setM(5, _scale.y)
    result.setM(10, _scale.z)
    return result

def scaleTranslation(_scale, _trans):
    """docstring for scaleTranslation"""
    return translation(_trans) * scale(_scale)

def cross(v1, v2):
    return Vec3(v1.y*v2.z - v1.z*v2.y, 
                v1.z*v2.x - v1.x*v2.z,
                v1.x*v2.y - v1.y*v2.x)

def smallestComponent(v):
    """docstring for smallestComponent"""
    x = math.fabs(v.x)
    y = math.fabs(v.y)
    z = math.fabs(v.z)
    if x < y and x < z:
        return Vec3(1.0, 0.0, 0.0)
    elif y < z:
        return Vec3(0.0, 1.0, 0.0)
    else:
        return Vec3(0.0, 0.0, 1.0)

def findOrtho(v):
    """docstring for findor"""
    return cross(smallestComponent(v), v)


def directionalLightOrientation(dir, upHint = None):
    """docstring for directionalLightOrientation"""
    _upHint = findOrtho(dir) if upHint == None else upHint

    proj = dot(dir, _upHint)
    if math.fabs( proj * proj - (dot(dir, dir) * dot(_upHint, _upHint)) ) < 0.001:
        raise Exception, "Up vector and forward vector parallel or close to parallel"

    x = normalize(cross(dir, _upHint))
    z = normalize(cross(dir, x))
    dir = normalize(dir)
    result = identity()
    result.setColumn(x, 0)
    result.setColumn(-dir, 1)
    result.setColumn(z, 2)
    return result

def setSpotlightMatrix(pos, forward, upHint = None):
    """docstring for setSpotlightMatrix"""
    _upHint = findOrtho(forward) if upHint == None else upHint

    trans = translation(pos)
    orient = directionalLightOrientation(forward, _upHint)
    return trans * orient

def setAreaLightMatrix(_pos, _forward,  _upHint, _scaling):
    """docstring for setAreaLightMatrix"""
    scalemtx = scale(Vec3(_scaling.x, 1.0, _scaling.y))
    return setSpotlightMatrix(_pos, _forward, _upHint) * scalemtx


def cameraOrientation(_forward, _upHint):
    """docstring for cameraOrientation"""
    proj = dot(_forward, _upHint)
    if math.fabs( proj * proj - (dot(_forward, _forward) * dot(_upHint, _upHint)) ) < 0.001:
        raise Exception, "Up vector and forward vector parallel or close to parallel"

    right = normalize(cross(_upHint, _forward))
    up = normalize(cross(_forward, right))
    _forward = normalize(_forward)
    result = identity()
    result.setColumn(-right, 0)
    result.setColumn(up, 1)
    result.setColumn(-_forward, 2)
    return result

def setCameraMatrix(_pos, _forward, _upHint):
    """docstring for setCameraMatrix"""
    trans = translation(_pos)
    orient = cameraOrientation(_forward, _upHint)
    return trans * orient
