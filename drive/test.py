from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
from Robot.Robot import *
from debugmessages import *
import multiprocessing as mp
import signal
import sys

#Creates Robot object
robot = Robot("/dev/ttyUSB0")

def exit(sig,frame):
    robot.drive(0)
    sys.exit(0)

if __name__ == '__main__':

    #Sets threading type to fork
    mp.set_start_method('fork',force=True)

    #Creates program pipes
    angleRead, angleWrite = mp.Pipe()
    distRead, distWrite = mp.Pipe()

    #Sets up lineTracing and LineCorrection classes
    tracing = lineTracing(angleWrite,distWrite)
    correction = LineCorrection(angleRead,distRead,robot)

    # Makes and starts lineTracing
    threadTrace = mp.Process(target=tracing.lineTracer, args=())
    threadTrace.start()

    # Starts thread for Robot path correction
    threadCorrect = mp.Process(target=correction.what_move, args=())
    threadCorrect.start()

    signal.signal(signal.SIGINT,exit)
# r = Robot("/dev/ttyUSB0")
