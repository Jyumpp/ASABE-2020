test: LineCorrection.o Linetracking.o Robot.o Motor.o
	g++ -std=c++11 -o test LineCorrection/LineCorrection.o LineTracking/LineTracking.o Movement/Robot/Robot.o Movement/Motor/Motor.o
LineCorrection.o: Robot.o Linetracking.o Linecorrection.cpp
	g++ -std=c++11 -c LineCorrection/LineCorrection.cpp
Robot.o: Movement/Motor/Motor.o Movement/Robot/Robot.cpp
	g++ -std=c++11 -c Movement/Robot/Robot.cpp
Motor.o: Movement/Motor/Motor.cpp
	g++ -std=c++11 -c Movement/Motor/Motor.cpp
