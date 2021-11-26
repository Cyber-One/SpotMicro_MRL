#!/bin/bash

#############################################################
# Spot Unix Start Script 
# Usage:  ./start_spot.sh
# This will launch MyRobotLab and run the Spot/Start.py 
# default startup script
#############################################################

echo "------------------------------------------------------"
echo "               Spot Micro LAUNCHER"
echo "------------------------------------------------------"
echo "Rotate Log files for clean no worky logs"
echo "------------------------------------------------------"
rm myrobotlab.log.1
mv myrobotlab.log myrobotlab.log.1
echo "Done."
echo "------------------------------------------------------"
echo "START MRL & Spot
echo "------------------------------------------------------"
# start the Spot script
# Let look at this line and break it down a bit.
# We start the line with the executable "java"
# the -jar myrobotlab.jar is the name of the java file to be 
# run by java when it starts.
# -m 4g tell the java system to allocate 4 Giga bytes of 
# Random Access Memory (RAM) to the java system.
# --service python Python is passes to the myrobotlab.jar 
# program, telling it to sert the Python service and name it python
# --invoke python execFile ./Spot/Start.py thells the myrobotlab.jar 
# program to use the python service and execute the file with the 
# path starting in the current directory look in the sub 
# directory "Spot" for the file "Start.py"
java -jar myrobotlab.jar -m 4g --service python Python --invoke python execFile ./Spot/Start.py

