import time
from debugmessages import *
from dynio import *
from multiprocessing import Process, Pipe, Value
from drive.LineTracing.lineTracing import *
from drive.LineCorrection.LineCorrection import *
from drive.Robot.Robot import *
from vision.dynamixeltrigger.dynamixeltrigger import DynaTrigger as dyn
from vision.imagecapture.imagecapture import ImageCapture as cap
from vision.imageclassifier.imageclassifier import ImgClassifier as classifier


if __name__ == '__main__':

    # Sets threading type to fork for LineCorrection Instances
    mp.set_start_method('fork',force=True)

    # Creates Robot object
    robot = Robot("/dev/ttyUSB0")

    # Creating Dynamixel Trigger motors
    dxl_io = dxl.DynamixelIO("/dev/ttyUSB0", 57600)
    motorList = [dxl_io.new_ax12(9), dxl_io.new_ax12(10), dxl_io.new_ax12(11), dxl_io.new_ax12(12)]

    # Running expandy boi
    robot.expandy_boi(motorList)

    # Creates pipes for drive/linecorrection
    angleRead, angleWrite = Pipe()
    distRead, distWrite = Pipe()

    # Creates pipes for vision
    triggerRead1, triggerWrite1 = Pipe()
    triggerRead2, triggerWrite2 = Pipe()
    triggerRead3, triggerWrite3 = Pipe()
    triggerRead4, triggerWrite4 = Pipe()

    # Create shared memnory for trigger and line correction
    stop = Value('i', 0)

    # Sets up lineTracing and LineCorrection classes
    tracing = lineTracing(angleWrite,distWrite)
    correction = LineCorrection(stop, angleRead,distRead,robot)

    # Sets up Vision system classes
    trigger1 = dyn(stop, motorList[0], triggerWrite1)
    capture1 = cap(triggerRead1, 2, "/home/mendel/ASABE-2020/vision/imagecapture/output")
    trigger2 = dyn(stop, motorList[1], triggerWrite2)
    capture2 = cap(triggerRead2, 3, "/home/mendel/ASABE-2020/vision/imagecapture/output")
    trigger3 = dyn(stop, motorList[2], triggerWrite3)
    capture3 = cap(triggerRead3, 3, "/home/mendel/ASABE-2020/vision/imagecapture/output")
    trigger4 = dyn(stop, motorList[3], triggerWrite4)
    capture4 = cap(triggerRead4, 4, "/home/mendel/ASABE-2020/vision/imagecapture/output")

    # Set up and run vision processes 
    trigger1Process = Process(target=trigger1.Run(), args=())
    capture1Process = Process(target=capture1.Run(), args=())
    trigger2Process = Process(target=trigger2.Run(), args=())
    capture2Process = Process(target=capture2.Run(), args=())
    trigger3Process = Process(target=trigger3.Run(), args=())
    capture3Process = Process(target=capture3.Run(), args=())
    trigger4Process = Process(target=trigger4.Run(), args=())
    capture4Process = Process(target=capture4.Run(), args=())
    trigger1Process.start()
    capture1Process.start()
    trigger2Process.start()
    capture2Process.start()
    trigger3Process.start()
    capture3Process.start()
    trigger4Process.start()
    capture4Process.start()

    # Makes and starts lineTracing/Correction
    traceProcess = Process(target=tracing.lineTracer, args=())
    correctProcess = Process(target=correction.what_move, args=())
    traceProcess.start()
    correctProcess.start()

    # Wait for the Processes to end
    trigger1Process.join()
    capture1Process.join()
    trigger2Process.join()
    capture2Process.join()
    trigger3Process.join()
    capture3Process.join()
    trigger4Process.join()
    capture4Process.join()
    traceProcess.join()
    correctProcess.join()

    # And then classify the images we took
    time.sleep(1)
    classify = classifier("/home/mendel/ASABE-2020/vision/imagecapture/output/")
    classify.print()

