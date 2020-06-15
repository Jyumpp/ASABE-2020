#!/usr/bin/python3

import datetime

class DebugMessages:

    def __init__(self, classObject):

        if classObject is not None:
            
            self.className = classObject.__name__
            self.classID = id(classObject)

        else:
            self.className = "None"
            self.classID = 0

        # Initalizing the debug strings for easier printing
        self.infoStr = "[INFO]\t[" + self.className + "\tID=" + str(self.classID) + "]"
        self.debugStr = "[DEBUG]\t[" + self.className + "\tID=" + str(self.classID) + "]"
        self.warningStr = "[WARN]\t[" + self.className + "\tID=" + str(self.classID) + "]"
        self.errorStr = "[ERROR]\t[" + self.className + "\tID=" + str(self.classID) + "]"
        self.fatalStr = "[FATAL]\t[" + self.className + "\tID=" + str(self.classID) + "]"

    def info(self, message):

        currentDT = datetime.datetime.now()

        print(self.infoStr + "[" + "{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second) + "]: " + message)
              
    def debug(self, message):

        currentDT = datetime.datetime.now()

        print(self.debugStr + "[" + "{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second) + "]: " + message)

    def warning(self, message):

        currentDT = datetime.datetime.now()

        print(self.warningStr + "[" + "{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second) + "]: " +  message)

    def error(self, message):

        currentDT = datetime.datetime.now()

        print(self.errorStr + "[" + "{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second) + "]: " + message)

    def fatal(self, message):

        currentDT = datetime.datetime.now()

        print(self.fatalStr + "[" + "{0:d}{1:d}{2:d}-{3:d}{4:2d}{5:d}".format(currentDT.year, currentDT.month, currentDT.day, currentDT.hour, currentDT.minute, currentDT.second) + "]: " + message)
