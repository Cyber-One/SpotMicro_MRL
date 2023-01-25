#################################################################
#                                                               #
# Program Code for Spot Micro MRL                               #
# Of the Cyber_One YouTube Channel                              #
# https://www.youtube.com/cyber_one                             #
#                                                               #
# This is version 0.1                                           #
# Divided up into sub programs                                  #
# Coded for the Nixie Version of MyRobotLab.                    #
#                                                               #
# Running on MyRobotLab (MRL) http://myrobotlab.org/            #
# Spot Micro MRL is a set of Python scripts that run inside     #
# the MRL system                                                #
#                                                               #
# .py                                                           #
# This file is a group of commands that perform actions         #
#                                                               #
#################################################################
import time
import math
print "Starting Balance Kinematics Services"
# This version of the kinematics also takes into account the
# tilt and roll of the robot.
# In this version we consider the center of mass of the robot
# to be an additional joint for each of the feet with a fixed
# origin of 0,0,0.
# This means the ground will be below the robot and the point
# of balance will there for always be at 0,0 in the X-Y plane.
# We will do the Forward Kinematics first as it is the easier
# one to do.
# Since we have already done the hard work of figuring out
# where the feet are in relation to the robots body relative
# to the body's rotational plane, we can use that info to work
# out the position of the feet relative to the rotated origin
# in the robot.
# Like the first Forward Kinematics, we will be using
# Trianlges to get some basic info.
def imuForwardKinematics(Shoulder, Arm, Wrist):
    LTF = math.sqrt(LWF*LWF + LTW*LTW - 2*LWF*LTW*math.cos(math.radians(Wrist)))
    AFW = math.degrees(math.acos((LTF*LTF + LTW*LTW - LWF*LWF)/(2*LTF*LTW)))
    workY = LTF * math.sin(math.radians(Arm-AFW-90))
    LTFa = math.cos(math.radians(AFW - Arm - 90)) * LTF
    LSF = math.sqrt(LST*LST + LTFa*LTFa)
    workX = math.sin(math.acos(LST/LSF)+math.radians(Shoulder))*LSF
    workZ = math.cos(math.acos(LST/LSF) + math.radians(Shoulder))*LSF
