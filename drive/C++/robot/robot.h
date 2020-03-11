#include <iostream>
#include <unistd.h>
#include <cmath>
#include <chrono>
#include <thread>
#include <math.h>
#include <array>
#include "motor/motor.h"
#define _USE_MATH_DEFINES

using namespace std;

class Robot{
    static double length;
    static double width;
    array<Motor*, 4> motors = {nullptr,nullptr,nullptr,nullptr };
    public:
        Robot(string);                      // Constructor for the Robot class

        double degreeToRadians(double);     // Converts degrees to radians

        int drive(double);                  // Moves the Robot forward and backwards

        int center();                       // Centers the Robot wheels

        int diff();                         // Turns the wheels to be normal to center axis of rotation

        int crabSteering(double);            // Turn all wheels normal to home position

        int turn(double);                    // Turns the front wheels only (Ackermann Steering)

        int translate(double, double);     // Translates the Robot horizontally distance

        int centerAxisTurn(double);          // Turns the Robot on it's center axis

        int expandyBoi();                   // Expanding routine for startup
};
