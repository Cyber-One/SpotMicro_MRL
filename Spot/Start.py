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
# StartConfig.py                                                #
# This file is called by the Python Service when it starts up   #
# once a config has been created.  This then starts all the     #
# other required scripts.                                       #
#                                                               #
#################################################################
# Because you might want to place your robots files into a      #
# different dicrectory compared to what I have,                 #
# the RunningFolder variable is the name of the folder you      #
# will be using.                                                #
#################################################################
RuningFolder="data/Spot"

#################################################################
# This is the name the robot will use in some sections of the   #
# program such as WebKitSpeechRecognition.                      #
#################################################################
RobotsName = "Spot"

#################################################################
# Load in the Common Variables used to help track and control   #
# various functions                                             #
#################################################################
execfile(RuningFolder+'/Common_Variables.py')

#################################################################
# Setup the Foot Class routines.                                #
# Once the class has been run, we can create an instance by     #
# calling the Feet method.  This requires all the servo objects #
# to be passed to it as parameters.                             #
#################################################################
execfile(RuningFolder+'/FootClass.py')

legs = Feet(FLShoulder, FLArm, FLWrist, FRShoulder, FRArm, FRWrist, BLShoulder, BLArm, BLWrist, BRShoulder, BRArm, BRWrist)
legs.disableAutoLevel()


#################################################################
# Setup the MPU6050 calibration and callback functions          #
#################################################################
if runtime.isStarted("MPU6050A"):
    MPU6050A.setXGyroOffset(MPU6050A.getGyroXSelfTestFactoryTrim())
    MPU6050A.setYGyroOffset(MPU6050A.getGyroYSelfTestFactoryTrim())
    MPU6050A.setZGyroOffset(MPU6050A.getGyroZSelfTestFactoryTrim())
    def updateOrientation(data):
        global Pitch
        global Roll
        global Yaw
        Pitch = data.pitch
        Roll = data.roll
        Yaw = data.yaw
        legs.updateIMU(data.pitch, data.roll)
    python.subscribe('MPU6050A', 'publishOrientation', 'python', 'updateOrientation')
#################################################################
# When not activly executing a command, we don't want the       #
# robot to just stand there,  This file is responsible for      #
# giving our robot a bitof life.                                #
# By blinking the eyes, coordinating the left and right eyes    #
# and performing other random like movements, just to make our  #
# robot appear to be alive.                                     #
#################################################################
#execfile(RuningFolder+'/Life.py')

#################################################################
# When not activly executing a command, we don't want the       #
# robot to just stand there,  This file is responsible for      #
# giving our robot a bitof life.                                #
# By blinking the eyes, coordinating the left and right eyes    #
# and performing other random like movements, just to make our  #
# robot appear to be alive.                                     #
#################################################################
#execfile(RuningFolder+'/Gestures.py')
