cmake_minimum_required(VERSION 3.10)
project(cpp)

set(CMAKE_CXX_STANDARD 14)

add_definitions(-D__MACOSX_CORE__ -D__LITTLE_ENDIAN__)
add_library(stk STATIC IMPORTED)
set_property(TARGET stk PROPERTY IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/stk/src/libstk.a)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/stk/include/)

add_executable(cpp main.cpp Chapter1LabEffect.h Rev.h RevLP.h FDNJot4.h ${CMAKE_CURRENT_SOURCE_DIR}/stk/projects/demo/utilities)
target_link_libraries(cpp stk)
target_link_libraries(cpp pthread)
target_link_libraries(cpp "-framework CoreAudio" "-framework CoreFoundation" "-framework CoreMIDI")
