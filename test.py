import time
from servocontrol.servo_control import SerialServo

time.sleep(2)
servos = [SerialServo(0, '/dev/ttyUSB1'), SerialServo(1, '/dev/ttyUSB1'), SerialServo(2, '/dev/ttyUSB1'),
          SerialServo(3, '/dev/ttyUSB1')]
servos[0].set_angle(85)
time.sleep(.1)
servos[1].set_angle(90)
time.sleep(.1)
servos[3].set_angle(85)
time.sleep(1)
servos[0].set_angle(90)
time.sleep(.1)
servos[2].set_angle(90)
time.sleep(.1)
servos[3].set_angle(75)
time.sleep(2)
