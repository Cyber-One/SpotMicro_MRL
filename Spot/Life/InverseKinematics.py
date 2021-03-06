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
# InverseKinematics.py                                          #
# This file calculates the requires servo angles to move a foot #
# to a given position.                                          #
#                                                               #
#################################################################
import math
print "Starting the Inverse Kinematics Functions"

#################################################################
# legInverseKinematics(X-Axis, Y-Axis, Z-Axis)                  #
# Parameters:                                                   #
#   X-Axis, Y-Axis, Z-Axis are the coordinates in mm relative   #
#   to the cetre of the shoulder joint.                         #
# Returned is library containing:                               #
#   Error = 0 is all ok, a value > 0 indicates an error and a   #
#        move should not be made.                               #
#   Shoulder position to set the servo for the set destination. #
#   Arm position to set the servo for the set destination.      #
#   Wrist position to set the servo for the set destination.    #
# Error Codes:                                                  #
#   0 = No Error.                                               #
#   1 = Result would set Shoulder servo to less than Min Pos.   #
#   2 = Result would set Shoulder servo to more than Max Pos.   #
#   3 = Result would set Arm servo to less than Min Pos.        #
#   4 = Result would set Arm servo to more than Max Pos.        #
#   5 = Result would set Wrist servo to less than Min Pos.      #
#   6 = Result would set Wrist servo to more than Max Pos.      #
#   7 = LTF is longer than LTW and LWF combined, Not possible.  #
#################################################################
def legInverseKinematics(LSFx, LAFy, Zt):
    Error = 0
    #print LSFx, ", LSFx:", LAFy, ", LAFy:", Zt, "Zt:"
    # we will assume the offsets from the center of the bot have already been applied.
    # Lets first work out the length between the shoulder joint and the foot
    LSF = math.sqrt((LSFx*LSFx) + (Zt*Zt))
    # Now that we have LSF and we know LST, lets work out the LTFz
    # we use the z suffix here, because this only relative to the X-Z plane and not the XY plane
    # LST = 50
    LTFz = math.sqrt(LSF*LSF - LST*LST)
    Ai = math.asin(LSFx/LSF) # Angle inside
    Ao = math.acos(LST/LSF)  # Angle Outside
    ServoS = 180 - math.degrees(Ai + Ao)
    #print ServoS, ", ServoS:", math.degrees(Ai), ", Ai:", math.degrees(Ao), "Ao:"
    if ServoS < ShoulderMin:
        Error = 1
        ServoS = ShoulderMin
    if ServoS > ShoulderMax:
        Error = 2
        ServoS = ShoulderMax
    LTF = math.sqrt((LTFz*LTFz) + (LAFy*LAFy))
    if (LTW+LWF) < LTF:
        #print "Warning, LTF is longer than LTW and LWF combined, this is impossible"
        Error = 7
        ServoA = 0
        ServoW = 0
    else:
        #print LTFz, ", LTFz:", LTF, ", LTF:", ((LTW*LTW) + (LWF*LWF) - (LTF*LTF))/(2*LTW*LWF), "C:"
        ServoWR = math.acos(((LTW*LTW) + (LWF*LWF) - (LTF*LTF))/(2*LTW*LWF))
        ServoW = math.degrees(ServoWR)
        #print ServoW, "ServoW:"
        if ServoW < WristMin:
            Error = 5
            ServoW = WristMin
        if ServoW > WristMax:
            Error = 6
            ServoW = WristMax
        Afw = math.asin((math.sin(math.radians(ServoW))*LWF)/LTF)
        if LAFy>0:
            Af = math.acos(LTFz/LTF)
        else:
            Af = -math.acos(LTFz/LTF)
        ServoA = math.degrees(Afw - Af) + 90
        #print ServoA, ", ServoA:", Afw, ", Afw:", Af, "Af:"
        if ServoA < ArmMin:
            Error = 3
            ServoA = ArmMin
        if ServoA > ArmMax:
            Error = 4
            ServoA = ArmMax
    return {"Error":Error, "Shoulder":ServoS, "Arm":ServoA, "Wrist":ServoW}


#################################################################
# moveFoot( Leg, X-Axis, Y-Axis, Z-Axis)                        #
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# X-Axis, Y-Axis, Z-Axis is the amount in mm to move the foot   #
#   in that axis. A negative value will move it in the reverse  #
#   direction.                                                  #
# This function first works out the current foot position,      #
# then calculate the new position by adding the X, Y and Z      #
# inputs to work out the new abosulte position using the        #
# legInverseKinematics function.                                #
# If an error during calculation occurs, then no movement is    #
# performed on any servo.                                       #
#################################################################
def moveFoot(Leg, X, Y, Z):
    if Leg == 0: # Front Left
        FL_Leg(0)
        ServoPos = legInverseKinematics(FL_X+LXS + X, FL_Y-LYS + Y, FL_Z + Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            FLShoulder.moveTo(ServoPos.get("Shoulder"))
            FLArm.moveTo(ServoPos.get("Arm"))
            FLWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 1: # Front Right
        FR_Leg(0)
        ServoPos = legInverseKinematics((FR_X-LXS) + X, (FR_Y-LYS) + Y, FR_Z + Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            FRShoulder.moveTo(ServoPos.get("Shoulder"))
            FRArm.moveTo(ServoPos.get("Arm"))
            FRWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 2: # Back Left
        BL_Leg(0)
        ServoPos = legInverseKinematics(BL_X+LXS + X, BL_Y+LYS + Y, BL_Z + Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            BLShoulder.moveTo(ServoPos.get("Shoulder"))
            BLArm.moveTo(ServoPos.get("Arm"))
            BLWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 3: # Back Right
        BR_Leg(0)
        ServoPos = legInverseKinematics(BR_X-LXS + X, BR_Y+LYS + Y, BR_Z + Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            BRShoulder.moveTo(ServoPos.get("Shoulder"))
            BRArm.moveTo(ServoPos.get("Arm"))
            BRWrist.moveTo(ServoPos.get("Wrist"))
        
#################################################################
# setServosInverseKinematics( Leg, X-Axis, Y-Axis, Z-Axis)      #
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# X-Axis, Y-Axis, Z-Axis is the coordinate of the foot relative #
# to the center of the robot that we want to move the foot to.  #
#################################################################
def setServosInverseKinematics(Leg, X, Y, Z):
    if Leg == 0: # Front Left
        #FL_Leg(0)
        ServoPos = legInverseKinematics(X - LXS, Y - LYS, Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            FLShoulder.moveTo(ServoPos.get("Shoulder"))
            FLArm.moveTo(ServoPos.get("Arm"))
            FLWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 1: # Front Right
        #FR_Leg(0)
        ServoPos = legInverseKinematics(-(X+LXS), Y - LYS, Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            FRShoulder.moveTo(ServoPos.get("Shoulder"))
            FRArm.moveTo(ServoPos.get("Arm"))
            FRWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 2: # Back Left
        #BL_Leg(0)
        ServoPos = legInverseKinematics(X - LXS, Y + LYS, Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            BLShoulder.moveTo(ServoPos.get("Shoulder"))
            BLArm.moveTo(ServoPos.get("Arm"))
            BLWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 3: # Back Right
        #BR_Leg(0)
        ServoPos = legInverseKinematics(-(X+LXS), Y + LYS, Z)
        # Error trapping, only move if no error occured
        if ServoPos.get("Error") == 0:
            BRShoulder.moveTo(ServoPos.get("Shoulder"))
            BRArm.moveTo(ServoPos.get("Arm"))
            BRWrist.moveTo(ServoPos.get("Wrist"))

