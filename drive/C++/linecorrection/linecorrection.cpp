#include "LineCorrection"

angle = 0;
centerDistance = 0;

LineCorrection(int pipeAngleR, int pipeDistanceR, Robot bot){
    Robot robot = bot;
    pipeAngleRead = pipeAngleR;
    pipeDistanceRead = pipeDistanceR;
    // make and start checkAngle thread
}

void checkAngle(){
    // what is the last paramenter
    read[pipeAngleRead,angle];
    read[pipeDistanceRead,centerDistance];
}

void whatMove() const{
    while true{
        try{
            if(centerDistance > errorDistance){
                robot.drive(0);
                robot.translate(90,-centerDistance/2);
            } else{
                robot.drive(0);
                robot.translate(90,fabs(centerDistance)/2);
            }
            if(angle < errorAngle && angle > -errorAngle){
                robot.drive(512);
            } else if(angle > self.error){
                robot.drive(0);
                robot.centerAxis(-angle*.5);
            } else{
                robot.drive(0);
                robot.centerAxis(fabs(angle)*.5);
            }
        } catch(int e){
            robot.drive(0);
            robot.center();
            cout << "An Exception Occured: #" << e << endl;
        }
    }
}
