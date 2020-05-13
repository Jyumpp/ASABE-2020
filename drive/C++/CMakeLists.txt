cmake_minimum_required(VERSION 2.8.4)
project(dynamixel_controller)

set(CMAKE_CXX_STANDARD 11)

file(GLOB JSON "cget/include/nlohmann/*.h")

file(GLOB DYNAMIXEL_SDK
        "DynamixelSDK/src/DynamixelSDK.h"
        "DynamixelSDK/src/dynamixel_sdk/*.cpp"
        "DynamixelSDK/src/dynamixel_sdk/*.h")


#add_library(dynamixel-controller cget/include/dynamixel-controller/DynamixelIO.cpp cget/include/dynamixel-controller/DynamixelMotor.cpp ${DYNAMIXEL_SDK} ${JSON})

#add_executable(linecorrection Movement/Motor/Motor.cpp Movement/Robot/Robot.cpp cget/include/dynamixel-controller/DynamixelIO.cpp cget/include/dynamixel-controller/DynamixelMotor.cpp ${DYNAMIXEL_SDK} ${JSON})

find_package(pybind11 REQUIRED)
pybind11_add_module(Robot cget/include/dynamixel-controller/DynamixelIO.cpp cget/include/dynamixel-controller/DynamixelMotor.cpp Movement/Motor/Motor.cpp Movement/Robot/Robot.cpp ${DYNAMIXEL_SDK} ${JSON})
