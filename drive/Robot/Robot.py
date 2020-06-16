from Robot.Motor import *
from debugmessages import *
import time
import math


class Robot:
    motors = []
    velocity = 0

    def drive(self, velocity):
        try:
            for motor in self.motors:
                motor.set_velocity(velocity)

        except Exception as e:
            print(e)
            self.center()

    def center(self):
        try:
            for motor in self.motors:
                motor.center()

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def four_wheel_turn(self):
        normalAngle = 8.993
        try:
            self.motors[1].set_angle(normalAngle)
            self.motors[2].set_angle(-normalAngle)
            self.motors[0].set_angle(-normalAngle)
            self.motors[3].set_angle(normalAngle)

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def diff_turn(self):
        self.motors[0].set_velocity(-512)
        self.motors[1].set_velocity(-512)
        self.motors[2].set_velocity(512)
        self.motors[3].set_velocity(512)

    def crab_steering(self, angle):
        try:
            if angle == 0:
                self.center()
            elif angle == 90:
                self.motors[1].set_angle(angle)
                self.motors[2].set_angle(-angle)
                self.motors[0].set_angle(-angle)
                self.motors[3].set_angle(angle)
            else:
                self.motors[1].set_angle(-angle)
                self.motors[2].set_angle(-angle)
                self.motors[0].set_angle(-angle)
                self.motors[3].set_angle(-angle)

                while math.fabs(self.motors[3].get_angle() - (150-angle)) < 1:
                    continue

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def translate(self, angle, distance):
        try:
            if distance > 0:
                inverse = 1
            else:
                inverse = -1

            sleepTime = (abs(distance)/(56.832*math.pi)) * 120
            self.crab_steering(angle)

            if angle == 90:

                self.motors[0].set_velocity(inverse*256)
                self.motors[3].set_velocity(-inverse*256)
                self.motors[1].set_velocity(-inverse*256)
                self.motors[2].set_velocity(inverse*256)
            else:
                self.drive(inverse*256)

            time.sleep(sleepTime)

            self.drive(0)

            self.center()

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def center_axis(self, angle):
        try:
            velocity = 256
            sleepTime = ((math.radians(abs(angle)))/(math.pi))*44.75

            self.center()

            self.four_wheel_turn()

            if angle > 0:
                self.motors[0].set_velocity(-velocity)
                self.motors[3].set_velocity(velocity)
                self.motors[1].set_velocity(-velocity)
                self.motors[2].set_velocity(velocity)
            else:
                self.motors[0].set_velocity(velocity)
                self.motors[3].set_velocity(-velocity)
                self.motors[1].set_velocity(velocity)
                self.motors[2].set_velocity(-velocity)

            time.sleep(sleepTime)

            self.center()
            self.drive(0)

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def expandy_boi(self):
        try:
            self.translate(0, -3)

            sleepTime = (abs(22.5)/(28.416*math.pi)) * 60
            self.crab_steering(90)

            self.motors[0].set_velocity(1023)
            self.motors[3].set_velocity(-200)
            self.motors[1].set_velocity(-1023)
            self.motors[2].set_velocity(200)

            time.sleep(sleepTime)

            self.drive(0)

            self.translate(90, 5)

            self.center()

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()
        self.center()

    def __init__(self, path):
        #self.badMsg = DebugMessages(self)
        self.motors = []
        for i in range(0, 4):
            if i < 2:
                self.motors.append(Motor(True, path))
            else:
                self.motors.append(Motor(False, path))
        self.drive(0)
        self.center()
        #self.badMsg.info("Done creating Robot object")
