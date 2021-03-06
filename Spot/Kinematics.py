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
# LegPosition.py                                                #
# This file calculates the requires servo angles to move a foot #
# to a given position.                                          #
#                                                               #
#################################################################
import math
print "Starting the leg calculation Functions"

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
# Wrist: 0 - 135 degrees. 0 degrees is straight.                #
# Arm: 0 - 180 degrees. 90 is straight down.                    #
# Shoulder: 45 - 125 degrees. 90 is with the leg straigt down.  #
# Just for clarity, I will define the Axis we will use here:    #
# X: is from side to side of the robot. Left is negative.       #
# Y: is from the back to Front of the robot. Back is negative.  #
# Z: is from top to bottom of the robot. Down is negative.      #
#                                                               #
#################################################################
# Lets first define the functions that we need to do our math.  #
# Lets make a couple of assumptions, each angle is opposite the #
# length in out triangle.  We can also assume we will always    #
# have two of the lengths in our triangle and either at least   #
# one angle or the third length.                                #
#################################################################
def LengthC(AngleC, LengthA, LengthB):
    return math.sqrt(LengthA*LengthA + LengthB*LengthB - 2*LengthA*LengthB*math.cos(math.radians(AngleC)))

def JointAngle(LengthA, LengthB, LengthC):
    return math.degrees(math.acos((LengthA*LengthA + LengthB*LengthB - LengthC*LengthC)/(2*LengthA*LengthB)))

#################################################################
# Value where the forwardkinematics will save.                  #
#################################################################
workX = 0
workY = 0
workZ = 0
#################################################################
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# Shoulder, Arm and Wrist are the current positions.            #
#################################################################
def forwardKinematics(Leg, Shoulder, Arm, Wrist):
    global workX
    global workY
    global workZ
    LTF = LengthC(Wrist, LWF, LTW)
    AFW = JointAngle(LTF, LTW, LWF)
    if Leg < 2:
        workY = LTF * math.sin(math.radians(Arm-AFW-90)) + LYS
    else:
        workY = LTF * math.sin(math.radians(Arm-AFW-90)) - LYS
    LTFa = math.cos(math.radians(AFW + Arm + 90)) * LTF
    LSF = math.sqrt(LST*LST + LTFa*LTFa)
    if (Leg == 0) or (Leg == 2):
        workX = -math.sin(math.acos(LST/LSF)+math.radians(Shoulder))*LSF - LXS
    else:
        workX = math.sin(math.acos(LST/LSF)+math.radians(Shoulder))*LSF + LXS
    workZ = math.cos(math.acos(LST/LSF) + math.radians(Shoulder))*LSF

WorkServoS = 90
WorkServoA = 90
WorkServoW = 90

def LeginverseKinematics(LSFx, LAFy, Zt):
    # all inputs x, y, and z are relative to the shoulder joint.
    # we will assume the offsets from the center of the bot have already been applied.
    global WorkServoS
    global WorkServoA
    global WorkServoW
    # Lets first work out the length between the shoulder joint and the foot
    LSF = math.sqrt((LSFx*LSFx) + (Zt*Zt))
    # Now that we have LSF and we know LST, lets work out the LTFz
    # we use the z suffix here, because this only relative to the X-Z plane and not the XY plane
    LTFz = math.sqrt(LSF*LSF - LST*LST)
    Ai = math.asin(LSFx/LSF)
    Ao = math.acos(LST/LSF)
    WorkServoS = math.degrees(Ai + Ao) - 90
    LTF = math.sqrt((LTFz*LTFz) + (LAFy*LAFy))
    WorkServoW = math.degrees(math.acos((LTW*LTW + LWF*LWF - LTF*LTF)/(2*LTW*LWF)))
    Afw = math.asin((math.sin(math.radians(WorkServoW))*LWF)/LTF)
    Af = math.acos(LTFz/LTF)
    WorkServoA = math.degrees(Afw+Af) - 90

def inverseKinematics(Leg, Xt, Yt, Zt):

def FL_Leg(data):
    global FL_X
    global FL_Y
    global FL_Z
    forwardKinematics(0, FLShoulder.getCurrentInputPos(), FLArm.getCurrentInputPos()+180, FLWrist.getCurrentInputPos())
    FL_X = workX
    FL_Y = workY
    FL_Z = workZ
    print "Front-Left-Leg"
    print data

def FR_Leg(data):
    global FR_X
    global FR_Y
    global FR_Z
    forwardKinematics(1, FRShoulder.getCurrentInputPos(), FRArm.getCurrentInputPos()+180, FRWrist.getCurrentInputPos())
    FR_X = workX
    FR_Y = workY
    FR_Z = workZ
    print "Front-Right-Leg"
    print data

def BL_Leg(data):
    global BL_X
    global BL_Y
    global BL_Z
    forwardKinematics(2, BLShoulder.getCurrentInputPos(), BLArm.getCurrentInputPos()+180, BLWrist.getCurrentInputPos())
    BL_X = workX
    BL_Y = workY
    BL_Z = workZ
    print "Back-Left-Leg"
    print data

def BR_Leg(data):
    global BR_X
    global BR_Y
    global BR_Z
    forwardKinematics(3, BRShoulder.getCurrentInputPos(), BRArm.getCurrentInputPos()+180, BRWrist.getCurrentInputPos())
    BR_X = workX
    BR_Y = workY
    BR_Z = workZ
    print "Back-Right-Leg"
    print data

python.subscribe('FLShoulder', 'publishServoMoveTo', 'python', 'FL_Leg')
python.subscribe('FLArm', 'publishServoMoveTo', 'python', 'FL_Leg')
python.subscribe('FLWrist', 'publishServoMoveTo', 'python', 'FL_Leg')

python.subscribe('FRShoulder', 'publishServoMoveTo', 'python', 'FR_Leg')
python.subscribe('FRArm', 'publishServoMoveTo', 'python', 'FR_Leg')
python.subscribe('FRWrist', 'publishServoMoveTo', 'python', 'FR_Leg')

python.subscribe('BLShoulder', 'publishServoMoveTo', 'python', 'BL_Leg')
python.subscribe('BLArm', 'publishServoMoveTo', 'python', 'BL_Leg')
python.subscribe('BLWrist', 'publishServoMoveTo', 'python', 'BL_Leg')

python.subscribe('BRShoulder', 'publishServoMoveTo', 'python', 'BR_Leg')
python.subscribe('BRArm', 'publishServoMoveTo', 'python', 'BR_Leg')
python.subscribe('BRWrist', 'publishServoMoveTo', 'python', 'BR_Leg')


forwardKinematics(0, FLShoulder.getCurrentInputPos(), FLArm.getCurrentInputPos()+180, FLWrist.getCurrentInputPos())
print FLShoulder.getCurrentInputPos(), "FL Shoulder = ", FLArm.getCurrentInputPos(), ", FL Arm = ", FLWrist.getCurrentInputPos(), ", FL Wrist = "
print workX, "X = ", workY, ", Y = ", workZ, ", Z = "
