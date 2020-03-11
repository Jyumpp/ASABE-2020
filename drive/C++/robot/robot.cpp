#include "robot.h"

using namespace std;

Robot::Robot(string path) {
    for (int i = 0; i < 4; i++) {
        if (i < 2) {
            *motors[i] = Motor(true, path);
        } else {
            *motors[i] = Motor(false, path);
        }
    }
    drive(0);
    center();
}

double Robot::degreeToRadians(double angle){
  return (angle*M_PI)/180;
}

int Robot::drive(double velocity){
  try{
    center();
    for(int i = 0; i < 4; i++){
      motors[i]->setVelocity(velocity);
    }
    return EXIT_SUCCESS;
  } catch (int e){
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int Robot::center(){
  try{
    for(int i = 0; i < 4; i++){
      motors[i]->setAngle(150);
    }
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int Robot::diff(){
  try{
      motors[0]->setAngle(13.101);
      motors[1]->setAngle(-13.101);
      motors[2]->setAngle(-13.101);
      motors[4]->setAngle(13.101);

    while(motors[3]->getAngle() - (150 - 13.101) < .5){
      continue;
    }
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int Robot::crabSteering(double angle){
  try {
    if(angle == 0){
        center();
        return EXIT_SUCCESS;
    } else{
        motors[0]->setAngle(angle);
        motors[1]->setAngle(-angle);
        motors[2]->setAngle(-angle);
        motors[3]->setAngle(angle);

        // while(motors[3]->getAngle() - (150 - angle) < .5){
        //     continue;
        // }
        return EXIT_SUCCESS;
    }
  } catch (int e) {
        drive(0);
        center();
        cout << "An Exception Occured: #" << e << endl;
        return EXIT_FAILURE;
  }
}

int Robot::turn(double angle){
    try{
        angle = degreeToRadians(angle);
        //double timeSleep = ;
        double inside = (2*length*sin(angle))/(2*length*cos(angle)-sin(angle));
        double outside = (2*length*sin(angle))/(2*length*cos(angle)+sin(angle));
        if(angle > 0){
            motors[1]->setAngle(inside);
            motors[2]->setAngle(outside);
        } else{
            motors[1]->setAngle(outside);
            motors[2]->setAngle(inside);
        }
        // while(motors[3]->getAngle() - (150 - angle) <  ..5){
        // 	continue;
        // }


        return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

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

    motors[0]->setVelocity(inverse*256);
    motors[1]->setVelocity(-inverse*256);
    motors[2]->setVelocity(-inverse*256);
    motors[3]->setVelocity(inverse*256);

    this_thread::sleep_for(chrono::nanoseconds(sleepTime));

    drive(0);

        center();
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int Robot::centerAxisTurn(double angle){
  try{
    long long sleepTime = (degreeToRadians(angle)/(M_PI)) *74*1000000000;

    center();
    diff();

    if(angle > 0){
      motors[0]->setVelocity(-128);
      motors[1]->setVelocity(128);
      motors[2]->setVelocity(-128);
      motors[3]->setVelocity(128);
    } else{
      motors[0]->setVelocity(128);
      motors[1]->setVelocity(-128);
      motors[2]->setVelocity(128);
      motors[3]->setVelocity(-128);
    }

    this_thread::sleep_for(chrono::nanoseconds(sleepTime));

    drive(0);
    center();
    return EXIT_SUCCESS;
  } catch (int e) {
      drive(0);
      center();
      cout << "An Exception Occured: #" << e << endl;
      return EXIT_FAILURE;
    }
}

int Robot::expandyBoi() {
    try {
        translate(0, -3);

        long long sleepTime = ((22.5) / (28.416 * M_PI)) * 60 *1000000000;

        crabSteering(90);

        motors[0]->setVelocity(1023);
        motors[1]->setVelocity(-230);
        motors[2]->setVelocity(-1023);
        motors[3]->setVelocity(230);

        this_thread::sleep_for(chrono::nanoseconds(sleepTime));

        drive(0);
        center();

        return EXIT_SUCCESS;
    }
    catch (int e) {
        drive(0);
        center();
        cout << "An Exception Occured: #" << e << endl;
        return EXIT_FAILURE;
    }
}
