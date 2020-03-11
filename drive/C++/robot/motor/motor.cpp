#include <iostream>
#include <string>
#include "motor.h"

using namespace std;

count = 1;
homeAngle = 150;

Motor::Motor(bool right, string path)
{
	// Motor def
	cout << "Motorc Constructor" << endl;
}

double Motor::getAngle()
{
	// gets angleMotor current position
	cout << "getAngle" << endl;
	return 0.0;
}

void Motor::setAngle(double angle)
{
	// Sets angleMotors position
	cout << "setAngle " << <angle < endl;
}


void Motor::setVelocity(double velocity)
{
	// sets the driveMotor velocity
	cout << "setVelocity: " << velocity << endl;

}

double Motor::getVelocity()
{
	// gets the current velocity of the driveMotor
	cout << "getVelocity"
	return 0.0;
}
