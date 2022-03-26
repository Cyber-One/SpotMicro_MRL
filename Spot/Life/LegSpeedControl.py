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
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# ServoPos is the dictionary returned by legInverseKinematics() #
# Speed is a value between 0.01 and 1.0 where 1.0 is full speed #
#################################################################
def kinematicsSetServo(Leg, ServoPos, Speed):
    # First of the sanity checks.
    if Speed > 1.0 or Speed < 0.01:
        Speed = 1.0
    # First we need to know the current position.
    if Leg == 0:
        ShoulderCurrentPos = FLShoulder.getCurrentInputPos()
        ArmCurrentPos = FLArm.getCurrentInputPos()
        WristCurrentPos = FLWrist.getCurrentInputPos()
        ShoulderVelocity = FLShoulderVelocity
        ArmVelocity = FLArmVelocity
        WristVelocity = FLWristVelocity
    elif Leg == 1:
        ShoulderCurrentPos = FRShoulder.getCurrentInputPos()
        ArmCurrentPos = FRArm.getCurrentInputPos()
        WristCurrentPos = FRWrist.getCurrentInputPos()
        ShoulderVelocity = FRShoulderVelocity
        ArmVelocity = FRArmVelocity
        WristVelocity = FRWristVelocity
    elif Leg == 2:
        ShoulderCurrentPos = BLShoulder.getCurrentInputPos()
        ArmCurrentPos = BLArm.getCurrentInputPos()
        WristCurrentPos = BLWrist.getCurrentInputPos()
        ShoulderVelocity = BLShoulderVelocity
        ArmVelocity = BLArmVelocity
        WristVelocity = BLWristVelocity
    elif Leg == 3:
        ShoulderCurrentPos = BRShoulder.getCurrentInputPos()
        ArmCurrentPos = BRArm.getCurrentInputPos()
        WristCurrentPos = BRWrist.getCurrentInputPos()
        ShoulderVelocity = BRShoulderVelocity
        ArmVelocity = BRArmVelocity
        WristVelocity = BRWristVelocity
    # Next we need to know the offset from the current pos to
    # the new pos.
    ShoulderOffset = ServoPos.get("Shoulder") - ShoulderCurrentPos
    ArmOffset = ServoPos.get("Arm") - ShoulderCurrentPos
    WristOffset = ServoPos.get("Wrist") - ShoulderCurrentPos
    # Next we need to know, how long it will take for the servos
    # to reach the new position. 
    # We can get max speed from the Spot config
    ShoulderTime = ShoulderOffset / ShoulderVelocity
    ArmTime = ArmOffset / ArmVelocity
    WristTime = WristOffset / WristVelocity
    # Now we need to know which has the longest time of movement 
    if (ShoulderTime > ArmTime) and (ShoulderTime > WristTime):
        ShoulderSpeed = ShoulderVelocity * Speed
        ArmSpeed = ArmVelocity * Speed * (ArmTime / ShoulderTime)
        WristSpeed = WristVelocity * Speed * (WristTime / ShoulderTime)
    elif (ArmTime > WristTime):
        ShoulderSpeed = ShoulderVelocity * Speed * (ShoulderTime / ArmTime)
        ArmSpeed = ArmVelocity * Speed
        WristSpeed = WristVelocity * Speed * (WristTime / ArmTime)
    else:
        ShoulderSpeed = ShoulderVelocity * Speed * (ShoulderTime / WristTime)
        ArmSpeed = ArmVelocity * Speed * (ArmTime / WristTime)
        WristSpeed = WristVelocity * Speed
    # Now we have our speeds and target servo positions, we can
    # set this up for each of the servos.
    if Leg == 0:
        FLShoulder.setSpeed(ShoulderSpeed)
        FLArm.setSpeed(ArmSpeed)
        FLWrist.setSpeed(WristSpeed)
        FLShoulder.moveTo(ServoPos.get("Shoulder"))
        FLArm.moveTo(ServoPos.get("Arm"))
        FLWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 1:
        FRShoulder.setSpeed(ShoulderSpeed)
        FRArm.setSpeed(ArmSpeed)
        FRWrist.setSpeed(WristSpeed)
        FRShoulder.moveTo(ServoPos.get("Shoulder"))
        FRArm.moveTo(ServoPos.get("Arm"))
        FRWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 2:
        BLShoulder.setSpeed(ShoulderSpeed)
        BLArm.setSpeed(ArmSpeed)
        BLWrist.setSpeed(WristSpeed)
        BLShoulder.moveTo(ServoPos.get("Shoulder"))
        BLArm.moveTo(ServoPos.get("Arm"))
        BLWrist.moveTo(ServoPos.get("Wrist"))
    elif Leg == 3:
        BRShoulder.setSpeed(ShoulderSpeed)
        BRArm.setSpeed(ArmSpeed)
        BRWrist.setSpeed(WristSpeed)
        BRShoulder.moveTo(ServoPos.get("Shoulder"))
        BRArm.moveTo(ServoPos.get("Arm"))
        BRWrist.moveTo(ServoPos.get("Wrist"))


