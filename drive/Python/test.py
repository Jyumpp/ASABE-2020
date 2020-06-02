<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
import multiprocessing as mp

if __name__ == '__main__':
    #Creates Robot object
    robot = Robot("/dev/ttyUSB0")

    #Creates program pipes
    angleValue = mp.Value('d',0.0)
    distanceValue = mp.Value('d',0.0)

    #Sets up lineTracing and LineCorrection classes
    tracing = lineTracing(angleValue,distanceValue)
    correction = LineCorrection(angleValue,distanceValue,robot)

    #Sets threading type to fork
    mp.set_start_method('fork')

    #Makes and starts lineTracing
    threadTrace = mp.Process(target=tracing.lineTracer, args=())
    threadTrace.start()

    #Starts the thread to check robot angle (Python Threads append data to pipes)
    threadCheckPipe = mp.Process(target=c.checkAngle,args=())
    threadCheckPipe.start()

    #Starts thread for Robot path correction
    threadCorrect = mp.Process(target=correction.whatMove, args=(robot,))
    threadCorrect.start()
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
# from LineTracing.lineTracing import *
# from LineCorrection.LineCorrection import *
# import multiprocessing as mp
#
# if __name__ == '__main__':
#     pipeAngleR,pipeAngleW = mp.Pipe()
#     pipeDistanceR,pipeDistanceW = mp.Pipe()
#     l = lineTracing(pipeAngleW,pipeDistanceW)
#     c = LineCorrection(pipeAngleR,pipeDistanceR)
#     mp.set_start_method('fork')
#     threadTrace = mp.Process(target=l.lineTracer, args=())
#     threadTrace.start()
#     robot = Robot("/dev/ttyUSB0")
#     # robot.expandyBoi()
#     # robot.drive(512)
#     # time.sleep(.5)
#     # robot.drive(0)
#     threadCorrect = mp.Process(target=c.whatMove, args=(robot,))
#     threadCorrect.start()
from Robot.Robot import *

r = Robot("/dev/ttyUSB0")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
