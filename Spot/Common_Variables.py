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
# Common_Variables.py                                           #
# This is where the configuration settings live for the         #
# varoius controllers.                                          #
#                                                               #
#################################################################
print "Creating the Common Variables"
##############################################################
#                                                            #
# System wide global variable creation                       #
#                                                            #
##############################################################

# when the sleep timer is enabled, this allows the program to
# know when the robot is sleeping and when it's awake.
Awake = True                

# Finite State Control of the emotional state.
# This variable holds a number to signal which state it is
# currently in.
# State 0 = Sleep
# State 1 = Neutral/Alert
# State 2 = Bored
# State 3 = Happy/Excited
# State 4 = Sad
# State 5 = Angry
# On startup, we will start in the State 1 Neutral/Alert state
EmotionalState = 1

# when using a pair of Ultrasonic sensors, we are best to test
# one side then the other, not the two together.
LastPingLeft = False

# These are the last values recorded with the Ultrasonic sensors
LastLeftPing = 0
LastRightPing = 0

# These variables describe a leg
LWF = 124   # Length between the Wrist joint and the foot
LTW = 110   # Length between the Arms joint and the Wrist joint
LST = 55    # Length between the Shoulder joint and the center line of the Arm
LYS = 90    # Length between the center Y plane and the shoulder joint
LXS = 38    # Length between the center X plane and the shoulder joint
MaxLTF = LTW + LWF   # Max length between the arm pivot and the foot.

# These setting are global for the four legs.
# If you change any of these, you will have to recalibrate all the servos.
ShoulderMin = 50.0
ShoulderRest = 90.0
ShoulderMax = 130.0
ArmMin = 15.0
ArmRest = 120.0
ArmMax = 165.0
WristMin = 50.0
WristRest = 125.0
WristMax = 180.0

# Foot Positions, the numbers here are set by the program at rest based on the setting above
FL_X = -93.0
FR_X = 93.0
BL_X = -93.0
BR_X = 93.0

FL_Y = 87.405
FR_Y = 87.405
BL_Y = -92.595
BR_Y = -92.595

FL_Z = -207.645
FR_Z = -207.645
BL_Z = -207.645
BR_Z = -207.645
