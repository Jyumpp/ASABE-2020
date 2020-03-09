#define PY_SSIZE_T_CLEAN
#include <Python.h>

class motor{
  static int count = 1;
  static dynIO* dyn = NULL;
  static double homeAngle = 150;
  dynIO* angleMotor = NULL;
  dynIO* driveMotor = NULL;

  public:
    motor();

    dobule getAngle();

    void setAngle(double);

    void center();

    void setVelocity(double);

    double getVelocity();

};
