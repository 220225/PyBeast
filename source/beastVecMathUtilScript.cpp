#include "beastVecMathUtilScript.h"
#include "common/vecmath.h"
#include <boost/python.hpp>
#include "beastapi/beastapitypes.h"
namespace bp = boost::python;

void BeastVecMathUtilInterface::registerInterface(boost::python::object& nspace) 
{
	bp::class_<bex::ColorRGB>("ColorRGB", bp::no_init)
		.def(bp::init<float, float, float >(bp::args("self", "_r", "_g", "_b")))
		.def_readwrite("r", &bex::ColorRGB::r)
		.def_readwrite("g", &bex::ColorRGB::g)
		.def_readwrite("b", &bex::ColorRGB::b)
		;

	bp::class_<bex::ColorRGBA>("ColorRGBA", bp::init<>(bp::args("self")))
		.def(bp::init<float, float, float, float >(bp::args("self", "_r", "_g", "_b", "_a")))
		.def("toColorRGB", &bex::ColorRGBA::toColorRGB)
		.def_readwrite("r", &bex::ColorRGBA::r)
		.def_readwrite("g", &bex::ColorRGBA::g)
		.def_readwrite("b", &bex::ColorRGBA::b)
		.def_readwrite("a", &bex::ColorRGBA::a)
		;

	bp::class_<bex::Vec2>("Vec2", bp::init<>(bp::args("self")))
		.def(bp::init<float, float >(bp::args("self", "_x", "_y")))
		.def_readwrite("x", &bex::Vec2::x)
		.def_readwrite("y", &bex::Vec2::y)
		;

	bp::class_<bex::Vec3>("Vec3", bp::init<>(bp::args("self")))
		.def(bp::init<float, float, float >(bp::args("self", "_x", "_y", "_z")))
		.def(bp::self += bp::self)
		.def(bp::self + bp::self)
		.def(bp::self - bp::self)
		.def(bp::self * float())
		.def(-bp::self)
		.def_readwrite("x", &bex::Vec3::x)
		.def_readwrite("y", &bex::Vec3::y)
		.def_readwrite("z", &bex::Vec3::z)
		;

	bp::class_<bex::Matrix4x4>("Matrix4x4", bp::init<>(bp::args("self")))
		.def("setColumn", &bex::Matrix4x4::setColumn)
		.def("setRow", &bex::Matrix4x4::setRow)
		.def("getM", &bex::Matrix4x4::getM)
		.def("setM", &bex::Matrix4x4::setM)
		.def(bp::self * bp::self)
		;
}
