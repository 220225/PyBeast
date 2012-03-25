# - Try to find Beast
# Once done this will define
#  BEAST_FOUND - System has Beast installed
#  BEAST_INCLUDE_DIRS - The Beast include directories
#  BEAST_LIBRARIES - The libraries needed to use Beast
FIND_PATH(BEAST_INCLUDE_DIR beastapi/beastapitypes.h
	PATHS $ENV{BEAST_SDK}/include )

FIND_LIBRARY(BEAST_LIBRARY NAMES beast32
				PATHS $ENV{BEAST_SDK}/lib)

SET(BEAST_LIBRARIES ${BEAST_LIBRARY} )
SET(BEAST_INCLUDE_DIRS ${BEAST_INCLUDE_DIR} )

INCLUDE(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set BEAST_FOUND to TRUE
# if all listed variables are TRUE
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Beast  DEFAULT_MSG
	BEAST_LIBRARY BEAST_INCLUDE_DIR)

MARK_AS_ADVANCED(BEAST_INCLUDE_DIR BEAST_LIBRARY )
