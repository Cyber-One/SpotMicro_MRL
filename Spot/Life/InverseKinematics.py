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

def legInverseKinematics(LSFx, LAFy, Zt):
    Error = 0
    # all inputs x, y, and z are relative to the shoulder joint.
    # we will assume the offsets from the center of the bot have already been applied.
    # Lets first work out the length between the shoulder joint and the foot
    LSF = math.sqrt((LSFx*LSFx) + (Zt*Zt))
    # Now that we have LSF and we know LST, lets work out the LTFz
    # we use the z suffix here, because this only relative to the X-Z plane and not the XY plane
    # LST = 50
    LTFz = math.sqrt(LSF*LSF - LST*LST)
    Ai = math.asin(LSFx/LSF)
    Ao = math.acos(LST/LSF)
    WorkServoS = math.degrees(Ai + Ao) - 90
    if WorkServoS < ShoulderMin:
        Error = 1
        WorkServoS = ShoulderMin
    if WorkServoS > ShoulderMax:
        Error = 2
        WorkServoS = ShoulderMax
    LTF = math.sqrt((LTFz*LTFz) + (LAFy*LAFy))
    ServoWR = math.acos(((LTW*LTW) + (LWF*LWF) - (LTF*LTF))/(2*LTW*LWF))
    WorkServoW = math.degrees(ServoWR)
    if WorkServoW < WristMin:
        Error = 5
        WorkServoW = WristMin
    if WorkServoW > WristMax:
        Error = 6
        WorkServoW = WristMax
    Afw = math.asin((math.sin(math.radians(WorkServoW))*LWF)/LTF)
    Af = math.acos(LTFz/LTF)
    WorkServoA = math.degrees(Afw+Af) - 90
    if WorkServoA < ArmMin:
        Error = 3
        WorkServoA = ArmMin
    if WorkServoA > ArmMax:
        Error = 4
        WorkServoA = ArmMax
    return {"Error":Error, "Shoulder":WorkServoS, "Arm":WorkServoA, "Wrist":WorkServoW}

def setServosInverseKinematics(Leg, X, Y, Z, Speed):
    if Leg == 0: # Front Left
        #FL_Leg(0)
        ServoPos = legInverseKinematics(X - LXS, Y - LYS, Z)
        FLShoulder.moveTo(ServoPos.get("Shoulder"))
        FLArm.moveTo(ServoPos.get("Arm"))
        FLWrist.moveTo(ServoPos.get("Wrist"))
    if Leg == 1: # Front Right
        #FR_Leg(0)
        ServoPos = legInverseKinematics(-(X+LXS), Y - LYS, Z)
        FRShoulder.moveTo(ServoPos.get("Shoulder"))
        FRArm.moveTo(ServoPos.get("Arm"))
        FRWrist.moveTo(ServoPos.get("Wrist"))
    if Leg == 2: # Back Left
        #BL_Leg(0)
        ServoPos = legInverseKinematics(X - LXS, Y + LYS, Z)
        BLShoulder.moveTo(ServoPos.get("Shoulder"))
        BLArm.moveTo(ServoPos.get("Arm"))
        BLWrist.moveTo(ServoPos.get("Wrist"))
    if Leg == 3: # Back Right
        #BR_Leg(0)
        ServoPos = legInverseKinematics(-(X+LXS), Y + LYS, Z)
        BRShoulder.moveTo(ServoPos.get("Shoulder"))
        BRArm.moveTo(ServoPos.get("Arm"))
        BRWrist.moveTo(ServoPos.get("Wrist"))
        
def moveFoot(Leg, X, Y, Z, Speed):
    if Leg == 0: # Front Left
        FL_Leg(0)
        ServoPos = legInverseKinematics(FL_X+LXS + X, FL_Y-LYS + Y, FL_Z + Z)
        FLShoulder.moveTo(ServoPos.get("Shoulder"))
        FLArm.moveTo(ServoPos.get("Arm"))
        FLWrist.moveTo(ServoPos.get("Wrist"))
    if Leg == 1: # Front Right
        FR_Leg(0)
        ServoPos = legInverseKinematics(FL_X-LXS + X, FL_Y-LYS + Y, FL_Z + Z)
        FRShoulder.moveTo(ServoPos.get("Shoulder"))
        FRArm.moveTo(ServoPos.get("Arm"))
        FRWrist.moveTo(ServoPos.get("Wrist"))
    if Leg == 2: # Back Left
        BL_Leg(0)
        ServoPos = legInverseKinematics(FL_X+LXS + X, FL_Y+LYS + Y, FL_Z + Z)
        BLShoulder.moveTo(ServoPos.get("Shoulder"))
        BLArm.moveTo(ServoPos.get("Arm"))
        BLWrist.moveTo(ServoPos.get("Wrist"))
    if Leg == 3: # Back Right
        BR_Leg(0)
        ServoPos = legInverseKinematics(FL_X-LXS + X, FL_Y+LYS + Y, FL_Z + Z)
        BRShoulder.moveTo(ServoPos.get("Shoulder"))
        BRArm.moveTo(ServoPos.get("Arm"))
        BRWrist.moveTo(ServoPos.get("Wrist"))
        
