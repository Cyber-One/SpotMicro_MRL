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
# 1_Sys_Config.py                                               #
# This is where the configuration settings live for the         #
# system.                                                       #
#                                                               #
#################################################################
print "Creating the System Config"

#################################################################
#                                                               #
# The Graphical User Interface (GUI)                            #
#                                                               #
#################################################################
# This is the name the robot will use in some sections of the
# program such as WebKitSpeechRecognition.
RobotsName = "Spot"

# WebGUI is the new boy on the block and is getting better.
# It will be started in anycase if you decide to use 
# WebKitSpeechRecognition.
RunWebGUI = True           # True for on, False for off
# WebGUI can be run headless, that is the web client interface 
# can be on another computer.  In this case we don't want to 
# launch the local web browser.  The local web browser also 
# uses a lot of computer power.
RunWebGUIbrowser = False    # True for on, False for off
