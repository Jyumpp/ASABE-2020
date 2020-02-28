from Motor import *
import time
import math

class Robot:
    motors = []
    velocity = 0

    def diffDrive(self):
        while True:
            time.sleep(1)
            if motor[0].getVelocity() == 0 or None:
                continue
            i = 0
            motorPosition = [0,0,0,0]
            for motor in self.motors:
                motorPosition[i] = motorPosition[i] + motor.getVelocity()
                i = i + 1
            max = motorPosition.max()
            ratio = motor[0].getVelocity()/1023
            for motor in self.motors:
                motor.drive((motor.getVelocity() + (abs(max-motor.getVelocity()))/17.05))

    def drive(self,velocity):
        try:
            for motor in self.motors:
                motor.setVelocity(velocity)
            return None
        except:
            print(e)
            self.center()

    def center(self):
        try:
            for motor in self.motors:
                motor.center()
            print(self.motors[3].getAngle() - 150)
            while self.motors[3].getAngle() - 150 < -.75:
                continue

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def diff(self):
        try:
            self.motors[1].setAngle(13.101)
            self.motors[2].setAngle(-13.101)
            self.motors[0].setAngle(-13.101)
            self.motors[3].setAngle(13.101)

            while self.motors[3].getAngle() - (150 - 13.101) < -.75:
                continue

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def crabSteering(self,angle):
        try:
            self.motors[1].setAngle(angle)
            self.motors[2].setAngle(-angle)
            self.motors[0].setAngle(-angle)
            self.motors[3].setAngle(angle)

            while self.motors[3].getAngle() - (150 - angle) > -.75 :
                continue

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def turnLeft(self,angle):
        # timeSleep = (math.radians(angle)*5.5)/(4*((math.cos(math.radians(45))*28)/60))

        self.diff()


        self.motors[1].toggleAngle()
        self.motors[2].toggleAngle()
        self.motors[0].setVelocity(512)
        self.motors[3].setVelocity(512)

        # self.motors[2].drive(512)

        time.sleep(1)

        self.drive(0)

        return None

    def turnRight(self,angle):
        timeSleep = (math.radians(angle)*5.5)/(4*((math.cos(math.radians(45))*28)/60))

        for motor in self.motors:
            self.ackermann(-111.251)

        time.sleep(1.6)

        self.motors[0].drive(-int(512.0*.43715))

        self.motors[3].drive(int(512.0*.43715))

        self.motors[1].drive(512)

        self.motors[2].drive(-512)

        return None

    def translate(self,angle,distance):
        try:
            if distance > 0:
                inverse = 1
            else:
                inverse = -1

            sleepTime = (abs(distance)/(56.832*math.pi)) * 60

            self.center()

            self.crabSteering(angle)

            self.motors[0].setVelocity(inverse*512)
            self.motors[3].setVelocity(-inverse*512)
            self.motors[1].setVelocity(-inverse*512)
            self.motors[2].setVelocity(inverse*512)

            time.sleep(sleepTime)

            self.drive(0)

            self.center()

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def centerAxis(self,angle):
        try:
            sleepTime = ((math.radians(abs(angle)))/(math.pi))*19.75

            self.center()

            self.diff()

            if angle > 0:
                self.motors[0].setVelocity(-512)
                self.motors[3].setVelocity(512)
                self.motors[1].setVelocity(-512)
                self.motors[2].setVelocity(512)
            else:
                self.motors[0].setVelocity(512)
                self.motors[3].setVelocity(-512)
                self.motors[1].setVelocity(512)
                self.motors[2].setVelocity(-512)

            time.sleep(sleepTime)

            self.drive(0)
            self.center()

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def __init__(self,path):
        self.motors = []
        for i in range(0,4):
            if i < 2:
                self.motors.append(Motor(True,path))
            else:
                self.motors.append(Motor(False,path))
        self.drive(0)
        self.center()
