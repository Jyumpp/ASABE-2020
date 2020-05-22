#include "LineCorrection.h"

//Constructor for the LineCorrection object takes pipes for data transfer
LineCorrection::LineCorrection(int pipeAngleR, int pipeDistanceR, std::string path){
    robot = new Robot(path);
    pipeAngleRead = pipeAngleR;
    pipeDistanceRead = pipeDistanceR;
    std::thread angleCheck(&LineCorrection::checkAngle,this);
}

//Gets the current anlge of the Robot from LineTacking
void LineCorrection::checkAngle(){
    while (true) {
        // what is the last paramenter
        read(pipeAngleRead, angle, 8);
        read(pipeDistanceRead, centerDistance, 8);
    }
}

//Decides what action to preform next
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
            std::cout << "An Exception Occured: #" << e << std::endl;
        }
    }
}
