#include <thread>
#include "../robot/robot.h"

class LineCorrection{
    public:
      LineCorrection(int,int);

      void checkAngle();

      void whatMove();
};
