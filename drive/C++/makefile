test: LineCorrection.o Linetracking.o Robot.o Motor.o
	g++ -o test LineCorrection/LineCorrection.o LineTracking/LineTracking.o Movement/Robot/Robot.o Moveemnt/Motor/Motor.o
LineCorrection.o: Robot.o Linetracking.o Linecorrection.cpp
	g++ -c LineCorrection/LineCorrection.cpp
Robot.o: Motor.o Movement/Robot/Robot.cpp
	g++ -c Movement/Robot/Robot.cpp
Motor.o: Movement/Motor/Motor.cpp
	g++ -c Movement/Motor/Motor.cpp
