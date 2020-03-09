test: linecorrection.o linetracking.o
    g++ -o test linecorrection.o linetracking.o robot.o motor.o
linecorrection.o: robot.o linetracking.o linecorrection.cpp
    g++ -c LineCorrection.cpp
robot.o: motor.o robot.cpp
    g++ -c robot.cpp
motor.o: motor.cpp
    g++ -c motor.cpp
