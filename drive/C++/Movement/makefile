robotWrapper: motor/motor.o Robot/robot.h Robot/robot.cpp
	c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` Robot/robot.cpp motor/motor.o -o Robot/robot`python3-config --extension-suffix`
motor.o: motor/motor.h
	c++ -c motor/motor.cpp
	mv motor.o motor/
