
#include "Motor.h"

static int count = 1;


Motor::Motor(){
	// cout << "Hello" << endl;
}

Motor::Motor(bool right, string path){
	if(dynio == nullptr){
		//Check Baudrate
		auto dynio = new DynamixelIO(path);
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
	this->right = right;
	homeAngle = 150;
}

Motor::Motor(const Motor& m){
	// cout << "copy" << endl;
}

Motor::~Motor(){

}

double Motor::getAngle(){
	// gets angleMotor current position
	angleMotor->getAngle();
	return EXIT_SUCCESS;
}

int Motor::setAngle(double angle){
	// Sets angleMotors position
	angleMotor->setAngle(homeAngle-angle);
	// cout << "setAngle: " << angle << endl;
	return EXIT_SUCCESS;
}


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

double Motor::getVelocity(){
	// gets the current velocity of the driveMotor
	// cout << "getVelocity" << endl;
	return driveMotor->readControlTable("Present_Speed");
}

void Motor::operator=(const Motor& m){
	// cout << "overload" << endl;
}
