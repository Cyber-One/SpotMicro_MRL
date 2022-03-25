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
# LegSpeedControl.py                                            #
# This file compares multiple servos and calculate the required #
# speed so all servos finish at the same time.                  #
#                                                               #
#################################################################

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
