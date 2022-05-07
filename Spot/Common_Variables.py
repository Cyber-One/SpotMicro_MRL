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
# This is where Global variables and Classes exist              #
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

# Physical state control.
# When moving between different positions, different types of
# movement are required, or the robot will fall over.
# State 0 = Laying Down
# State 1 = Crouch
# State 2 = Sit
# State 3 = Standing at rest
# State 4 = Standing High.
# State 5 = Sit Up
PhysicalState = 0

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
# The following would be required is the robot is front or rear heavy.
CoMoffsetX = 0  # Center of mass offset X axis
CoMoffsetY = 0  # Center of mass offset Y axis
CoMoffsetZ = 0  # Center of mass offset Z axis

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

# Foot Positions, the numbers here are set by the program
# the pre-set numbers based on at rest position
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

# Now for all the IMU Foot position data
Pitch = 0.0
Roll = 0.0
Yaw = 0.0
RequestedPitch = 0.0
RequestedRoll = 0.0
RequestedYaw = 0.0
imuFL_X = FL_X
imuFR_X = FR_X
imuBL_X = BL_X
imuBR_X = BR_X
imuFL_Y = FL_Y
imuFR_Y = FR_Y
imuBL_Y = BL_Y
imuBR_Y = BR_Y
imuFL_Z = FL_Z
imuFR_Z = FR_Z
imuBL_Z = BL_Z
imuBR_Z = BR_Z


# Last know servo positions
FLS_Servo = ShoulderRest
FRS_Servo = ShoulderRest
BLS_Servo = ShoulderRest
BRS_Servo = ShoulderRest

FLA_Servo = ArmRest
FRA_Servo = ArmRest
BLA_Servo = ArmRest
BRA_Servo = ArmRest

FLW_Servo = WristRest
FRW_Servo = WristRest
BLW_Servo = WristRest
BRW_Servo = WristRest

# Dictionary versions
Servos = [[FLS_Servo, FLA_Servo, FLW_Servo],
        [FRS_Servo, FRA_Servo, FRW_Servo],
        [BLS_Servo, BLA_Servo, BLW_Servo],
        [BRS_Servo, BRA_Servo, BRW_Servo]]
