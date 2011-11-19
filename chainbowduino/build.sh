#!/bin/bash
export ARDUINO_HOME=$HOME/src/arduino/arduino-0022
scons ARDUINO_HOME=$ARDUINO_HOME "$@"
