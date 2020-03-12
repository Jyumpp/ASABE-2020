#include "linecorrection.h"
#include <thread>
#include <functional>
#include <iostream>

using namespace std;

static double* angle;
static double* centerDistance;
static double errorAngle = .25;
static double errorDistance = .25;
static int pipeAngleRead;
static int pipeDistanceRead;
Robot* robot;

LineCorrection::LineCorrection(int pipeAngleR, int pipeDistanceR){
    robot = new Robot("test");
    pipeAngleRead = pipeAngleR;
    pipeDistanceRead = pipeDistanceR;
    thread angleCheck(&LineCorrection::checkAngle,this);
}

void LineCorrection::checkAngle(){
    while (true) {
        // what is the last paramenter
        read(pipeAngleRead, angle, 8);
        read(pipeDistanceRead, centerDistance, 8);
    }
}

void LineCorrection::whatMove(){
    while (true) {
        try{
            if(*centerDistance > errorDistance){
                robot->drive(0);
                robot->translate(90,-(*centerDistance)/2);
            } else{
                robot->drive(0);
                robot->translate(90,fabs(*centerDistance)/2);
            }
            if(*angle < errorAngle && *angle > -errorAngle){
                robot->drive(512);
            } else if(*angle > errorAngle){
                robot->drive(0);
                robot->centerAxisTurn(-(*angle)*.5);
            } else{
                robot->drive(0);
                robot->centerAxisTurn(fabs(*angle)*.5);
            }
        } catch(int e){
            robot->drive(0);
            robot->center();
            cout << "An Exception Occured: #" << e << endl;
        }
    }
}
