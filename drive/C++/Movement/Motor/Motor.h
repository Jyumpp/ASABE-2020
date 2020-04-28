#include <iostream>
#include <string>

using namespace std;

class Motor{

  static int count;
  static double homeAngle;

  public:
    Motor();
    Motor(bool,string);
    Motor(const Motor&);
    ~Motor();

    double getAngle();

    int setAngle(double);

    int setVelocity(double);

    double getVelocity();

    void operator=(const Motor&); // Copy Constructor for Motor

};
