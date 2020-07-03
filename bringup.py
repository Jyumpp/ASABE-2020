import time
from time import sleep
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

motors = []

if __name__ == '__main__':

    # Sets threading type to fork for LineCorrection Instances
    mp.set_start_method('fork', force=True)

    # # Creates Message Sender of GUI
    # sender = MessageSender()

    # Creates pipes for drive/linecorrection
    angle_read, angle_write = Pipe(False)
    dist_read, dist_write = Pipe(False)

    # Creates pipes for vision
    triggerRead1, triggerWrite1 = Pipe()
    triggerRead2, triggerWrite2 = Pipe()
    triggerRead3, triggerWrite3 = Pipe()
    triggerRead4, triggerWrite4 = Pipe()

    # Creates array of trigger states to control line following with
    correct_enable = [triggerWrite1, triggerWrite2, triggerWrite3, triggerWrite4]

    # Sets up lineTracing classes
    tracing = lineTracing(angle_write, dist_write)

    # Starts Line Tracing Process
    traceProcess = Process(target=tracing.lineTracer, args=())
    traceProcess.start()

    #Sets up LineCorrection classes
    correction = LineCorrection(angle_read, dist_read, correct_enable)

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

    # Makes and starts Correction
    correctProcess = Process(target=correction.what_move, args=())
    correctProcess.start()

    # # Wait for the Processes to end
    capture1Process.join()
    capture2Process.join()
    capture3Process.join()
    capture4Process.join()
    correctProcess.join()

    # # # And then classify the images we took
    # time.sleep(1)
    # classify = classifier("/home/mendel/ASABE-2020/vision/imagecapture/output/")
    # classify.print()  # <- can this be made to return a list of values for each picture
    # # # # Look at Competition_gui for what numbers to use lines 100-104
