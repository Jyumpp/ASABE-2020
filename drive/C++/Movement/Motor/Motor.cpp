#include "Motor.h"

int Motor::count = 0;

using DynamixelIO = dynio::DynamixelIO;
using dynMotor = dynio::DynamixelMotor;

Motor::Motor(){

}

Motor::Motor(bool side, DynamixelIO& dxlIO){
    // Motor def
    // std::cout << "Motor Constructor" << std::endl;
    angleMotor = dxlIO.newAX12Raw(count++);
    angleMotor->setPositionMode(512);
    angleMotor->torqueEnable();
    driveMotor = dxlIO.newAX12Raw(count++);
    driveMotor->setVelocityMode();
    driveMotor->torqueEnable();
    homeAngle = 150;
    right = side;
}

Motor::Motor(const Motor& m){
  driveMotor = m.getDriveMotor();
  angleMotor = m.getAngleMotor();
  this->setSide(m.getSide());
  homeAngle = 150;
}

//Motor destructor
Motor::~Motor(){
  delete angleMotor;
  delete driveMotor;
}

//Gets the motor angle
double Motor::getAngle(){
    // gets angleMotor current position
    angleMotor->getAngle();
    return EXIT_SUCCESS;
}

//Sets the motor angle
int Motor::setAngle(double angle){
    // Sets angleMotors position
    angleMotor->setAngle(homeAngle-angle);
    // cout << "setAngle: " << angle << endl;
    return EXIT_SUCCESS;
}

//Sets the motor velocity
int Motor::setVelocity(double velocity){
    // sets the driveMotor velocity
    // cout << "setVelocity: " << velocity << endl;
    if(right){
            driveMotor->setVelocity(-velocity);
    } else{
        driveMotor->setVelocity(velocity);
    }
    return EXIT_SUCCESS;

}

const bool Motor::getSide() const{
  return right;
}

void Motor::setSide(bool side){
  right = side;
}

dynMotor* Motor::getAngleMotor()const{
  return angleMotor;
}

dynMotor* Motor::getDriveMotor()const{
  return driveMotor;
}

//Reads the motor velocity from the motor control table
double Motor::getVelocity(){
    // gets the current velocity of the driveMotor
    // cout << "getVelocity" << endl;
    return driveMotor->readControlTable("Present_Speed");
}

void Motor::operator=(const Motor& m) {
  this->driveMotor = m.getDriveMotor();
  this->angleMotor = m.getAngleMotor();
  this->setSide(m.getSide());
  homeAngle = 150;
}
