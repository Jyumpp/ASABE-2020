from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
from Robot.Robot import *
from debugmessages import *
import multiprocessing as mp

if __name__ == '__main__':

    badMsg = DebugMessages(self)

    #Sets threading type to fork
    mp.set_start_method('fork',force=True)

    #Creates Robot object
    badMsg.info("Initalizing Robot object")
    robot = Robot("/dev/ttyUSB0")

    #Creates program pipes
    angleValue = mp.Value('d',0.0)
    distanceValue = mp.Value('d',0.0)

    #Sets up lineTracing and LineCorrection classes
    badMsg.info("Initalizing Line Tracing Object")
    tracing = lineTracing(angleValue,distanceValue)
    badMsg.info("Initalizing Line Correction Object")
    correction = LineCorrection(angleValue,distanceValue,robot)

    #Makes and starts lineTracing
    badMsg.info("Starting Line Tracing")
    threadTrace = mp.Process(target=tracing.lineTracer, args=())
    threadTrace.start()

    #Starts thread for Robot path correction
    badMsg.info("Starting course correction")
    threadCorrect = mp.Process(target=correction.whatMove, args=(robot,))
    threadCorrect.start()
# r = Robot("/dev/ttyUSB0")
