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
# Life.py                                                       #
# This file is a group of commands that perform actions         #
#                                                               #
#################################################################
import time
print "Starting the various Life Services"

# Display time on the LCD
# I was having an issue with the Raspi dropping ofline.
# In order to help narrow down the cause, I am adding in a clock
# to the LCD display.
# If the clock continues to keep time on the LCD, then the fault
# is with the network interface.
def LCD_DisplayTime(data):
    LCD.display(RobotsName, 0)
    format = "%I:%M:%S %p"
    LCD.display(time.strftime(format), 1)
    #LCD.display(str(data), 1)
    


clock = Runtime.start("clock","Clock")
clock.addListener("publishTime", "python", "LCD_DisplayTime")
clock.setInterval(1000)
clock.startClock()
LCD.clear()

#################################################################
# updateServoPositions()                                        #
# This function update the global references for all 12 servos  #
# both the Servo Position and the 3D Space position of all      #
# 4 feet                                                        #
#################################################################
def updateServoPositions():
    global FLS_Servo
    global FLA_Servo
    global FLW_Servo
    global FRS_Servo
    global FRA_Servo
    global FRW_Servo
    global BLS_Servo
    global BLA_Servo
    global BLW_Servo
    global BRS_Servo
    global BRA_Servo
    global BRW_Servo
    global FL_X
    global FR_X
    global BL_X
    global BR_X
    global FL_Y
    global FR_Y
    global BL_Y
    global BR_Y
    global FL_Z
    global FR_Z
    global BL_Z
    global BR_Z
    FLS_Servo = FLShoulder.getCurrentInputPos()
    FLA_Servo = FLArm.getCurrentInputPos()
    FLW_Servo = FLWrist.getCurrentInputPos()
    FRS_Servo = FRShoulder.getCurrentInputPos()
    FRA_Servo = FRArm.getCurrentInputPos()
    FRW_Servo = FRWrist.getCurrentInputPos()
    BLS_Servo = BLShoulder.getCurrentInputPos()
    BLA_Servo = BLArm.getCurrentInputPos()
    BLW_Servo = BLWrist.getCurrentInputPos()
    BRS_Servo = BRShoulder.getCurrentInputPos()
    BRA_Servo = BRArm.getCurrentInputPos()
    BRW_Servo = BRWrist.getCurrentInputPos()
    FLPos = forwardKinematics(FLS_Servo, FLA_Servo+180, FLW_Servo)
    FRPos = forwardKinematics(FRS_Servo, FRA_Servo+180, FRW_Servo)
    BLPos = forwardKinematics(BLS_Servo, BLA_Servo+180, BLW_Servo)
    BRPos = forwardKinematics(BRS_Servo, BRA_Servo+180, BRW_Servo)
    FL_X = -FLPos.get("X") - LXS
    FL_Y = FLPos.get("Y") + LYS
    FL_Z = FLPos.get("Z")
    FR_X = FRPos.get("X") + LXS
    FR_Y = FRPos.get("Y") + LYS
    FR_Z = FRPos.get("Z")
    BL_X = -BLPos.get("X") - LXS
    BL_Y = BLPos.get("Y") - LYS
    BL_Z = BLPos.get("Z")
    BR_X = BRPos.get("X") + LXS
    BR_Y = BRPos.get("Y") - LYS
    BR_Z = BRPos.get("Z")
    print FL_Z, " FL-Z:", FL_Y, " FL-Y:", FL_X, "FL-X:"
    print FR_Z, " FR-Z:", FR_Y, " FR-Y:", FR_X, "FR-X:"
    print BL_Z, " BL-Z:", BL_Y, " BL-Y:", BL_X, "BL-X:"
    print BR_Z, " BR-Z:", BR_Y, " BR-Y:", BR_X, "BR-X:"

#################################################################
# Setup the Foot Class routines.                                #
#################################################################
execfile(RuningFolder+'/FootClass.py')

#data.getPitch()
#data.getRoll()
#data.getYaw()
if runtime.isStarted("MPU6050A"):
    def updateOrientation(data):
        global Pitch
        global Roll
        global Yaw
        Pitch = data.pitch
        Roll = data.roll
        Yaw = data.yaw
    python.subscribe('MPU6050A', 'publishOrientation', 'python', 'updateOrientation')

#################################################################
# Setup the Froward Kinematics routines.                        #
#################################################################
execfile(RuningFolder+'/Life/ForwardKinematics.py')

#################################################################
# Setup the Inverse Kinematics routines.                        #
#################################################################
execfile(RuningFolder+'/Life/InverseKinematics.py')

#################################################################
# Setup the Leg Movement routines.                        #
#################################################################
execfile(RuningFolder+'/Life/LegSpeedControl.py')



