#include <iostream>
#include <string>

using namespace std;

class Motor{

  static int count;
  static double homeAngle;

  public:
    Motor(bool,string);

    double getAngle();

    void setAngle(double);

    void center();

    void setVelocity(double);

    double getVelocity();

};
