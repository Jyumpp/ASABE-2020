from LineTracing.lineTracing import *
from LineCorrection.LineCorrection import *
from Robot.Robot import *
from dynio import *
from debugmessages import *
import multiprocessing as mp
import signal
import sys


badMsg = DebugMessages()

badMsg.info("Creating Dropper Motors")
#Creates Robot object
dyn = dxl.DynamixelIO(device_name="/dev/ttyUSB0")
robot = Robot(dyn)
dropperMotors = []
deployAngles = [1023,671,0,0]

badMsg.info("Done creating Dropper Motors")

for i in range(9,13):
    dropperMotors.append(dyn.new_ax12(i))

def exit(sig,frame):
    robot.drive(0)
    sys.exit(0)
    dyn = None

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

    # Running expandy boi
    robot.expandy_boi()
    robot.translate(0,-8)
    dropperMotors[3].set_position(deployAngles[3])
    dropperMotors[0].set_position(deployAngles[0])
    time.sleep(.25)
    robot.translate(0,10)
    dropperMotors[1].set_position(deployAngles[1])
    dropperMotors[2].set_position(deployAngles[2])
    robot.translate(0,5)
    for motor in dropperMotors:
        motor.torque_disable()

    # Starts thread for Robot path correction
    threadCorrect = mp.Process(target=correction.what_move, args=())
    threadCorrect.start()

    signal.signal(signal.SIGINT,exit)
# r = Robot("/dev/ttyUSB0")
