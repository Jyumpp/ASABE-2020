from Motor import *
import time
import math
class Robot:
    motors = []
    velocity = 0

    #Sets Robot drive motors to velocity
    def drive(self,velocity):
        try:
            self.center()
            for motor in self.motors:
                motor.setVelocity(velocity)
            return None
        except Exception as e:
            print(e)
            self.center()

    #Sets the Robot angle motors to home angle(150)
    def center(self):
        try:
            for motor in self.motors:
                motor.center()
            # print(self.motors[3].getAngle() - 150)
            while math.fabs(self.motors[3].getAngle() - 150) < 1:
                continue

            return None
        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    #Turns drive motors to be normal to center axis
    def diff(self):
        try:
            self.motors[1].setAngle(13.101)
            self.motors[2].setAngle(-13.101)
            self.motors[0].setAngle(-13.101)
            self.motors[3].setAngle(13.101)

            while self.motors[3].getAngle() - (150 - 13.101) < -.5:
                continue

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def crabSteering(self,angle):
        try:
            if angle == 0:
                self.center()
            else:
                self.motors[1].setAngle(angle)
                self.motors[2].setAngle(-angle)
                self.motors[0].setAngle(-angle)
                self.motors[3].setAngle(angle)

                while self.motors[3].getAngle() - (150 - angle) > -.5 :
                    continue

        except Exception as e:
            print(e)
            self.drive(0)
            self.center()

    def ackermannTurn(self,angle):
        length = 11.25
        width = 36.125
        # timeSleep = (math.radians(angle)*5.5)/(4*((math.cos(math.radians(45))*28)/60))
        angle = math.radians(angle)
        numerator = 2*length *math.sin(angle)
        if angle > 0:
            self.motor[1].setAngle(math.arctan(numerator/(2*length*cos(angle)-width*sin(angle)))
            self.motor[2].setAngle(math.arctan(numerator/(2*length*cos(angle)+width*sin(angle)))
        else:
            self.motor[1].setAngle(math.arctan(numerator/(2*length*cos(angle)+width*sin(angle)))
            self.motor[2].setAngle(math.arctan(numerator/(2*length*cos(angle)-width*sin(angle)))


        self.motors[1].setAngle((2*length*math.sin(radAngle))/(2*length*math.cos(radAngle)+width*math.sin(radAngle)))
        self.motors[2].setAngle((2*length*math.sin(radAngle))/(2*length*math.cos(radAngle)-width*math.sin(radAngle)))


        # self.drive(512)

        time.sleep(5)

        self.drive(0)

        return None

    def translate(self,angle,distance):
        try:
            if distance > 0:
                inverse = 1
            else:
                inverse = -1

            sleepTime = (abs(distance)/(56.832*math.pi)) * 120


            self.crabSteering(angle)

            self.motors[0].setVelocity(inverse*256)
            self.motors[3].setVelocity(-inverse*256)
            self.motors[1].setVelocity(-inverse*256)
            self.motors[2].setVelocity(inverse*256)

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
            sleepTime = ((math.radians(abs(angle)))/(math.pi))*74

            self.center()

            self.diff()

            if angle > 0:
                self.motors[0].setVelocity(-128)
                self.motors[3].setVelocity(128)
                self.motors[1].setVelocity(-128)
                self.motors[2].setVelocity(128)
            else:
                self.motors[0].setVelocity(128)
                self.motors[3].setVelocity(-128)
                self.motors[1].setVelocity(128)
                self.motors[2].setVelocity(-128)

            time.sleep(sleepTime)

            self.drive(0)
            self.center()

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
            self.motors[3].setVelocity(-230)
            self.motors[1].setVelocity(-1023)
            self.motors[2].setVelocity(230)

            time.sleep(sleepTime)

            self.drive(0)
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
