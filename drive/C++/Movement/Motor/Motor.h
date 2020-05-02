#include <iostream>
#include <string>
#include "/home/michael/Documents/RobotClub/dynamixel-controller/dynio.h"

typedef std::unique_ptr<dynio::DynamixelMotor> dyn_ptr;

using string=std::string;
using DynamixelIO = dynio::DynamixelIO;

class Motor{

  static int count;
  static double homeAngle;
  DynamixelIO* dynio = nullptr;
  dyn_ptr angleMotor;
  dyn_ptr driveMotor;
  bool right;


  public:
    Motor();

    Motor(bool,string);

    Motor(const Motor&);

    ~Motor();

    double getAngle();

    int setAngle(double);

    int setVelocity(double);

    double getVelocity();

    void operator=(const Motor& m);

};
