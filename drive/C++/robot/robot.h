#include <iostream>
#include <uistd.h>
#include <cmath>
#include <chrono>
#include <thread>
#include <math.h>
#include "motor/motor.h"
#define _USE_MATH_DEFINES

using namespace std;
static doulbe length;
static double width;
class Robot{
  Motor* motors;

  public:

    Robot(const Motor*);                // Constructor for the Robot class

    double degreeToRadians(double);     // Converts degrees to radians

    int drive(double);                  // Moves the Robot forward and backwards

    int center();                       // Centers the Robot wheels

    int diff();                         // Turns the wheels to be normal to center axis of rotation

    int crabSteering(angle);            // Turn all wheels normal to home position

    int turn(angle);                    // Turns the front wheels only (Ackermann Steering)

    int translate(angle, distance);     // Translates the Robot horizontally distance

    int centerAxisTurn(angle);          // Turns the Robot on it's center axis

    int expandyBoi();                   // Expanding routine for startup
};
