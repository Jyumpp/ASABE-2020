#include <thread>
#include "../robot/robot.h"
#include "linecorrection.h"
#include <thread>
#include <functional>
#include <iostream>

class LineCorrection{

    static double* angle;
    static double* centerDistance;
    static double errorAngle = .25;
    static double errorDistance = .25;
    static int pipeAngleRead;
    static int pipeDistanceRead;
    Robot* robot;

    public:
      LineCorrection(int,int); //LineCorrection constuctor

      void checkAngle(); //Gets the current anlge of the Robot from LineTacking

      void whatMove(); //Decides what action to preform next
};
