#include "beastVecMathUtilScript.h"
#include "common\vecmath.h"

namespace bp = boost::python;
void BeastVecMathUtilInterface::registerInterface(boost::python::object& nspace) 
{
	class_<bex::ColorRGB>("ColorRGB", no_init)
		.def(init<float, float, float >(args("self", "_r", "_g", "_b")))
		.def_readwrite("r", &bex::ColorRGB::r)
		.def_readwrite("g", &bex::ColorRGB::g)
		.def_readwrite("b", &bex::ColorRGB::b)
		;

	class_<bex::ColorRGBA>("ColorRGBA", init<>(args("self")))
		.def(init<float, float, float, float >(args("self", "_r", "_g", "_b", "_a")))
		.def("toColorRGB", &bex::ColorRGBA::toColorRGB)
		.def_readwrite("r", &bex::ColorRGBA::r)
		.def_readwrite("g", &bex::ColorRGBA::g)
		.def_readwrite("b", &bex::ColorRGBA::b)
		.def_readwrite("a", &bex::ColorRGBA::a)
		;

	class_<bex::Vec2>("Vec2", init<>(args("self")))
		.def(init<float, float >(args("self", "_x", "_y")))
		.def_readwrite("x", &bex::Vec2::x)
		.def_readwrite("y", &bex::Vec2::y)
		;

	class_<bex::Vec3>("Vec3", init<>(args("self")))
		.def(init<float, float, float >(args("self", "_x", "_y", "_z")))
		.def(self += self)
		.def(self + self)
		.def(self - self)
		.def(self * float())
		.def(-self)
		.def_readwrite("x", &bex::Vec3::x)
		.def_readwrite("y", &bex::Vec3::y)
		.def_readwrite("z", &bex::Vec3::z)
		;

	class_<bex::Matrix4x4>("Matrix4x4", init<>(args("self")))
		.def("setColumn", &bex::Matrix4x4::setColumn)
		.def("setRow", &bex::Matrix4x4::setRow)
		.def("getM", &bex::Matrix4x4::getM)
		.def("setM", &bex::Matrix4x4::setM)
		.def(self * self)
		;
}
