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
import math
print "Starting the Leg Speed Control Functions"

#################################################################
# List of functions.                                            #
#################################################################
# setAllServoSpeeds(Speed)                                      #
# sMoveFoot(Leg, X-Axis, Y-Axis, Z-Axis, Speed)                 #
# sMoveFootTo(Leg, X-Axis, Y-Axis, Z-Axis, Speed)               #
# lMoveFoot(Leg, X, Y, Z, Speed, Steps)                         #
# sMoveFeet(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX,   #
#   BRY, BRZ, Speed)                                            #
# sMoveFeetTo(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX, #
#   BRY, BRZ, Speed)                                            #
#################################################################

def areServosMoving():
    rValue = 0
    if FLShoulder.isMoving(): rValue = 1
    if FLArm.isMoving(): rValue = 1
    if FLWrist.isMoving(): rValue = 1
    if FRShoulder.isMoving(): rValue = 1
    if FRArm.isMoving(): rValue = 1
    if FRWrist.isMoving(): rValue = 1
    if BLShoulder.isMoving(): rValue = 1
    if BLArm.isMoving(): rValue = 1
    if BLWrist.isMoving(): rValue = 1
    if BRShoulder.isMoving(): rValue = 1
    if BRArm.isMoving(): rValue = 1
    if BRWrist.isMoving(): rValue = 1
    return rValue

def blockServosMoving():
    a = 0
    while not round(FLShoulder.getCurrentInputPos()) == round(FLShoulder.getTargetPos()): a = a+1
    while not round(FLArm.getCurrentInputPos()) == round(FLArm.getTargetPos()): a = a+1
    while not round(FLWrist.getCurrentInputPos()) == round(FLWrist.getTargetPos()): a = a+1
    while not round(FRShoulder.getCurrentInputPos()) == round(FRShoulder.getTargetPos()): a = a+1
    while not round(FRArm.getCurrentInputPos()) == round(FRArm.getTargetPos()): a = a+1
    while not round(FRWrist.getCurrentInputPos()) == round(FRWrist.getTargetPos()): a = a+1
    while not round(BLShoulder.getCurrentInputPos()) == round(BLShoulder.getTargetPos()): a = a+1
    while not round(BLArm.getCurrentInputPos()) == round(BLArm.getTargetPos()): a = a+1
    while not round(BLWrist.getCurrentInputPos()) == round(BLWrist.getTargetPos()): a = a+1
    while not round(BRShoulder.getCurrentInputPos()) == round(BRShoulder.getTargetPos()): a = a+1
    while not round(BRArm.getCurrentInputPos()) == round(BRArm.getTargetPos()): a = a+1
    while not round(BRWrist.getCurrentInputPos()) == round(BRWrist.getTargetPos()): a = a+1
    #print a, "Wait Time:"

#################################################################
# setAllServoSpeeds(Speed)                                      #
# As the name suggest, this sets the speed of all the servos to #
# the percentage of max speed based on the value of Speed.      #
# Speed is a value between 0.01 and 1.0                         #
#################################################################
def setAllServoSpeeds(Speed):
    # First of the sanity checks.
    if Speed > 1.0 or Speed < 0.01:
        Speed = 1.0
    # Set all the base speeds
    FLShoulder.setSpeed(FLShoulderVelocity * Speed)
    FRShoulder.setSpeed(FRShoulderVelocity * Speed)
    BLShoulder.setSpeed(BLShoulderVelocity * Speed)
    BRShoulder.setSpeed(BRShoulderVelocity * Speed)
    FLArm.setSpeed(FLArmVelocity * Speed)
    FRArm.setSpeed(FRArmVelocity * Speed)
    BLArm.setSpeed(BLArmVelocity * Speed)
    BRArm.setSpeed(BRArmVelocity * Speed)
    FLWrist.setSpeed(FLWristVelocity * Speed)
    FRWrist.setSpeed(FRWristVelocity * Speed)
    BLWrist.setSpeed(BLWristVelocity * Speed)
    BRWrist.setSpeed(BRWristVelocity * Speed)
    sleep(0.1)

#################################################################
# sMoveFoot(Leg, X-Axis, Y-Axis, Z-Axis, Speed)                 #
# This routine sets the speed of each of the servos for a leg   #
# so that the servos all finish moving at the same time         #
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
# Speed is a value between 0.01 and 1.0 where 1.0 is full speed #
#################################################################
def sMoveFoot(Leg, X, Y, Z, Speed):
    # First of the sanity checks.
    if Speed > 1.0 or Speed < 0.01:
        Speed = 1.0
    # First we need to know the current position.
    # And the max rate for the servos
    if Leg == 0:
        ShoulderCurrentPos = FLShoulder.getTargetPos()
        ArmCurrentPos = FLArm.getTargetPos()
        WristCurrentPos = FLWrist.getTargetPos()
        ShoulderVelocity = FLShoulderVelocity
        ArmVelocity = FLArmVelocity
        WristVelocity = FLWristVelocity
    elif Leg == 1:
        ShoulderCurrentPos = FRShoulder.getTargetPos()
        ArmCurrentPos = FRArm.getTargetPos()
        WristCurrentPos = FRWrist.getTargetPos()
        ShoulderVelocity = FRShoulderVelocity
        ArmVelocity = FRArmVelocity
        WristVelocity = FRWristVelocity
    elif Leg == 2:
        ShoulderCurrentPos = BLShoulder.getTargetPos()
        ArmCurrentPos = BLArm.getTargetPos()
        WristCurrentPos = BLWrist.getTargetPos()
        ShoulderVelocity = BLShoulderVelocity
        ArmVelocity = BLArmVelocity
        WristVelocity = BLWristVelocity
    elif Leg == 3:
        ShoulderCurrentPos = BRShoulder.getTargetPos()
        ArmCurrentPos = BRArm.getTargetPos()
        WristCurrentPos = BRWrist.getTargetPos()
        ShoulderVelocity = BRShoulderVelocity
        ArmVelocity = BRArmVelocity
        WristVelocity = BRWristVelocity
    # Lets get the current 3D space position of the foot
    Position = forwardKinematics(Leg, ShoulderCurrentPos, ArmCurrentPos+180, WristCurrentPos)
    # Now that we have the current 3D Space position, lets calculate where we want to put it.
    ServoPos = legInverseKinematics(Position.get("X") + X, Position.get("Y") + Y, Position.get("Z") + Z)
    #print Position.get("Z"), " Cur-Z:", Position.get("Y"), " Cur-Y:", Position.get("X"), "Cur-X:"
    #print Position.get("Z") + Z, " Tar-Z:", Position.get("Y") + Y, " Tar-Y:", Position.get("X") + X, "Tar-X:"
    #print WristCurrentPos, " Wrist Pos:", ArmCurrentPos, " Arm Pos:", ShoulderCurrentPos, "Shoulder Pos:"
    #print ServoPos.get("Wrist"), " Tar-Wrist:", ServoPos.get("Arm"), " Tar-Arm:", ServoPos.get("Shoulder"), "Tar-Shoulder:"
    #print ServoPos.get("Error"), "Error code returned:"
    if ServoPos.get("Error") == 0:
        # Assuming no errors occured.
        # Next we need to know the offset from the current pos to
        # the new pos.
        ShoulderOffset = abs(ServoPos.get("Shoulder") - ShoulderCurrentPos)
        ArmOffset = abs(ServoPos.get("Arm") - ArmCurrentPos)
        WristOffset = abs(ServoPos.get("Wrist") - WristCurrentPos)
        #print WristOffset, " Wrist Ofset:", ArmOffset, " Arm Offset:", ShoulderOffset, "Shoulder Offset:"
        # Next we need to know, how long it will take for the servos
        # to reach the new position. 
        # We can get max speed from the Spot config
        ShoulderTime = ShoulderOffset / ShoulderVelocity
        ArmTime = ArmOffset / ArmVelocity
        WristTime = WristOffset / WristVelocity
        #print WristTime, " Wrist Time:", ArmTime, " Arm Time:", ShoulderTime, "Shoulder Time:"
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
        #print WristSpeed, " Wrist Speed:", ArmSpeed, " Arm Speed:", ShoulderSpeed, "Shoulder Speed:"
        # Now we have our speeds and target servo positions, we can
        # set this up for each of the servos.
        blockServosMoving()
        if Leg == 0:
            #print "Front Left Leg"
            FLShoulder.setSpeed(ShoulderSpeed)
            FLArm.setSpeed(ArmSpeed)
            FLWrist.setSpeed(WristSpeed)
            if ShoulderSpeed > 0.1: FLShoulder.moveTo(ServoPos.get("Shoulder"))
            if ArmSpeed > 0.1: FLArm.moveTo(ServoPos.get("Arm"))
            if WristSpeed > 0.1: FLWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 1:
            #print "Front Right Leg"
            FRShoulder.setSpeed(ShoulderSpeed)
            FRArm.setSpeed(ArmSpeed)
            FRWrist.setSpeed(WristSpeed)
            if ShoulderSpeed > 0.1: FRShoulder.moveTo(ServoPos.get("Shoulder"))
            if ArmSpeed > 0.1: FRArm.moveTo(ServoPos.get("Arm"))
            if WristSpeed > 0.1: FRWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 2:
            #print "Back Left Leg"
            BLShoulder.setSpeed(ShoulderSpeed)
            BLArm.setSpeed(ArmSpeed)
            BLWrist.setSpeed(WristSpeed)
            if ShoulderSpeed > 0.1: BLShoulder.moveTo(ServoPos.get("Shoulder"))
            if ArmSpeed > 0.1: BLArm.moveTo(ServoPos.get("Arm"))
            if WristSpeed > 0.1: BLWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 3:
            #print "Back Right Leg"
            BRShoulder.setSpeed(ShoulderSpeed)
            BRArm.setSpeed(ArmSpeed)
            BRWrist.setSpeed(WristSpeed)
            if ShoulderSpeed > 0.1: BRShoulder.moveTo(ServoPos.get("Shoulder"))
            if ArmSpeed > 0.1: BRArm.moveTo(ServoPos.get("Arm"))
            if WristSpeed > 0.1: BRWrist.moveTo(ServoPos.get("Wrist"))

#################################################################
# sMoveFootTo(Leg, X-Axis, Y-Axis, Z-Axis, Speed)               #
# This routine sets the speed of each of the servos for a leg   #
# so that the servos all finish moving at the same time         #
# The Leg value is between 0 and 3                              #
# 0 = Front left Leg                                            #
# 1 = Front Right Leg                                           #
# 2 = Back left Leg                                             #
# 3 = Back Right Leg                                            #
# X-Axis, Y-Axis, Z-Axis is the target position X, Y and Z      #
# relative to the center of the robot.                          #
# Unlike the previous functions, we only need to know the       #
# current servo positions, then calculate the new position      #
# using the Inverse kinimatics to workout the new servo         #
# positions as we already know the absolute destination         #
# position.                                                     #
# Speed is a value between 0.01 and 1.0 where 1.0 is full speed #
#################################################################
def sMoveFootTo(Leg, Xpos, Ypos, Zpos, Speed):
    # First of the sanity checks.
    if Speed > 1.0 or Speed < 0.01:
        Speed = 1.0
    # First we need to know the current position.
    # And the max rate for the servos
    if Leg == 0:
        ShoulderCurrentPos = FLShoulder.getCurrentInputPos()
        ArmCurrentPos = FLArm.getCurrentInputPos()
        WristCurrentPos = FLWrist.getCurrentInputPos()
        ShoulderVelocity = FLShoulderVelocity
        ArmVelocity = FLArmVelocity
        WristVelocity = FLWristVelocity
        ServoPos = legInverseKinematics(-Xpos - LXS, Ypos + LYS, Zpos)
    elif Leg == 1:
        ShoulderCurrentPos = FRShoulder.getCurrentInputPos()
        ArmCurrentPos = FRArm.getCurrentInputPos()
        WristCurrentPos = FRWrist.getCurrentInputPos()
        ShoulderVelocity = FRShoulderVelocity
        ArmVelocity = FRArmVelocity
        WristVelocity = FRWristVelocity
        ServoPos = legInverseKinematics(Xpos + LXS, Ypos + LYS, Zpos)
    elif Leg == 2:
        ShoulderCurrentPos = BLShoulder.getCurrentInputPos()
        ArmCurrentPos = BLArm.getCurrentInputPos()
        WristCurrentPos = BLWrist.getCurrentInputPos()
        ShoulderVelocity = BLShoulderVelocity
        ArmVelocity = BLArmVelocity
        WristVelocity = BLWristVelocity
        ServoPos = legInverseKinematics(-Xpos - LXS, -Ypos - LYS, Zpos)
    elif Leg == 3:
        ShoulderCurrentPos = BRShoulder.getCurrentInputPos()
        ArmCurrentPos = BRArm.getCurrentInputPos()
        WristCurrentPos = BRWrist.getCurrentInputPos()
        ShoulderVelocity = BRShoulderVelocity
        ArmVelocity = BRArmVelocity
        WristVelocity = BRWristVelocity
        ServoPos = legInverseKinematics(Xpos + LXS, -Ypos - LYS, Zpos)
    #print WristCurrentPos, " Wrist Pos:", ArmCurrentPos, " Arm Pos:", ShoulderCurrentPos, "Shoulder Pos:"
    #print ServoPos.get("Wrist"), " Tar-Wrist:", ServoPos.get("Arm"), " Tar-Arm:", ServoPos.get("Shoulder"), "Tar-Shoulder:"
    #print ServoPos.get("Error"), "Error code returned:"
    if ServoPos.get("Error") == 0:
        # Assuming no errors occured.
        # Next we need to know the offset from the current pos to
        # the new pos.
        ShoulderOffset = abs(ServoPos.get("Shoulder") - ShoulderCurrentPos)
        ArmOffset = abs(ServoPos.get("Arm") - ArmCurrentPos)
        WristOffset = abs(ServoPos.get("Wrist") - WristCurrentPos)
        #print WristOffset, " Wrist Ofset:", ArmOffset, " Arm Offset:", ShoulderOffset, "Shoulder Offset:"
        # Next we need to know, how long it will take for the servos
        # to reach the new position. 
        # We can get max speed from the Spot config
        ShoulderTime = ShoulderOffset / ShoulderVelocity
        ArmTime = ArmOffset / ArmVelocity
        WristTime = WristOffset / WristVelocity
        #print WristTime, " Wrist Time:", ArmTime, " Arm Time:", ShoulderTime, "Shoulder Time:"
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
        #print WristSpeed, " Wrist Speed:", ArmSpeed, " Arm Speed:", ShoulderSpeed, "Shoulder Speed:"
        # Now we have our speeds and target servo positions, we can
        # set this up for each of the servos.
        blockServosMoving()
        if Leg == 0:
            #print "Front Left Leg"
            FLShoulder.setSpeed(ShoulderSpeed)
            FLArm.setSpeed(ArmSpeed)
            FLWrist.setSpeed(WristSpeed)
            FLShoulder.moveTo(ServoPos.get("Shoulder"))
            FLArm.moveTo(ServoPos.get("Arm"))
            FLWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 1:
            #print "Front Right Leg"
            FRShoulder.setSpeed(ShoulderSpeed)
            FRArm.setSpeed(ArmSpeed)
            FRWrist.setSpeed(WristSpeed)
            FRShoulder.moveTo(ServoPos.get("Shoulder"))
            FRArm.moveTo(ServoPos.get("Arm"))
            FRWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 2:
            #print "Back Left Leg"
            BLShoulder.setSpeed(ShoulderSpeed)
            BLArm.setSpeed(ArmSpeed)
            BLWrist.setSpeed(WristSpeed)
            BLShoulder.moveTo(ServoPos.get("Shoulder"))
            BLArm.moveTo(ServoPos.get("Arm"))
            BLWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 3:
            #print "Back Right Leg"
            BRShoulder.setSpeed(ShoulderSpeed)
            BRArm.setSpeed(ArmSpeed)
            BRWrist.setSpeed(WristSpeed)
            BRShoulder.moveTo(ServoPos.get("Shoulder"))
            BRArm.moveTo(ServoPos.get("Arm"))
            BRWrist.moveTo(ServoPos.get("Wrist"))

#################################################################
# lMoveFoot(Leg, X, Y, Z, Speed, Steps)                         #
#################################################################
def lMoveFoot(Leg, X, Y, Z, Speed, Steps):
    # lets do the sanity checks first
    if Speed > 1.0 or Speed < 0.01: Speed = 1.0
    if Steps > 20 or Steps < 1: Steps = 10
    for i in range(Steps):
        sMoveFoot(Leg, X/Steps, Y/Steps, Z/Steps, Speed)

#################################################################
# sMoveFeet(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX,   #
#   BRY, BRZ, Speed)                                            #
# This routine sets the speed of each of the servos for a leg   #
# to produce a movement with all four legs completing the       #
# movement at the same time.                                    #
# X-Axis, Y-Axis, Z-Axis for each of the four feet is the       #
#   amount in mm to move the foot in that axis.                 #
#   A negative value will move it in the reverse direction.     #
# This function first works out the current foot position,      #
# then calculate the new position by adding the X, Y and Z      #
# inputs to work out the new abosulte position using the        #
# legInverseKinematics function.                                #
# Speed is a value between 0.01 and 1.0 where 1.0 is full speed #
#################################################################
def sMoveFeet(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX, BRY, BRZ, Speed):
    # First of the sanity checks.
    if Speed > 1.0 or Speed < 0.01:
        Speed = 1.0
    # First we need to know the current position.
    FLPosition = forwardKinematics(0, FLShoulder.getCurrentInputPos(), FLArm.getCurrentInputPos()+180, FLWrist.getCurrentInputPos())
    FRPosition = forwardKinematics(1, FRShoulder.getCurrentInputPos(), FRArm.getCurrentInputPos()+180, FRWrist.getCurrentInputPos())
    BLPosition = forwardKinematics(2, BLShoulder.getCurrentInputPos(), BLArm.getCurrentInputPos()+180, BLWrist.getCurrentInputPos())
    BRPosition = forwardKinematics(3, BRShoulder.getCurrentInputPos(), BRArm.getCurrentInputPos()+180, BRWrist.getCurrentInputPos())
    # Now that we have the current 3D Space position, lets calculate where we want to put it.
    FLServoPos = legInverseKinematics(FLPosition.get("X") + FLX, FLPosition.get("Y") + FLY, FLPosition.get("Z") + FLZ)
    FRServoPos = legInverseKinematics(FRPosition.get("X") + FRX, FRPosition.get("Y") + FRY, FRPosition.get("Z") + FRZ)
    BLServoPos = legInverseKinematics(BLPosition.get("X") + BLX, BLPosition.get("Y") + BLY, BLPosition.get("Z") + BLZ)
    BRServoPos = legInverseKinematics(BRPosition.get("X") + BRX, BRPosition.get("Y") + BRY, BRPosition.get("Z") + BRZ)
    if FLServoPos.get("Error") == 0 and FRServoPos.get("Error") == 0 and BLServoPos.get("Error") == 0 and BRServoPos.get("Error") == 0:
        # Assuming no errors occured.
        # Next we need to know the offset from the current pos to
        # the new pos.
        FLShoulderOffset = abs(FLServoPos.get("Shoulder") - FLShoulder.getCurrentInputPos())
        FLArmOffset = abs(FLServoPos.get("Arm") - FLArm.getCurrentInputPos())
        FLWristOffset = abs(FLServoPos.get("Wrist") - FLWrist.getCurrentInputPos())
        FRShoulderOffset = abs(FRServoPos.get("Shoulder") - FRShoulder.getCurrentInputPos())
        FRArmOffset = abs(FRServoPos.get("Arm") - FRArm.getCurrentInputPos())
        FRWristOffset = abs(FRServoPos.get("Wrist") - FRWrist.getCurrentInputPos())
        BLShoulderOffset = abs(BLServoPos.get("Shoulder") - BLShoulder.getCurrentInputPos())
        BLArmOffset = abs(BLServoPos.get("Arm") - BLArm.getCurrentInputPos())
        BLWristOffset = abs(BLServoPos.get("Wrist") - BLWrist.getCurrentInputPos())
        BRShoulderOffset = abs(BRServoPos.get("Shoulder") - BRShoulder.getCurrentInputPos())
        BRArmOffset = abs(BRServoPos.get("Arm") - BRArm.getCurrentInputPos())
        BRWristOffset = abs(BRServoPos.get("Wrist") - BRWrist.getCurrentInputPos())
        # Next we need to know, how long it will take for the servos
        # to reach the new position. 
        # We can get max speed from the Spot config
        FLShoulderTime = FLShoulderOffset / FLShoulderVelocity
        FLArmTime = FLArmOffset / FLArmVelocity
        FLWristTime = FLWristOffset / FLWristVelocity
        FRShoulderTime = FRShoulderOffset / FRShoulderVelocity
        FRArmTime = FRArmOffset / FRArmVelocity
        FRWristTime = FRWristOffset / FRWristVelocity
        BLShoulderTime = BLShoulderOffset / BLShoulderVelocity
        BLArmTime = BLArmOffset / BLArmVelocity
        BLWristTime = BLWristOffset / BLWristVelocity
        BRShoulderTime = BRShoulderOffset / BRShoulderVelocity
        BRArmTime = BRArmOffset / BRArmVelocity
        BRWristTime = BRWristOffset / BRWristVelocity
        # Now we need to know which has the longest time of movement 
        BigTime = FLShoulderTime
        if FLArmTime > BigTime : BigTime = FLArmTime
        if FLWristTime > BigTime : BigTime = FLWristTime
        if FRShoulderTime > BigTime : BigTime = FRShoulderTime
        if FRArmTime > BigTime : BigTime = FRArmTime
        if FRWristTime > BigTime : BigTime = FRWristTime
        if BLShoulderTime > BigTime : BigTime = BLShoulderTime
        if BLArmTime > BigTime : BigTime = BLArmTime
        if BLWristTime > BigTime : BigTime = BLWristTime
        if BRShoulderTime > BigTime : BigTime = BRShoulderTime
        if BRArmTime > BigTime : BigTime = BRArmTime
        if BRWristTime > BigTime : BigTime = BRWristTime
        # Now that we have the longest move time, lets setup all the servo speeds
        blockServosMoving()
        FLShoulder.setSpeed(FLShoulderVelocity * Speed * (FLShoulderTime / BigTime))
        FLArm.setSpeed(FLArmVelocity * Speed * (FLArmTime / BigTime))
        FLWrist.setSpeed(FLWristVelocity * Speed * (FLWristTime / BigTime))
        FRShoulder.setSpeed(FRShoulderVelocity * Speed * (FRShoulderTime / BigTime))
        FRArm.setSpeed(FRArmVelocity * Speed * (FRArmTime / BigTime))
        FRWrist.setSpeed(FRWristVelocity * Speed * (FRWristTime / BigTime))
        BLShoulder.setSpeed(BLShoulderVelocity * Speed * (BLShoulderTime / BigTime))
        BLArm.setSpeed(BLArmVelocity * Speed * (BLArmTime / BigTime))
        BLWrist.setSpeed(BLWristVelocity * Speed * (BLWristTime / BigTime))
        BRShoulder.setSpeed(BRShoulderVelocity * Speed * (BRShoulderTime / BigTime))
        BRArm.setSpeed(BRArmVelocity * Speed * (BRArmTime / BigTime))
        BRWrist.setSpeed(BRWristVelocity * Speed * (BRWristTime / BigTime))
        # Now we have our speeds and target servo positions, we can
        # set this up for each of the servos.
        FLShoulder.moveTo(FLServoPos.get("Shoulder"))
        FLArm.moveTo(FLServoPos.get("Arm"))
        FLWrist.moveTo(FLServoPos.get("Wrist"))
        FRShoulder.moveTo(FRServoPos.get("Shoulder"))
        FRArm.moveTo(FRServoPos.get("Arm"))
        FRWrist.moveTo(FRServoPos.get("Wrist"))
        BLShoulder.moveTo(BLServoPos.get("Shoulder"))
        BLArm.moveTo(BLServoPos.get("Arm"))
        BLWrist.moveTo(BLServoPos.get("Wrist"))
        BRShoulder.moveTo(BRServoPos.get("Shoulder"))
        BRArm.moveTo(BRServoPos.get("Arm"))
        BRWrist.moveTo(BRServoPos.get("Wrist"))

#################################################################
# sMoveFeetTo(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX, #
#   BRY, BRZ, Speed)                                            #
# This routine sets the speed of each of the servos for a leg   #
# to produce a straight line movement with all four legs        #
# completing the movement at the same time.                     #
# X-Axis, Y-Axis, Z-Axis for each of the four feet is the       #
#   X, Y and Z coordinates for each of the legs relative to the #
#   center of the robot.                                        #
# Speed is a value between 0.01 and 1.0 where 1.0 is full speed #
#################################################################
def sMoveFeetTo(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX, BRY, BRZ, Speed):
    # First of the sanity checks.
    if Speed > 1.0 or Speed < 0.01:
        Speed = 1.0
    # First lets calculate where we want to put it.
    FLServoPos = legInverseKinematics(-FLX - LXS, FLY - LYS, FLZ)
    FRServoPos = legInverseKinematics(FRX - LXS, FRY - LYS, FRZ)
    BLServoPos = legInverseKinematics(-BLX - LXS, BLY + LYS, BLZ)
    BRServoPos = legInverseKinematics(BRX - LXS, BRY + LYS, BRZ)
    if FLServoPos.get("Error") == 0 and FRServoPos.get("Error") == 0 and BLServoPos.get("Error") == 0 and BRServoPos.get("Error") == 0:
        # Assuming no errors occured.
        # Next we need to know the offset from the current pos to
        # the new pos.
        FLShoulderOffset = abs(FLServoPos.get("Shoulder") - FLShoulder.getCurrentInputPos())
        FLArmOffset = abs(FLServoPos.get("Arm") - FLArm.getCurrentInputPos())
        FLWristOffset = abs(FLServoPos.get("Wrist") - FLWrist.getCurrentInputPos())
        FRShoulderOffset = abs(FRServoPos.get("Shoulder") - FRShoulder.getCurrentInputPos())
        FRArmOffset = abs(FRServoPos.get("Arm") - FRArm.getCurrentInputPos())
        FRWristOffset = abs(FRServoPos.get("Wrist") - FRWrist.getCurrentInputPos())
        BLShoulderOffset = abs(BLServoPos.get("Shoulder") - BLShoulder.getCurrentInputPos())
        BLArmOffset = abs(BLServoPos.get("Arm") - BLArm.getCurrentInputPos())
        BLWristOffset = abs(BLServoPos.get("Wrist") - BLWrist.getCurrentInputPos())
        BRShoulderOffset = abs(BRServoPos.get("Shoulder") - BRShoulder.getCurrentInputPos())
        BRArmOffset = abs(BRServoPos.get("Arm") - BRArm.getCurrentInputPos())
        BRWristOffset = abs(BRServoPos.get("Wrist") - BRWrist.getCurrentInputPos())
        # Next we need to know, how long it will take for the servos
        # to reach the new position. 
        # We can get max speed from the Spot config
        FLShoulderTime = FLShoulderOffset / FLShoulderVelocity
        FLArmTime = FLArmOffset / FLArmVelocity
        FLWristTime = FLWristOffset / FLWristVelocity
        FRShoulderTime = FRShoulderOffset / FRShoulderVelocity
        FRArmTime = FRArmOffset / FRArmVelocity
        FRWristTime = FRWristOffset / FRWristVelocity
        BLShoulderTime = BLShoulderOffset / BLShoulderVelocity
        BLArmTime = BLArmOffset / BLArmVelocity
        BLWristTime = BLWristOffset / BLWristVelocity
        BRShoulderTime = BRShoulderOffset / BRShoulderVelocity
        BRArmTime = BRArmOffset / BRArmVelocity
        BRWristTime = BRWristOffset / BRWristVelocity
        # Now we need to know which has the longest time of movement 
        BigTime = FLShoulderTime
        if FLArmTime > BigTime : BigTime = FLArmTime
        if FLWristTime > BigTime : BigTime = FLWristTime
        if FRShoulderTime > BigTime : BigTime = FRShoulderTime
        if FRArmTime > BigTime : BigTime = FRArmTime
        if FRWristTime > BigTime : BigTime = FRWristTime
        if BLShoulderTime > BigTime : BigTime = BLShoulderTime
        if BLArmTime > BigTime : BigTime = BLArmTime
        if BLWristTime > BigTime : BigTime = BLWristTime
        if BRShoulderTime > BigTime : BigTime = BRShoulderTime
        if BRArmTime > BigTime : BigTime = BRArmTime
        if BRWristTime > BigTime : BigTime = BRWristTime
        #print BigTime, "Largest Time calculated for max speed:"
        #print BRWristTime, " Wrist Time:", BRArmTime, " Arm Time:", BRShoulderTime, "Move Time Back Right Leg Shoulder Time:"
        #print BLWristTime, " Wrist Time:", BLArmTime, " Arm Time:", BLShoulderTime, "Move Time Back Left Leg Shoulder Time:"
        #print FRWristTime, " Wrist Time:", FRArmTime, " Arm Time:", FRShoulderTime, "Move Time Front Right Leg Shoulder Time:"
        #print FLWristTime, " Wrist Time:", FLArmTime, " Arm Time:", FLShoulderTime, "Move Time Front Left Leg Shoulder Time:"
        # Now that we have the longest move time, lets setup all the servo speeds
        FLShoulder.setSpeed(FLShoulderVelocity * Speed * (FLShoulderTime / BigTime))
        FLArm.setSpeed(FLArmVelocity * Speed * (FLArmTime / BigTime))
        FLWrist.setSpeed(FLWristVelocity * Speed * (FLWristTime / BigTime))
        FRShoulder.setSpeed(FRShoulderVelocity * Speed * (FRShoulderTime / BigTime))
        FRArm.setSpeed(FRArmVelocity * Speed * (FRArmTime / BigTime))
        FRWrist.setSpeed(FRWristVelocity * Speed * (FRWristTime / BigTime))
        BLShoulder.setSpeed(BLShoulderVelocity * Speed * (BLShoulderTime / BigTime))
        BLArm.setSpeed(BLArmVelocity * Speed * (BLArmTime / BigTime))
        BLWrist.setSpeed(BLWristVelocity * Speed * (BLWristTime / BigTime))
        BRShoulder.setSpeed(BRShoulderVelocity * Speed * (BRShoulderTime / BigTime))
        BRArm.setSpeed(BRArmVelocity * Speed * (BRArmTime / BigTime))
        BRWrist.setSpeed(BRWristVelocity * Speed * (BRWristTime / BigTime))
        #print BRWrist.getSpeed(), " Wrist:", BRArm.getSpeed(), " Arm:", BRShoulder.getSpeed(), "Set Speed Back Right Shoulder:"
        #print BLWrist.getSpeed(), " Wrist:", BLArm.getSpeed(), " Arm:", BLShoulder.getSpeed(), "Set Speed Back Left Shoulder:"
        #print FRWrist.getSpeed(), " Wrist:", FRArm.getSpeed(), " Arm:", FRShoulder.getSpeed(), "Set Speed Front Right Shoulder:"
        #print FLWrist.getSpeed(), " Wrist:", FLArm.getSpeed(), " Arm:", FLShoulder.getSpeed(), "Set Speed Front Left Shoulder:"
        sleep(0.1)
        # Now we have our speeds and target servo positions, we can
        # set this up for each of the servos.
        FLShoulder.moveTo(FLServoPos.get("Shoulder"))
        FLArm.moveTo(FLServoPos.get("Arm"))
        FLWrist.moveTo(FLServoPos.get("Wrist"))
        FRShoulder.moveTo(FRServoPos.get("Shoulder"))
        FRArm.moveTo(FRServoPos.get("Arm"))
        FRWrist.moveTo(FRServoPos.get("Wrist"))
        BLShoulder.moveTo(BLServoPos.get("Shoulder"))
        BLArm.moveTo(BLServoPos.get("Arm"))
        BLWrist.moveTo(BLServoPos.get("Wrist"))
        BRShoulder.moveTo(BRServoPos.get("Shoulder"))
        BRArm.moveTo(BRServoPos.get("Arm"))
        BRWrist.moveTo(BRServoPos.get("Wrist"))
    else:
        print BRServoPos.get("Error"), " BR Servo Error:", BLServoPos.get("Error"), " BL Servo Error:", FRServoPos.get("Error"), " FR Servo Error:", FLServoPos.get("Error"), "FL Servo Error:"

