from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
from Robot.Robot import *
import multiprocessing as mp

if __name__ == '__main__':

    #Sets threading type to fork
    mp.set_start_method('fork',force=True)

    #Creates Robot object
    robot = Robot("/dev/ttyUSB0")

    #Creates program pipes
    angleValue = mp.Value('d',0.0)
    distanceValue = mp.Value('d',0.0)

    #Sets up lineTracing and LineCorrection classes
    tracing = lineTracing(angleValue,distanceValue)
    correction = LineCorrection(angleValue,distanceValue,robot)

    #Makes and starts lineTracing
    threadTrace = mp.Process(target=tracing.lineTracer, args=())
    threadTrace.start()

    #Starts thread for Robot path correction
    threadCorrect = mp.Process(target=correction.whatMove, args=(robot,))
    threadCorrect.start()
