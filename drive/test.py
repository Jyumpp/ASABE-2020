from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
import multiprocessing as mp

if __name__ == '__main__':
    pipeAngleR,pipeAngleW = mp.Pipe()
    pipeDistanceR,pipeDistanceW = mp.Pipe()
    l = lineTracing(pipeAngleW,pipeDistanceW)
    c = LineCorrection(pipeAngleR,pipeDistanceR)
    mp.set_start_method('fork')
    threadTrace = mp.Process(target=l.lineTracer, args=())
    threadTrace.start()
    robot = Robot("/dev/ttyUSB0")
    # robot.expandyBoi()
    # robot.drive(512)
    # time.sleep(.5)
    # robot.drive(0)
    threadCorrect = mp.Process(target=c.whatMove, args=(robot,))
    threadCorrect.start()
