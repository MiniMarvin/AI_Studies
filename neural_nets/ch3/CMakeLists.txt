cmake_minimum_required(VERSION 2.8)

##set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_FLAGS "-O2")        ## Optimize

project( ex5 )
find_package( OpenCV REQUIRED )
add_executable( ex5 ex5.cpp libs/neuron.cpp )
target_link_libraries( ex5 ${OpenCV_LIBS} )