
#include "motor.h"

using namespace std;

static int count = 1;

Motor::Motor(){
	// cout << "Hello" << endl;
}

Motor::Motor(bool right, string path)
{
	// Motor def
	// cout << "Motor Constructor" << endl;
}

Motor::Motor(const Motor& m){
	// cout << "copy" << endl;
}

Motor::~Motor(){

}

double Motor::getAngle()
{
	// gets angleMotor current position
	// cout << "getAngle" << endl;
	return EXIT_SUCCESS;
}

int Motor::setAngle(double angle)
{
	// Sets angleMotors position
	// cout << "setAngle " << angle << endl;
	return EXIT_SUCCESS;
}


int Motor::setVelocity(double velocity)
{
	// sets the driveMotor velocity
	// cout << "setVelocity: " << velocity << endl;
	return EXIT_SUCCESS;

}

double Motor::getVelocity()
{
	// gets the current velocity of the driveMotor
	// cout << "getVelocity" << endl;
	return 0.0;
}

void Motor::operator=(const Motor& m){
	// cout << "overload" << endl;
}
