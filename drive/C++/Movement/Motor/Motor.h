#include <iostream>
#include <string>
#include "../../cget/include/dynamixel-controller/dynio.h"

typedef std::unique_ptr<dynio::DynamixelMotor> dyn_ptr;

using string=std::string;
using DynamixelIO = dynio::DynamixelIO;

class Motor{

  static int count;
  DynamixelIO* dynio = nullptr;
  dyn_ptr angleMotor;
  dyn_ptr driveMotor;
  bool right;
  double homeAngle;


  public:

    Motor(bool,string); //Motor Constructor takes the math to Dynamixel port and position of the motor

    ~Motor(); //Destructor for Motor object

    double getAngle(); //Gets the current angle of the motor

    int setAngle(double); //Sets the angle for the motor

    int setVelocity(double); //Sets velocity of the motor

    double getVelocity();	//gets the velocity of the motor

    void operator=(const Motor& m); //I do not know why I have this. Will look into

};
