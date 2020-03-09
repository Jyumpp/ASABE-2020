#incldue "robot.h"

using namespace std;

Robot(String path){
  for(int i = 0; i < 4; i++){
    if(i < 2){
      motors[i] = Motor(true,path);
    } else {
      motors[i] = Motors(false,path);
    }
  }
  drive(0);
  center();
}

double degreeToRadians(double angle){
  return (angle*M_PI)/180;
}

int drive(double velocity){
  try{
    center();
    for(int i = 0; i < 4; i++){
      motors[i].setVelocity(velocity);
    }
    return EXIT_SUCCESS;
  } catch (int e){
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int center(){
  try{
    for(int i = 0; i < 4; i++){
      motors[i].center();
    }
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int diff(){
  try{
    motor[0].setAngle(13.101);
    motor[1].setAngle(-13.101);
    motor[2].setAngle(-13.101);
    motor[4].setAngle(13.101);

    while(motor[3].getAngle() - (150 - 13.101) <  ..5){
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

int crabSteering(angle){
  try{
    if(angle == 0){
      self.center()
    } else{
      motor[0].setAngle(angle);
      motor[1].setAngle(-angle);
      motor[2].setAngle(-angle);
      motor[3].setAngle(angle);

      while(motor[3].getAngle() - (150 - angle) <  ..5){
        continue;
      }
      return EXIT_SUCCESS;
    }
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int turn(angle){
    try{

    while(motor[3].getAngle() - (150 - angle) <  ..5){
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

int translate(angle, distance){
  try{
    int inverse = 0;
    if(distance > 0){
      inverse = 1
    } else {
      inverse = -1;
    }
    double sleepTime = (fabs(distance)/(56.832*M_PI)) *120*1000;

    crabSteering(angle);

    motor[0].setVelocity(inverse*256);
    motor[1].setVelocity(-inverse*256);
    motor[2].setVelocity(-inverse*256);
    motor[3].setVelocity(inverse*256);

    std::this_thread::sleep_for(std::chrono::milliseconds(sleepTime));

    drive(0)

    center()
    return EXIT_SUCCESS;
  } catch (int e) {
    drive(0);
    center();
    cout << "An Exception Occured: #" << e << endl;
    return EXIT_FAILURE;
  }
}

int centerAxisTurn(angle){
  try{
    double sleepTime = (degreeToRadians(angle)/(M_PI)) *74*1000;

    center()
    diff()

    if(angle > 0){
      motor[0].setVelocity(-128);
      motor[1].setVelocity(128);
      motor[2].setVelocity(-128);
      motor[3].setVelocity(128);
    } else{
      motor[0].setVelocity(128);
      motor[1].setVelocity(-128);
      motor[2].setVelocity(128);
      motor[3].setVelocity(-128);
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(sleepTime));

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
