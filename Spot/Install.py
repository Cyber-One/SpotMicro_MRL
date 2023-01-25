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
# Start.py                                                      #
# This file starts the GUI if required and runs all the         #
# other files required for the Spot Micro robot to run.         #
#                                                               #
#################################################################
# Because you might want to place your robots files into a      #
# different dicrectory compared to what I have,                 #
# the RunningFolder variable is the name of the folder you      #
# will be using.                                                #
#################################################################
RuningFolder="Spot"
DestinationFolder="data"

#################################################################
# The execfile() function loads and executes the named program. #
# This is handy for breaking a program into smaller more        #
# manageable parts.                                             #
# This file is the system configuration file.                   #
#################################################################
execfile(RuningFolder+'/1_Configuration/1_Sys_Config.py')

#################################################################
# Before we get too carried away, I plan to start Spot using a  #
# shell script called start_spot.sh                             #
# This will start the MRL and the Spot scripts with no          #
# Graphical User Interfaces (GUI) at all.                       #
# Under normal conditions, this would be desirable as spot      #
# doesn't have a monitor at all, however we can connect to it   #
# with VNC which does give us a monitor so we may want a GUI.   #
# To overcome this issue, we will start the GUI here.           #
#                                                               #
# Python uses indentation or white space to show each of the    #
# lines to be executed as part of an if statement.              #
# In the first if statement, there is only one indented line    #
# following, then we have a blank line (for clarity) before     #
# we have another if statement.  The second If statement needs  #
# to execute a number of line, and you can see these lines are  #
# all indented.  There is also one nested if statement.         #
#################################################################

if RunWebGUI == True:
    plan = runtime.load("webgui","WebGui")
    config = plan.get("webgui")
    config.autoStartBrowser = False
    runtime.start("webgui", "WebGui")
    #WebGui = Runtime.create("WebGui","WebGui")
    #WebGui.hide('cli')
    #sleep(1)
    #WebGui.show('cli')
    #sleep(1)
    #WebGui.set('cli', 400, 400, 999)
    #############################################################
    # if you don't want the browser to autostart to homepage    #
    # then set the autoStartBrowser to False                    #
    #############################################################
    #if RunWebGUIbrowser == False:
    #    WebGui.autoStartBrowser(False)
    #############################################################
    # set a different port number to listen to. default is 8888 #
    #    WebGui.setPort(7777)                                   #
    # on startup the WebGui will look for a "resources"         #
    # directory (may change in the future)                      #
    # static html files can be placed here and accessed         #
    # through the WebGui service starts the websocket server    #
    # and attempts to autostart browser unless it was disabled  #
    #############################################################
    #WebGui.startService();

#################################################################
# Load in the Common Variables used to help track and control   #
# various functions                                             #
#################################################################
execfile(RuningFolder+'/Common_Variables.py')

#################################################################
# Controllers.py starts the major controller interface services #
# such as the Raspberry Pi service and the Adafruit Servo       #
# controller services                                           #
# This is also where you would start any Arduino services you   #
# might want to add like the Nano for the Ultra-Sonic sensors.  #
#################################################################
execfile(RuningFolder+'/Controllers.py')

#################################################################
# The IO services are for things like the PIR, Ultrasonic
# range finders and NeoPixel rings ect.
#################################################################
execfile(RuningFolder+'/IO.py')

#################################################################
# The next is for the different servos we will be running.      #
# This set of files are responsible for starting and            #
# configuring each of the servos throughout the robot.          #
#################################################################
execfile(RuningFolder+'/Servos.py')

#################################################################
# There are a number of options for Text To Speech (TTS) and    #
# Speech To Text (STT) service.  You will need to have a look   #
# in this file to select which ones you want to use.            #
#################################################################
#execfile(RuningFolder+'/Speech.py')

#################################################################
# When not activly executing a command, we don't want the       #
# robot to just stand there,  This file is responsible for      #
# giving our robot a bitof life.                                #
# By blinking the eyes, coordinating the left and right eyes    #
# and performing other random like movements, just to make our  #
# robot appear to be alive.                                     #
#################################################################
execfile(RuningFolder+'/Life.py')

#################################################################
# When not activly executing a command, we don't want the       #
# robot to just stand there,  This file is responsible for      #
# giving our robot a bitof life.                                #
# By blinking the eyes, coordinating the left and right eyes    #
# and performing other random like movements, just to make our  #
# robot appear to be alive.                                     #
#################################################################
execfile(RuningFolder+'/Gestures.py')

#################################################################
# If your robot has cameras in it's eye, then we may want to    #
# add in Open Computer Vison to help the robot make sense of    #
# the world around it.                                          #
#################################################################
#execfile(RuningFolder+'/OpenCV.py')

#################################################################
# This file sets up the WebKitSpeechRecognition service         #
# The MarySpeech TTS service and the ProgramAB service that     #
# interperates the Alice2 AIML files                            #
#################################################################
#execfile(RuningFolder+'/Brain.py')

