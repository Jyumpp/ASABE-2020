#include <iostream>
#include <string>
#include "../../cget/include/dynamixel-controller/dynio.h"

using DynamixelIO = dynio::DynamixelIO;
using dynMotor = dynio::DynamixelMotor;

class Motor{

  static int count;
  dynMotor* angleMotor;
  dynMotor* driveMotor;
  bool right;
  double homeAngle;


  public:

    Motor(); //Motor default constructor
    Motor(bool,DynamixelIO&); //Motor Constructor takes the path to Dynamixel port and position of the motor
    Motor(const Motor&); //Copy Constructor

    ~Motor(); //Destructor for Motor object

    double getAngle(); //Gets the current angle of the motor

    int setAngle(double); //Sets the angle for the motor

    int setVelocity(double); //Sets velocity of the motor

    double getVelocity();	//gets the velocity of the motor

    const bool getSide() const;

    void setSide(bool); //Setter for motor side

    dynMotor* getAngleMotor() const;

    dynMotor* getDriveMotor()const;

    void operator=(const Motor&); //I do not know why I have this. Will look


};
