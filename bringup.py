import time
from MessageSender import *
from debugmessages import *
from dynio import *
from multiprocessing import Process, Pipe, Value
from drive.Robot.Motor import *
from drive.LineTracing.lineTracing import *
from drive.LineCorrection.LineCorrection import *
from drive.Robot.Robot import *
from vision.imagecapture.imagecapture import ImageCapture as cap
from vision.imageclassifier.imageclassifier import ImgClassifier as classifier

deployAngles = [1023, 671, 0, 0]
motors = []

if __name__ == '__main__':

    # Sets threading type to fork for LineCorrection Instances
    mp.set_start_method('spawn', force=True)

    # Creating Dynamixel Trigger motors
    dxl_io = dxl.DynamixelIO("/dev/ttyUSB0", 57600)
    motorList = [dxl_io.new_ax12(9), dxl_io.new_ax12(10), dxl_io.new_ax12(11), dxl_io.new_ax12(12)]
    for motor in motorList:
        motor.torque_disable()
    # Creats Motor Objects
    for i in range(0, 4):
        if i < 2:
            motors.append(Motor(True, dxl_io))
        else:
            motors.append(Motor(False, dxl_io))

    # Creates Robot object
    robot = Robot(motors)

    # # Creates Message Sender of GUI
    # sender = MessageSender()

    # Creates pipes for drive/linecorrection
    angleRead, angleWrite = Pipe(False)
    distRead, distWrite = Pipe(False)

    # Creates pipes for vision
    triggerRead1, triggerWrite1 = Pipe()
    triggerRead2, triggerWrite2 = Pipe()
    triggerRead3, triggerWrite3 = Pipe()
    triggerRead4, triggerWrite4 = Pipe()

    # Create shared memory for trigger and line correction
    stop = Value('i', 0)

    # Creates array of trigger states to control line following with
    correctEnable = {triggerRead1, triggerRead2, triggerRead3, triggerRead4}

    # Sets up lineTracing and LineCorrection classes
    tracing = lineTracing(angleWrite, distWrite)
    correction = LineCorrection(stop, correctEnable, angleRead, distRead, robot)

    # Sets up Vision system classes
    capture1 = cap(triggerRead1, 2, "/home/mendel/ASABE-2020/vision/imagecapture/output")
    capture2 = cap(triggerRead2, 3, "/home/mendel/ASABE-2020/vision/imagecapture/output")
    capture3 = cap(triggerRead3, 4, "/home/mendel/ASABE-2020/vision/imagecapture/output")
    capture4 = cap(triggerRead4, 5, "/home/mendel/ASABE-2020/vision/imagecapture/output")

    # Set up and run vision processes
    capture1Process = Process(target=capture1.Run, args=())
    capture2Process = Process(target=capture2.Run, args=())
    capture3Process = Process(target=capture3.Run, args=())
    capture4Process = Process(target=capture4.Run, args=())

    capture1Process.start()
    capture2Process.start()
    capture3Process.start()
    capture4Process.start()

    # Makes and starts lineTracing/Correction
    traceProcess = Process(target=tracing.lineTracer, args=())
    correctProcess = Process(target=correction.what_move, args=())
    traceProcess.start()
    correctProcess.start()

    # Wait for the Processes to end
    capture1Process.join()
    capture2Process.join()
    capture3Process.join()
    capture4Process.join()
    traceProcess.join()
    correctProcess.join()

    # # And then classify the images we took
    # time.sleep(1)
    # classify = classifier("/home/mendel/ASABE-2020/vision/imagecapture/output/")
    # classify.print()  # <- can this be made to return a list of values for each picture
    # # Look at Competition_gui for what numbers to use lines 100-104

    robot.drive(0)
