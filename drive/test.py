from lineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
import multiprocessing as mp

if __name__ == '__main__':
    pipeR,pipeW = mp.Pipe()
    l = lineTracing(pipeW)
    c = LineCorrection(pipeR)
    mp.set_start_method('spawn')
    threadTrace = mp.Process(target=l.lineTracer, args=())
    threadTrace.start()
    threadCorrect = mp.Process(target=c.whatMove, args=())
    threadCorrect.start()
