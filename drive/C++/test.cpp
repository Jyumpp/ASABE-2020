#include <thread>
#include "linecorrection/linecorrection.h"
//#include "linetracking/linetracking.h"


int main(){
    int AnglePipe[2];
    int centerDistancePipe[2];
    Robot robot = Robot("/dev/ttyUSB0");
    // LineTracer Object
    LineCorrection correction = LineCorrection(AnglePipe[0],centerDistancePipe[0],robot);
    std::thread thread_object(); // LineTracking Object
    std::thread thread_object(correction.whatMove());
}
