#define PY_SSIZE_T_CLEAN
#include <Python.h>

class Motor{
  static int count = 1;
  static dynIO* dyn = NULL;
  static double homeAngle = 150;
  dynIO* angleMotor = NULL;
  dynIO* driveMotor = NULL;

  public:
    Motor();

    dobule getAngle();

    void setAngle(double);

    void center();

    void setVelocity(double);

    double getVelocity();

};
