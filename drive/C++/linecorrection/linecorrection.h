#include <thread>
#include "../robot/robot.h"

class LineCorrection{
  static double angle;
  static double centerDistance;
  static double errorAngle;
  static double errorDistance;
  static int pipeAngleRead;
  static int pipeDistanceRead;
  Robot robot;

  LineCorrection();

  void checkAngle();

  void whatmove() const;
};
