#include "Robot.h"

using DynamixelIO = dynio::DynamixelIO;

static double length = 8;
static double width = 36;
const double NORMALANGLE = 13.101;
const double homeAngle = 150;

//Robot Contructor takes path to Dynamixel port
Robot::Robot(std::string path) {
  DynamixelIO dxlObject = DynamixelIO(path);
  for(int i = 0; i < 4; i++){
    if(i < 2){
      motors.assign(i,Motor(true,dxlObject));
    } else{
      motors.assign(i,Motor(false,dxlObject));
    }
  }
  drive(0);
  center();
  // std::cout << path << std::endl;
}

//Helper method for converting degrees to radians (This is probably already a thing)
double Robot::degreeToRadians(double angle){
  return (angle*M_PI)/180;
}


//Causes the Robot to move either forward of backaward; takes a velocity value
int Robot::drive(double velocity){
  try{
    for(int i = 0; i < 4; i++){
      motors[i].setVelocity(velocity);
    }
    return EXIT_SUCCESS;
  } catch (int e){
    center();
    std::cout << "An Exception Occured: #" << e << std::endl;
    return EXIT_FAILURE;
  }
}


//Turns the motors to home angle(150)
int Robot::center(){
  try{
    for(int i = 0; i < 4; i++){
      motors[i].setAngle(150);
    }
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    // std::cout << "An Exception Occured: #" << e << std::endl;
    return EXIT_FAILURE;
  }
}

//Turns the wheels to be at angle
int Robot::crabSteering(double angle){
  try {
    if(angle == 0){
        center();
        return EXIT_SUCCESS;
    } else{
        motors[0].setAngle(angle);
        motors[1].setAngle(-angle);
        motors[2].setAngle(-angle);
        motors[3].setAngle(angle);

        while(motors[3].getAngle() - (150 - angle) < .5){
            continue;
        }
        return EXIT_SUCCESS;
    }
  } catch (int e) {
        drive(0);
        center();
        std::cout << "An Exception Occured: #" << e << std::endl;
        return EXIT_FAILURE;
  }
}

//Turns the robot angle from current position
int Robot::turn(double angle){
    try{
        angle = degreeToRadians(angle);
        //double timeSleep = ;
        double inside = (2*length*sin(angle))/(2*length*cos(angle)-width*sin(angle));
        double outside = (2*length*sin(angle))/(2*length*cos(angle)+width*sin(angle));
        if(angle > 0){
            motors[1].setAngle(inside);
            motors[2].setAngle(outside);
        } else{
            motors[1].setAngle(outside);
            motors[2].setAngle(inside);
        }
        while(motors[3].getAngle() - (150 - angle) <  .5){
            continue;
        }


        return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    std::cout << "An Exception Occured: #" << e << std::endl;
    return EXIT_FAILURE;
  }
}


//Translates the robot at angle distance form current position
int Robot::translate(double angle, double distance){
  try{
    int inverse = 0;
    if(distance > 0){
        inverse = 1;
    } else {
      inverse = -1;
    }
    long long sleepTime = (fabs(distance)/(56.832*M_PI)) *120*1000000000;

    crabSteering(angle);

    motors[0].setVelocity(inverse*256);
    motors[1].setVelocity(-inverse*256);
    motors[2].setVelocity(-inverse*256);
    motors[3].setVelocity(inverse*256);

    std::this_thread::sleep_for(std::chrono::nanoseconds(sleepTime));

    drive(0);

        center();
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    std::cout << "An Exception Occured: #" << e << std::endl;
    return EXIT_FAILURE;
  }
}


//Turns the robot angle from current position on the center axis
int Robot::centerAxisTurn(double angle){
  try{
    long long sleepTime = (degreeToRadians(angle)/(M_PI)) *74*1000000000;

    center();
    crabSteering(NORMALANGLE);

    if(angle > 0){
      motors[0].setVelocity(-128);
      motors[1].setVelocity(128);
      motors[2].setVelocity(-128);
      motors[3].setVelocity(128);
    } else{
      motors[0].setVelocity(128);
      motors[1].setVelocity(-128);
      motors[2].setVelocity(128);
      motors[3].setVelocity(-128);
    }

    std::this_thread::sleep_for(std::chrono::nanoseconds(sleepTime));

    drive(0);
    center();
    return EXIT_SUCCESS;
  } catch (int e) {
      drive(0);
      center();
      std::cout << "An Exception Occured: #" << e << std::endl;
      return EXIT_FAILURE;
    }
}


//Expands the robot and positions it on the center row to being sensing
int Robot::expandyBoi() {
    try {
        translate(0, -3);

        long long sleepTime = ((22.5) / (28.416 * M_PI)) * 60 *1000000000;

        crabSteering(90);

        motors[0].setVelocity(1023);
        motors[1].setVelocity(-230);
        motors[2].setVelocity(-1023);
        motors[3].setVelocity(230);

        std::this_thread::sleep_for(std::chrono::nanoseconds(sleepTime));

        drive(0);
        center();

        return EXIT_SUCCESS;
    }
    catch (int e) {
        drive(0);
        center();
        std::cout << "An Exception Occured: #" << e << std::endl;
        return EXIT_FAILURE;
    }
}
