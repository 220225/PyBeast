#include "beastapitypesScript.h"
#include "beasttextureScript.h"
#include <beastapi/beasttexture.h>
#include <boost/python.hpp>
namespace bp = boost::python;

ILBStatus ILBBeginTexture_WrapperFn(ILBManagerHandleWrapper& _beastManager,
								   ILBConstString _uniqueName,
								   int32 _width,
								   int32 _height,
								   ILBPixelFormat _inputFormat,
								   ILBTextureHandleWrapper& _target)
{
	return ILBBeginTexture( _beastManager.getHandle(), _uniqueName, _width, _height, _inputFormat, &(_target.getHandle()) );
}
ILBStatus ILBEndTexture_WrapperFn(ILBTextureHandleWrapper& _target)
{
	return ILBEndTexture( _target.getHandle() );
}
ILBStatus ILBSetInputGamma_WrapperFn(ILBTextureHandleWrapper& _texture,
																   ILBImageGammaType _type, 
																   float _gamma)
{
	 return ILBSetInputGamma(_texture.getHandle(), _type, _gamma);
}
ILBStatus ILBAddPixelDataLDR_WrapperFn(ILBTextureHandleWrapper& _texture,
												  std::vector<unsigned char>& _data,
												  int32 _pixelCount)
{
	return ILBAddPixelDataLDR(_texture.getHandle(), &_data[0], _pixelCount);
}

ILBStatus ILBAddPixelDataHDR_WrapperFn(ILBTextureHandleWrapper& _texture,
											  std::vector<float>& _data,
											  int32 _pixelCount)
{
	return ILBAddPixelDataHDR(_texture.getHandle(), &_data[0], _pixelCount);

}


ILBStatus ILBFindTexture_WrapperFn(ILBManagerHandleWrapper& _beastManager,
										  ILBConstString _uniqueName,
										  ILBTextureHandleWrapper& _target)
{
	return ILBFindTexture(_beastManager.getHandle(), _uniqueName, &(_target.getHandle()));
}

void BeastTextureInterface::registerInterface(boost::python::object& nspace) 
{
	bp::enum_< ILBPixelFormat>("ILBPixelFormat")
		.value("ILB_PF_MONO_FLOAT", ILB_PF_MONO_FLOAT)
		.value("ILB_PF_RGB_FLOAT", ILB_PF_RGB_FLOAT)
		.value("ILB_PF_RGBA_FLOAT", ILB_PF_RGBA_FLOAT)
		.value("ILB_PF_MONO_BYTE", ILB_PF_MONO_BYTE)
		.value("ILB_PF_RGB_BYTE", ILB_PF_RGB_BYTE)
		.value("ILB_PF_RGBA_BYTE", ILB_PF_RGBA_BYTE)
		.export_values()
		;
	bp::enum_< ILBImageGammaType>("ILBImageGammaType")
		.value("ILB_IG_GAMMA", ILB_IG_GAMMA)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBBeginTexture)
	DECLARE_METHOD_BINDING(ILBEndTexture)
	DECLARE_METHOD_BINDING(ILBSetInputGamma)
	DECLARE_METHOD_BINDING(ILBAddPixelDataLDR)
	DECLARE_METHOD_BINDING(ILBAddPixelDataHDR)
	DECLARE_METHOD_BINDING(ILBFindTexture)
}
