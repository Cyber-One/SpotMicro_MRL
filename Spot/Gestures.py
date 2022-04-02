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
# Gestures.py                                                   #
# This file is a group of commands that perform actions         #
#                                                               #
#################################################################
print "Starting the various Gestures Services"


#################################################################
# this command returns all the servos to the starting rest      #
# position.  Handy when calibrating.                            #
#################################################################
def rest(Speed):
    print "Moving to Rest postition"
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
    # Now send the legs to the rest position
    FLShoulder.rest()
    FRShoulder.rest()
    BLShoulder.rest()
    BRShoulder.rest()
    FLArm.rest()
    FRArm.rest()
    BLArm.rest()
    BRArm.rest()
    FLWrist.rest()
    FRWrist.rest()
    BLWrist.rest()
    BRWrist.rest()


