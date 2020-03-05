from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
import multiprocessing as mp

if __name__ == '__main__':
    pipeAngleR,pipeAngleW = mp.Pipe()
    pipeDistanceR,pipeDistanceW = mp.Pipe()
    l = lineTracing(pipeAngleW,pipeDistanceW)
    c = LineCorrection(pipeAngleR,pipeDistanceR)
    mp.set_start_method('spawn')
    threadTrace = mp.Process(target=l.lineTracer, args=())
    threadTrace.start()
    threadCorrect = mp.Process(target=c.whatMove, args=())
    threadCorrect.start()
