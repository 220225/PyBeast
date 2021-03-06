INCLUDE_DIRECTORIES(${PyBeast_SOURCE_DIR}/include) 

# boost section
SET(Boost_USE_STATIC_LIBS ON)
SET(Boost_USE_MULTITHREADED ON)
FIND_PACKAGE(Boost COMPONENTS
				python
			 REQUIRED)

MESSAGE("Include dirs of boost: " ${Boost_INCLUDE_DIRS} )
MESSAGE("Libs of boost: " ${Boost_LIBRARIES} )

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS})
LINK_DIRECTORIES(${Boost_LIBRARY_DIRS})


ADD_DEFINITIONS(-DBOOST_PYTHON_STATIC_LIB)

# python section
FIND_PACKAGE(PythonLibs REQUIRED)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_DIRS})
LINK_DIRECTORIES(${PYTHON_LIBRARIES})
	
# beast section
FIND_PACKAGE(Beast REQUIRED)
INCLUDE_DIRECTORIES(${BEAST_INCLUDE_DIR})
LINK_DIRECTORIES(${BEAST_LIBRARY})

#FIXME
INCLUDE_DIRECTORIES($ENV{BEAST_COMMON})
MESSAGE("Beast Common Dir = " $ENV{BEAST_COMMON} )

FILE(GLOB py_beast_cpp "*.cpp")
ADD_LIBRARY (beastPython SHARED ${py_beast_cpp})
SET_TARGET_PROPERTIES( beastPython PROPERTIES SUFFIX ".pyd")

TARGET_LINK_LIBRARIES(beastPython ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} ${BEAST_LIBRARY})
