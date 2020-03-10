#include <iostream>
#include <string>
#include "motor.h"

using namespace std;

count = 1;
homeAngle = 150;

Motor::Motor(bool, string)
{
	// Motor def
}

double Motor::getAngle()
{
	// gets angleMotor current position
	return 0.0;
}

void Motor::setAngle(double)
{
	// Sets angleMotors position
}

void Motor::center()
{
	// Sets angleMotor to home position
	setAngle(150);
}

void Motor::setVelocity(double)
{
	// sets the driveMotor velocity

}

double Motor::getVelocity()
{
	// gets the current velocity of the driveMotor
	return 0.0;
}
