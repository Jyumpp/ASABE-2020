#include <thread>
#include "../Movement/Robot/Robot.h"
// #include "../LineTacking/LineTracking.h"
#include <functional>
#include <iostream>

class LineCorrection{

    double* angle;
    double* centerDistance;
    double errorAngle = .25;
    double errorDistance = .25;
    static int pipeAngleRead;
    static int pipeDistanceRead;
    Robot* robot;

    public:
      LineCorrection(int,int); //LineCorrection constuctor

      void checkAngle(); //Gets the current anlge of the Robot from LineTacking

      void whatMove(); //Decides what action to preform next
};
