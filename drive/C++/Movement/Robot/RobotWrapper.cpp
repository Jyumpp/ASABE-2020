#include <python3.6/Python.h>
#include <pybind11/pybind11.h>
# include"Robot.h"

namespace py = pybind11;

//Wrapper for Python, magic that I do not understand (FRAGILE)
PYBIND11_MODULE(RobotWrapper, m) {
  py::class_<Robot>(m, "Robot")
      .def(py::init<std::string>())
      .def("drive",&Robot::drive)
      .def("center", &Robot::center)
      .def("crabSteering",&Robot::crabSteering)
      .def("turn",&Robot::turn)
      .def("translate",&Robot::translate)
      .def("centerAxisTurn",&Robot::centerAxisTurn)
      .def("expandyBoi",&Robot::expandyBoi)
      ;
}
