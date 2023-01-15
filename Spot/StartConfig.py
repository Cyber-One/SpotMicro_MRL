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
RuningFolder="Spot"

#################################################################
# Load in the Common Variables used to help track and control   #
# various functions                                             #
#################################################################
execfile(RuningFolder+'/Common_Variables.py')

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
