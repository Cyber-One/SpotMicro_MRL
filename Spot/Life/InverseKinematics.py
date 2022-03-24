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
# kinematicsSetServo(Leg, ServoPos, Speed)                      #
# This routine sets the speed of each of the servos for a leg   #
# to produce a straight line movement.                          #
#################################################################
def kinematicsSetServo(Leg, ServoPos, Speed):
    # First we need to know the current position.
    if Leg == 0:
        ShoulderCurrentPos = FLShoulder.getCurrentInputPos()
        ArmCurrentPos = FLArm.getCurrentInputPos()
        WristCurrentPos = FLWrist.getCurrentInputPos()
    elif Leg == 1:
        ShoulderCurrentPos = FRShoulder.getCurrentInputPos()
        ArmCurrentPos = FRArm.getCurrentInputPos()
        WristCurrentPos = FRWrist.getCurrentInputPos()
    elif Leg == 2:
        ShoulderCurrentPos = BLShoulder.getCurrentInputPos()
        ArmCurrentPos = BLArm.getCurrentInputPos()
        WristCurrentPos = BLWrist.getCurrentInputPos()
    elif Leg == 3:
        ShoulderCurrentPos = BRShoulder.getCurrentInputPos()
        ArmCurrentPos = BRArm.getCurrentInputPos()
        WristCurrentPos = BRWrist.getCurrentInputPos()
    # Next we need to know the offset from the current pos to
    # the new pos.
    ShoulderOffset = ServoPos.get("Shoulder") - ShoulderCurrentPos
    ArmOffset = ServoPos.get("Arm") - ShoulderCurrentPos
    WristOffset = ServoPos.get("Wrist") - ShoulderCurrentPos
    # Next we need to know, how long it will take for the servos
    # to reach the new position. 
    # We can get max speed from the Spot config
    if Leg == 0:
        ShoulderTime = ShoulderOffset / FLShoulderVelocity
        ArmTime = ArmOffset / FLArmVelocity
        WristTime = WristOffset / FLWristVelocity
    elif Leg == 1:
        ShoulderTime = ShoulderOffset / FRShoulderVelocity
        ArmTime = ArmOffset / FRArmVelocity
        WristTime = WristOffset / FRWristVelocity
    elif Leg == 2:
        ShoulderTime = ShoulderOffset / BLShoulderVelocity
        ArmTime = ArmOffset / BLArmVelocity
        WristTime = WristOffset / BLWristVelocity
    elif Leg == 3:
        ShoulderTime = ShoulderOffset / BRShoulderVelocity
        ArmTime = ArmOffset / BRArmVelocity
        WristTime = WristOffset / BRWristVelocity
    # Now we need to know which has the longest time of movement 
    if (ShoulderTime > ArmTime) and (ShoulderTime > WristTime):
    elif (ArmTime > WristTime):
    else:
        #

#################################################################
# moveFoot( Leg, X-Axis, Y-Axis, Z-Axis, Speed)                 #
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# X-Axis, Y-Axis, Z-Axis is the amount in mm to move the foot   #
#   in that axis. A negative value will move it in the reverse  #
#   direction.                                                  #
# Speed is a value between 0.01 and 1.00 and represents the     #
#   multiplyer time the maximum rotation rate.                  #
#################################################################
def moveFoot(Leg, X, Y, Z, Speed):
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
        
def setServosInverseKinematics(Leg, X, Y, Z, Speed):
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

