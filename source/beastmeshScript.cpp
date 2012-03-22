#include <vector>

#include "beastmeshScript.h"
#include "beastapi\beastmesh.h"
using namespace boost::python;

ILBStatus ILBBeginMesh_WrapperFn(ILBManagerHandleWrapper& _beastManager, 
								 ILBConstString _uniqueName, 
								 ILBMeshHandleWrapper& _targetMesh)
{
	return ILBBeginMesh(_beastManager.getHandle(), _uniqueName, &(_targetMesh.getHandle()));
}

ILBStatus ILBEndMesh_WrapperFn(ILBMeshHandleWrapper& _mesh)
{
	return ILBEndMesh(_mesh.getHandle());
}


ILBStatus ILBAddVertexData_WrapperFn(ILBMeshHandleWrapper& _mesh, 
									 std::vector<bex::Vec3>& _vertexData, 
									 std::vector<bex::Vec3>& _normalData, 
									 int32 _vertexCount)
{
	return ILBAddVertexData(_mesh.getHandle(), &_vertexData[0], &_normalData[0], _vertexCount);
}

ILBStatus ILBBeginMaterialGroup_WrapperFn(ILBMeshHandleWrapper& _mesh, 
								ILBConstString materialName)
{
	return ILBBeginMaterialGroup(_mesh.getHandle(), materialName);
}
ILBStatus ILBEndMaterialGroup_WrapperFn(ILBMeshHandleWrapper& _mesh)
{
	return ILBEndMaterialGroup(_mesh.getHandle());
}

ILBStatus ILBAddTriangleData_WrapperFn(ILBMeshHandleWrapper& _mesh,
									   std::vector<int32> _indexData, 
									   int32 indexCount)
{
	return ILBAddTriangleData(_mesh.getHandle(), &_indexData[0], indexCount);
}

ILBStatus ILBBeginUVLayer_WrapperFn(ILBMeshHandleWrapper& _mesh,
									ILBConstString _layerName)
{
	return ILBBeginUVLayer(_mesh.getHandle(), _layerName);
}

ILBStatus ILBEndUVLayer_WrapperFn(ILBMeshHandleWrapper& _mesh)
{
	return ILBEndUVLayer(_mesh.getHandle());
}

ILBStatus ILBAddUVData_WrapperFn(ILBMeshHandleWrapper& _mesh, 
								 std::vector<bex::Vec2>& _uvData, 
								 int32 _count)
{
	return ILBAddUVData(_mesh.getHandle(), &_uvData[0], _count);
}


ILBStatus ILBBeginColorLayer_WrapperFn(ILBMeshHandleWrapper& _mesh,
									   ILBConstString _layerName)
{
	return ILBBeginColorLayer(_mesh.getHandle(), _layerName);
}

ILBStatus ILBEndColorLayer_WrapperFn(ILBMeshHandleWrapper& _mesh)
{
	return ILBEndColorLayer(_mesh.getHandle());
}

ILBStatus ILBAddColorData_WrapperFn(ILBMeshHandleWrapper& _mesh, 
								    std::vector<bex::ColorRGBA>& _colorData, 
									int32 _count)
{
	return ILBAddColorData(_mesh.getHandle(), &_colorData[0], _count);
}

ILBStatus ILBBeginTangents_WrapperFn(ILBMeshHandleWrapper& _mesh)
{
	return ILBBeginTangents(_mesh.getHandle());
}
ILBStatus ILBEndTangents_WrapperFn(ILBMeshHandleWrapper& _mesh)
{
	return ILBEndTangents(_mesh.getHandle());
}
ILBStatus ILBAddTangentData_WrapperFn(ILBMeshHandleWrapper _mesh, 
																	std::vector<bex::Vec3> _tangentData, 
																	std::vector<bex::Vec3> _bitangentData, 
																	int32 _count)
{
	return ILBAddTangentData(_mesh.getHandle(), &_tangentData[0], &_bitangentData[0], _count);
}

ILBStatus ILBFindMesh_WrapperFn(ILBManagerHandleWrapper& _beastManager,
								   ILBConstString _uniqueName,
								   ILBMeshHandleWrapper& _target)
{
	return ILBFindMesh(_beastManager.getHandle(), _uniqueName, &(_target.getHandle()));
}
void BeastMeshInterface::registerInterface(boost::python::object& nspace) 
{
	DECLARE_METHOD_BINDING(ILBBeginMesh)
	DECLARE_METHOD_BINDING(ILBEndMesh)
	DECLARE_METHOD_BINDING(ILBAddVertexData)
	DECLARE_METHOD_BINDING(ILBBeginMaterialGroup)
	DECLARE_METHOD_BINDING(ILBEndMaterialGroup)
	DECLARE_METHOD_BINDING(ILBAddTriangleData)
	DECLARE_METHOD_BINDING(ILBBeginUVLayer)
	DECLARE_METHOD_BINDING(ILBEndUVLayer)
	DECLARE_METHOD_BINDING(ILBAddVertexData)
	DECLARE_METHOD_BINDING(ILBAddUVData)
	DECLARE_METHOD_BINDING(ILBBeginColorLayer)
	DECLARE_METHOD_BINDING(ILBEndColorLayer)
	DECLARE_METHOD_BINDING(ILBAddColorData)
	DECLARE_METHOD_BINDING(ILBBeginTangents)
	DECLARE_METHOD_BINDING(ILBEndTangents)
	DECLARE_METHOD_BINDING(ILBAddTangentData)
	DECLARE_METHOD_BINDING(ILBFindMesh)

}
