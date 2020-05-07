#include "Motor.h"

static int count = 1;

typedef std::shared_ptr<dynio::DynamixelMotor> dyn_ptr;

Motor::Motor(){

}

Motor::Motor(bool side, std::string path){
    if(dynio == nullptr){
        //Check Baudrate
        dynio = new DynamixelIO(path);
    }
    // Motor def
    // cout << "Motor Constructor" << endl;
    angleMotor = dynio->newAX12(count);
    angleMotor->setPositionMode(512);
    angleMotor->torqueEnable();
    count = count + 1;
    driveMotor=dynio->newAX12(count);
    driveMotor->setVelocityMode();
    driveMotor->torqueEnable();
    count = count + 1;
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
    delete dynio;
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

const dyn_ptr Motor::getAngleMotor()const{
  return angleMotor;
}

const dyn_ptr Motor::getDriveMotor()const{
  return driveMotor;
}

//Reads the motor velocity from the motor control table
double Motor::getVelocity(){
    // gets the current velocity of the driveMotor
    // cout << "getVelocity" << endl;
    return driveMotor->readControlTable("Present_Speed");
}

void Motor::operator=(const Motor& m) {
  driveMotor = m.getDriveMotor();
  angleMotor = m.getAngleMotor();
  this->setSide(m.getSide());
  homeAngle = 150;
}
