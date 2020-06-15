from Robot.Motor import *
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

    def fourWheelTurn(self):
        normalAngle = 8.993
        try:
            self.motors[1].setAngle(normalAngle)
            self.motors[2].setAngle(-normalAngle)
            self.motors[0].setAngle(-normalAngle)
            self.motors[3].setAngle(normalAngle)

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def diffTurn(self):
        self.motors[0].setVelocity(-512)
        self.motors[1].setVelocity(-512)
        self.motors[2].setVelocity(512)
        self.motors[3].setVelocity(512)

    def crabSteering(self,angle):
        try:
            if angle == 0:
                self.center()
            elif angle == 90:
                self.motors[1].setAngle(angle)
                self.motors[2].setAngle(-angle)
                self.motors[0].setAngle(-angle)
                self.motors[3].setAngle(angle)
            else:
                self.motors[1].setAngle(-angle)
                self.motors[2].setAngle(-angle)
                self.motors[0].setAngle(-angle)
                self.motors[3].setAngle(-angle)

                while math.fabs(self.motors[3].getAngle() - (150 - angle)) < 1 :
                    continue

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def ackermannTurn(self,angle):
        length = 5.5
        width = 35.125
        # timeSleep = (math.radians(angle)*5.5)/(4*((math.cos(math.radians(45))*28)/60))
        radAngle = math.radians(angle)
        numerator = 2*length *math.sin(radAngle)
        inner = (2*length*math.cos(angle)) - (width*math.sin(angle))
        outer = (2*length*math.cos(angle)) + (width*math.sin(angle))

        self.motors[1].toggleTorque()
        self.motors[2].toggleTorque()

        if angle > 0:
            self.motors[1].setAngle(math.degrees(math.atan(numerator/inner)))
            self.motors[2].setAngle(-math.degrees(math.atan(numerator/outer)))
        else:
            self.motors[1].setAngle(math.degrees(math.atan(numerator/outer)))
            self.motors[2].setAngle(-math.degrees(math.atan(numerator/inner)))


        # self.motors[0].setVelocity(256)
        # self.motors[1].setVelocity(512)
        # self.motors[2].setVelocity(512)
        # self.motors[3].setVelocity(256)

        # time.sleep(5)
        #
        # self.drive(0)

        return None

    def translate(self,angle,distance):
        try:
            if distance > 0:
                inverse = 1
            else:
                inverse = -1

            sleepTime = (abs(distance)/(56.832*math.pi)) * 120


            self.crabSteering(angle)

            if angle == 90:

                self.motors[0].setVelocity(inverse*256)
                self.motors[3].setVelocity(-inverse*256)
                self.motors[1].setVelocity(-inverse*256)
                self.motors[2].setVelocity(inverse*256)
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

    def centerAxis(self,angle):
        try:
            velocity = 256
            sleepTime = ((math.radians(abs(angle)))/(math.pi))*44.75

            self.center()

            self.fourWheelTurn()

            if angle > 0:
                self.motors[0].setVelocity(-velocity)
                self.motors[3].setVelocity(velocity)
                self.motors[1].setVelocity(-velocity)
                self.motors[2].setVelocity(velocity)
            else:
                self.motors[0].setVelocity(velocity)
                self.motors[3].setVelocity(-velocity)
                self.motors[1].setVelocity(velocity)
                self.motors[2].setVelocity(-velocity)

            time.sleep(sleepTime)

            self.center()
            self.drive(0)

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()


    def expandyBoi(self):
        try:
            self.translate(0,-3)

            sleepTime = (abs(22.5)/(28.416*math.pi)) * 60


            self.crabSteering(90)

            self.motors[0].setVelocity(1023)
            self.motors[3].setVelocity(-200)
            self.motors[1].setVelocity(-1023)
            self.motors[2].setVelocity(200)

            time.sleep(sleepTime)

            self.drive(0)

            self.translate(90,5)

            self.center()

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()
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
