#include <iostream>
#include <unistd.h>
#include <cmath>
#include <chrono>
#include <thread>
#include <math.h>
#include <map>
#include <cstdarg>
#include <python3.6/Python.h>
#include "../../cget/include/pybind11/pybind11.h"
#include "../Motor/Motor.h"
#define _USE_MATH_DEFINES

using namespace std;

class Robot{

    Motor* motors;

    double degreeToRadians(double);      // Converts degrees to radians

    const double NORMALANGLE = 13.101;
    const double homeAngle = 150;

    public:

        Robot(string);                       // Constructor for the Robot class

        int drive(double);                   // Moves the Robot forward and backwards

        int center();                        // Centers the Robot wheels

        int diff();                          // Turns the wheels to be normal to center axis of rotation

        int crabSteering(double);            // Turn all wheels normal to home position

        int turn(double);                    // Turns the front wheels only (Ackermann Steering)

        int translate(double, double);     	 // Translates the Robot horizontally distance

        int centerAxisTurn(double);          // Turns the Robot on it's center axis

        int expandyBoi();                    // Expanding routine for startup

};
