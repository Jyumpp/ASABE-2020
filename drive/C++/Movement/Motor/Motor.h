#include <iostream>
#include <string>
#include "../../cget/include/dynamixel-controller/dynio.h"

typedef std::shared_ptr<dynio::DynamixelMotor> dyn_ptr;

using DynamixelIO = dynio::DynamixelIO;

class Motor{

  static int count;
  static DynamixelIO* dynio;
  dyn_ptr angleMotor;
  dyn_ptr driveMotor;
  bool right;
  double homeAngle;


  public:

    Motor(); //Motor default constructor
    Motor(bool,std::string); //Motor Constructor takes the path to Dynamixel port and position of the motor
    Motor(const Motor&); //Copy Constructor

    ~Motor(); //Destructor for Motor object

    double getAngle(); //Gets the current angle of the motor

    int setAngle(double); //Sets the angle for the motor

    int setVelocity(double); //Sets velocity of the motor

    double getVelocity();	//gets the velocity of the motor

    const bool getSide() const;

    void setSide(bool); //Setter for motor side

    const dyn_ptr getAngleMotor() const;

    const dyn_ptr getDriveMotor()const;

    void operator=(const Motor&); //I do not know why I have this. Will look


};
