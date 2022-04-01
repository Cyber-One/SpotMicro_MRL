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
# sMoveFoot(Leg, X-Axis, Y-Axis, Z-Axis, Speed)                 #
# This routine sets the speed of each of the servos for a leg   #
# to produce a straight line movement.                          #
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
    # Lets get the current 3D space position of the foot
    Position = forwardKinematics(Leg, ShoulderCurrentPos, ArmCurrentPos+180, WristCurrentPos)
    # Now that we have the current 3D Space position, lets calculate where we want to put it.
    ServoPos = legInverseKinematics(Position.get("X") + X, Position.get("Y") + Y, Position.get("Z") + Z)
    print Position.get("Z"), " Cur-Z:", Position.get("Y"), " Cur-Y:", Position.get("X"), "Cur-X:"
    print Position.get("Z") + Z, " Tar-Z:", Position.get("Y") + Y, " Tar-Y:", Position.get("X") + X, "Tar-X:"
    print WristCurrentPos, " Wrist Pos:", ArmCurrentPos, " Arm Pos:", ShoulderCurrentPos, "Shoulder Pos:"
    print ServoPos.get("Wrist"), " Tar-Wrist:", ServoPos.get("Arm"), " Tar-Arm:", ServoPos.get("Shoulder"), "Tar-Shoulder:"
    print ServoPos.get("Error"), "Error code returned:"
    if ServoPos.get("Error") == 0:
    # Assuming no errors occured.
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
        print WristSpeed, " Wrist Speed:", ArmSpeed, " Arm Speed:", ShoulderSpeed, "Shoulder Speed:"
        # Now we have our speeds and target servo positions, we can
        # set this up for each of the servos.
        if Leg == 0:
            print "Front Left Leg"
            FLShoulder.setSpeed(ShoulderSpeed)
            FLArm.setSpeed(ArmSpeed)
            FLWrist.setSpeed(WristSpeed)
            FLShoulder.moveTo(ServoPos.get("Shoulder"))
            FLArm.moveTo(ServoPos.get("Arm"))
            FLWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 1:
            print "Front Right Leg"
            FRShoulder.setSpeed(ShoulderSpeed)
            FRArm.setSpeed(ArmSpeed)
            FRWrist.setSpeed(WristSpeed)
            FRShoulder.moveTo(ServoPos.get("Shoulder"))
            FRArm.moveTo(ServoPos.get("Arm"))
            FRWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 2:
            print "Back Left Leg"
            BLShoulder.setSpeed(ShoulderSpeed)
            BLArm.setSpeed(ArmSpeed)
            BLWrist.setSpeed(WristSpeed)
            BLShoulder.moveTo(ServoPos.get("Shoulder"))
            BLArm.moveTo(ServoPos.get("Arm"))
            BLWrist.moveTo(ServoPos.get("Wrist"))
        elif Leg == 3:
            print "Back Right Leg"
            BRShoulder.setSpeed(ShoulderSpeed)
            BRArm.setSpeed(ArmSpeed)
            BRWrist.setSpeed(WristSpeed)
            BRShoulder.moveTo(ServoPos.get("Shoulder"))
            BRArm.moveTo(ServoPos.get("Arm"))
            BRWrist.moveTo(ServoPos.get("Wrist"))

#################################################################
# sMoveFeet(FLX, FLY, FLZ, FRX, FRY, FRZ, BLX, BLY, BLZ, BRX,   #
# BRY, BRZ, Speed)                                              #
# This routine sets the speed of each of the servos for a leg   #
# to produce a straight line movement with all four legs        #
# completing the movement at the same time.                     #
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
    # And the max rate for the servos

