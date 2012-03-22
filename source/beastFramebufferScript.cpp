#include "beastFramebufferScript.h"
#include "beastapi/beastframebuffer.h"

namespace bp = boost::python;
ILBStatus ILBGetChannelName_WrapperFn(ILBFramebufferHandleWrapper& _fb, 
																	  int32 _index,
																	  ILBStringHandleWrapper& _name)
{
	return ILBGetChannelName(_fb.getHandle(), _index, &(_name.getHandle()));
}
ILBStatus ILBGetChannelCount_WrapperFn(ILBFramebufferHandleWrapper _fb, ILBInt32Wrapper& _channels)
{
	return ILBGetChannelCount(_fb.getHandle(), &(_channels.m_value));
}
ILBStatus ILBGetResolution_WrapperFn(ILBFramebufferHandleWrapper& _fb, 
											ILBInt32Wrapper& _width,
											ILBInt32Wrapper& _height)
{
	return ILBGetResolution(_fb.getHandle(), &(_width.m_value), &(_height.m_value));
}
ILBStatus ILBReadRegionHDR_WrapperFn(ILBFramebufferHandleWrapper& _fb, 
											int32 _minX,
											int32 _minY,
											int32 _maxX,
											int32 _maxY,
											ILBChannelSelection _channels,
											std::vector<float>& _target)
{
	return ILBReadRegionHDR(_fb.getHandle(), _minX, _minY, _maxX, _maxY, _channels, &(_target[0]));
}

ILBStatus ILBReadRegionLDR_WrapperFn(ILBFramebufferHandleWrapper& _fb, 
									 int32 _minX,
									 int32 _minY,
									 int32 _maxX,
									 int32 _maxY,
									 ILBChannelSelection _channels,
									 float _gamma,
									 std::vector<unsigned char> _target)
{
	return ILBReadRegionLDR(_fb.getHandle(), _minX, _minY, _maxX, _maxY, _channels, _gamma, &(_target[0]));
}
ILBStatus ILBDestroyFramebuffer_WrapperFn(ILBFramebufferHandleWrapper& _fb)
{
	return ILBDestroyFramebuffer(_fb.getHandle());
}

void BeastFrameBufferInterface::registerInterface(boost::python::object& nspace) 
{
	bp::enum_< ILBChannelSelection>("ILBChannelSelection")
		.value("ILB_CS_R", ILB_CS_R)
		.value("ILB_CS_G", ILB_CS_G)
		.value("ILB_CS_B", ILB_CS_B)
		.value("ILB_CS_A", ILB_CS_A)
		.value("ILB_CS_Z", ILB_CS_Z)
		.value("ILB_CS_RGB", ILB_CS_RGB)
		.value("ILB_CS_RGBA", ILB_CS_RGBA)
		.value("ILB_CS_RGBAZ", ILB_CS_RGBAZ)
		.value("ILB_CS_ALL", ILB_CS_ALL)
		.export_values()
		;

	DECLARE_METHOD_BINDING(ILBGetChannelName)
	DECLARE_METHOD_BINDING(ILBGetChannelCount)
	DECLARE_METHOD_BINDING(ILBGetResolution)
	DECLARE_METHOD_BINDING(ILBReadRegionHDR)
	DECLARE_METHOD_BINDING(ILBReadRegionLDR)
	DECLARE_METHOD_BINDING(ILBDestroyFramebuffer)

}
