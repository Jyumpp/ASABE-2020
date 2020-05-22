from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
import multiprocessing as mp

if __name__ == '__main__':
    #Creates program pipes
    pipeAngleR,pipeAngleW = mp.Pipe()
    pipeDistanceR,pipeDistanceW = mp.Pipe()

    #Sets up lineTracing and LineCorrection classes
    tracing = lineTracing(pipeAngleW,pipeDistanceW)
    correction = LineCorrection(pipeAngleR,pipeDistanceR)

    #Sets threading type to fork
    mp.set_start_method('fork')

    #Makes and starts lineTracing
    threadTrace = mp.Process(target=tracing.lineTracer, args=())
    threadTrace.start()

    #Creates Robot object
    robot = Robot("/dev/ttyUSB0")

    #Starts the thread to check robot angle (Python Threads append data to pipes)
    threadCheckPipe = mp.Process(target=c.checkAngle,args=())
    threadCheckPipe.start()

    #Starts thread for Robot path correction
    threadCorrect = mp.Process(target=correction.whatMove, args=(robot,))
    threadCorrect.start()
