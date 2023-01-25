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
print ("Starting the leg calculation Functions")

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
# LAW: length between the Arm joint and the Wrist joint.        #
# LSA: length between the shoulder joint and the Arm joint.     #
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
# Y: is from the front to back of the robot. Back is negative.  #
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

def AngleC(LengthA, LengthB, LengthC):
    return math.degrees(math.acos((LengthA*LengthA + LengthB*LengthB - LengthC*LengthC)/(2*LengthA*LengthB)))

#################################################################
#                                                               #
# Foward Kinematics                                             #
#                                                               #
#################################################################
# First thing we need to know is the length of the leg between  #
# the Arm and the foot, let call that LAF (Length Arm Foot),    #
# but we have four legs to deal with, so we will preface each   #
# one with a 2 leter indentifier to help, FL (Front Left),      #
# FR (Front Right), BL (Back Left), BR (Back Right).            #
#################################################################
FLLAF = LengthC(FLWrist.currentOutputPos, LAW, LWF)
FRLAF = LengthC(FRWrist.currentOutputPos, LAW, LWF)
BLLAF = LengthC(BLWrist.currentOutputPos, LAW, LWF)
BRLAF = LengthC(BRWrist.currentOutputPos, LAW, LWF)

#################################################################
# The direction the foot is from the arm is not always the      #
# angle set by the Arm servo.  We need to calculate the offset  #
# then add that to the servo position.  We will call this AAF   #
# (Angle Arm Foot).  Again we will prefix with the leg code.    #
#################################################################
FLAAF = FLArm.currentOutputPos + AngleC(FLLAF, LAW, LWF)
FRAAF = FRArm.currentOutputPos + AngleC(FRLAF, LAW, LWF)
BLAAF = BLArm.currentOutputPos + AngleC(BLLAF, LAW, LWF)
BRAAF = BRArm.currentOutputPos + AngleC(BRLAF, LAW, LWF)

#################################################################
# Now we have the length and angle in 2 dimension, we need to   #
# add in the third dimension to get the current location.       #
# the last two calculation were based in the shoulders output   #
# plane, but we need it in the XYZ plane, that make LAF the     #
# hypotenuse of a right angle triangle.                         #
# Lets work out the Y axis first since the shoulder joint can't #
# affect that axis.                                             #
#################################################################
FLY = FLLAF * math.sin(math.radians(FLAAF-90)) + LYS
FRY = FLLAF * math.sin(math.radians(FRAAF-90)) + LYS
BLY = FLLAF * math.sin(math.radians(BLAAF-90)) - LYS
BRY = FLLAF * math.sin(math.radians(BRAAF-90)) - LYS

#################################################################
# Now we have the Y-Axis, work out the X Axis.                  #
# What complicates this a bit is the centerline of the leg is   #
# set out from the pivot point of the shoulder.  This forms a   #
# right angle triangel with the three points between the        #
# Shoulder pivot, the top of the leg and the foot.  The right   #
# angle is at the top of the leg.  The length between the       #
# Shoulder pivot and the top of the leg is fixed. LSA           #
# (Length Shoulder Arm) and we know the length from the top of  #
# the leg to the foot LAF (Length Arm Foot), so we can          #
# calculate the length between the Shoulder pivot and the Foot  #
# (LSF - Length Shoulder Foot).                                 #
#################################################################
FLLSF = math.sqrt(LSA*LAS + FLLAF*FLLAF)
FRLSF = math.sqrt(LSA*LAS + FRLAF*FRLAF)
BLLSF = math.sqrt(LSA*LAS + BLLAF*BLLAF)
BRLSF = math.sqrt(LSA*LAS + BRLAF*BRLAF)

#################################################################
# We also need the angle the LSF is at relative the to          #
# Shoulder-Arm line.  For this we can use either the Sin() or   #
# the Cos() formula to work it out.  I'll use the Cos() as one  #
# of the measuerments is pretty much fixed :-)  We are going to #
# need this angle for both the X and the Z positions.           #
# Lets call this ASF (Angle Shoulder Foot) and includes the     #
# shoulder servo position.                                      #
#################################################################
FLASF = FLShoulder.currentOutputPos + math.cos(LSA/FLLSF)
FRASF = FLShoulder.currentOutputPos + math.cos(LSA/FRLSF)
BLASF = FLShoulder.currentOutputPos + math.cos(LSA/BLLSF)
BRASF = FLShoulder.currentOutputPos + math.cos(LSA/BRLSF)

#################################################################
# We should now have everything we need to work out the X-Axis  #
# foot position.  Just a bit more Tigonometry. :-)              #
#################################################################
FLX = FLLAF * math.sin(FLASF)

FLY = FLLAF * math.cos(FLASF)

#################################################################
#                                                               #
# Inverse Kinematics                                            #
#                                                               #
#################################################################

def WristServoPosLegLength(length):
