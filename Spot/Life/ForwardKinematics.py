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
# ForwardKinematics.py                                          #
# This file calculates the current position of each foot using  #
# the current servo position.                                   #
#                                                               #
#################################################################
import math
print "Starting the leg Forward Kinematics Functions"

#################################################################
#                                                               #
# There are a number of ways of calculating the current foot    #
# position, one of the more popular ways is to use the          #
# Kinematic model.  Converseley, planning how to set the joints #
# to place the foot in a set position is known as Inverse       #
# Kinematics or IK.                                             #
# There are a number of very complex methods of performing thes #
# calculations, but this tends to hide the simple maths of      #
# Tigonometry.  For this reason, I'm going to use the basic     #
# maths so that you can follow along more easily.               #
# Lets start with the foot and first joint.  For this we will   #
# be using the two formula know as the Law of Cosines.          #
# Just a note, when looking at the labels on a triangle, the    #
# angle is on the opposite side to the same named length.       #
# The following formula use lower case as the length and upper  #
# case as the angle.                                            #
# c = sqrt(a*a + b*b -2*a*b*cos(C))                             #
# C = acos((a*a + b*b - c*c)/(2*a*b))                           #
#                                                               #
# When calculating out the position of the foot, we know the    #
# following bits of the equation:                               #
# LWF: length of the leg between the Wrist joint and the foot.  #
# LTW: length between the Arm joint and the Wrist joint.        #
# LST: length between the shoulder joint and the Arm joint.     #
# LYS: Length between the center Y plane and the shoulder joint #
# LXS: Length between the center X plane and the shoulder joint #
# We also know the position of each of the servos, but each     #
# servo also has an allowable range. Based off this information #
# we can calculate the current position of the foot relative to #
# the center of the robot.  But just for clarity, lets list the #
# servo ranges.                                                 #
# Wrist: 40 - 180 degrees. 180 degrees is straight.             #
# Arm: 0 - 180 degrees. 90 is straight down.                    #
# Shoulder: 45 - 125 degrees. 90 is with the leg straigt down.  #
# Just for clarity, I will define the Axis we will use here:    #
# X: is from side to side of the robot. Left is negative.       #
# Y: is from the back to Front of the robot. Back is negative.  #
# Z: is from top to bottom of the robot. Down is negative.      #
# This is all from the robots perspective.                      #
#                                                               #
#################################################################
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# Shoulder, Arm and Wrist are the current positions.            #
#################################################################
def forwardKinematics(Shoulder, Arm, Wrist):
    LTF = math.sqrt(LWF*LWF + LTW*LTW - 2*LWF*LTW*math.cos(math.radians(Wrist)))
    AFW = math.degrees(math.acos((LTF*LTF + LTW*LTW - LWF*LWF)/(2*LTF*LTW)))
    workY = LTF * math.sin(math.radians(Arm-AFW-90))
    LTFa = math.cos(math.radians(AFW - Arm - 90)) * LTF
    LSF = math.sqrt(LST*LST + LTFa*LTFa)
    workX = math.sin(math.acos(LST/LSF)+math.radians(Shoulder))*LSF
    workZ = math.cos(math.acos(LST/LSF) + math.radians(Shoulder))*LSF
    return {"X":workX, "Y":workY, "Z":workZ}

def FL_Leg(data):
    global FL_X
    global FL_Y
    global FL_Z
    Position = forwardKinematics(FLShoulder.getCurrentInputPos(), FLArm.getCurrentInputPos()+180, FLWrist.getCurrentInputPos())
    FL_X = -Position.get("X") - LXS
    FL_Y = Position.get("Y") + LYS
    FL_Z = Position.get("Z")
    print "Front-Left-Leg"
    print FL_Z, " FL-Z:", FL_Y, " FL-Y:", FL_X, "FL-X:"

def FR_Leg(data):
    global FR_X
    global FR_Y
    global FR_Z
    Position = forwardKinematics(FRShoulder.getCurrentInputPos(), FRArm.getCurrentInputPos()+180, FRWrist.getCurrentInputPos())
    FR_X = Position.get("X") + LXS
    FR_Y = Position.get("Y") + LYS
    FR_Z = Position.get("Z")
    print "Front-Right-Leg"
    print FR_Z, " FR-Z:", FR_Y, " FR-Y:", FR_X, "FR-X:"

def BL_Leg(data):
    global BL_X
    global BL_Y
    global BL_Z
    Position = forwardKinematics(BLShoulder.getCurrentInputPos(), BLArm.getCurrentInputPos()+180, BLWrist.getCurrentInputPos())
    BL_X = -Position.get("X") - LXS
    BL_Y = Position.get("Y") - LYS
    BL_Z = Position.get("Z")
    print "Back-Left-Leg"
    print BL_Z, " BL-Z:", BL_Y, " BL-Y:", BL_X, "BL-X:"

def BR_Leg(data):
    global BR_X
    global BR_Y
    global BR_Z
    Position = forwardKinematics(BRShoulder.getCurrentInputPos(), BRArm.getCurrentInputPos()+180, BRWrist.getCurrentInputPos())
    BR_X = Position.get("X") + LXS
    BR_Y = Position.get("Y") - LYS
    BR_Z = Position.get("Z")
    print "Back-Right-Leg"
    print BR_Z, " BR-Z:", BR_Y, " BR-Y:", BR_X, "BR-X:"

#################################################################
# The routine assumes all the memory positions for the servos   #
# and feet position relative to the body are up to date.        #
# This can be achived by calling updateServoPositions() first.  #
#################################################################
def imuForwardKinematics():
    global Pitch
    global Roll
    global Yaw
    global CoMoffsetX
    global CoMoffsetY
    global CoMoffsetZ
    global FL_X
    global FR_X
    global BL_X
    global BR_X
    global FL_Y
    global FR_Y
    global BL_Y
    global BR_Y
    global FL_Z
    global FR_Z
    global BL_Z
    global BR_Z
    global imuFL_X
    global imuFR_X
    global imuBL_X
    global imuBR_X
    global imuFL_Y
    global imuFR_Y
    global imuBL_Y
    global imuBR_Y
    global imuFL_Z
    global imuFR_Z
    global imuBL_Z
    global imuBR_Z
    # Just to add to the confusion here, we have the center of 
    # the robot at the origin of 0,0,0. But your robot might 
    # have extra equipment attached on the top at the front 
    # such as an Arm, lidar sensor or a camera.  This additional
    # load will move the point of balance away from the center 
    # of origin.
    # When we built our kinematic model, we used the center of 
    # the robot as the origin, Now we need to work out the feet 
    # positions based on the center of mass (CoM)
    comFLX = FL_X - CoMoffsetX
    comFLY = FL_Y - CoMoffsetY
    comFLZ = FL_Z - CoMoffsetZ
    # Next lets work out the distance between the CoM and the feet
    FLxzL = math.sqrt((comFLX*comFLX)+(comFLZ*comFLZ))
    FLyzL = math.sqrt((comFLY*comFLY)+(comFLZ*comFLZ))
    # We also need to know the angle of the line between the CoM 
    # and the feet
    FLxA = asin(comFLX/FLxzL)
    FLyA = asin(comFLY/FLyzL)
    FLimuXA = FLxA + Roll
    FLimuYA = FLyA + Pitch
    imuFL_X = math.sin(FLimuXA)*FLxzL
    imuFL_Y = math.sin(FLimuYA)*FLYzL
    imuFL_Z = math.cos(FLimuYA)*FLYzL
