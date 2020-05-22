cmake_minimum_required(VERSION 2.8.4)
project(dynamixel_controller)

set(CMAKE_CXX_STANDARD 11)

file(GLOB JSON "../cget/include/nlohmann/*.h")


file(GLOB DYNAMIXEL_SDK
        "DynamixelSDK/src/DynamixelSDK.h"
        "DynamixelSDK/src/dynamixel_sdk/*.cpp"
        "DynamixelSDK/src/dynamixel_sdk/*.h")


add_library(dynamixel-controller main.cpp DynamixelIO.cpp DynamixelMotor.cpp ${DYNAMIXEL_SDK} ${JSON})

add_executable(main main.cpp DynamixelIO.cpp DynamixelMotor.cpp ${DYNAMIXEL_SDK} ${JSON})
