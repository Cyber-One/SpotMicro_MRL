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
# FiniteStateMachine.py                                                   #
# This file is a group of commands that perform actions         #
#                                                               #
#################################################################
print "Starting the Finite State Machine Services"

fsm = Runtime.start("fsm","FiniteStateMachine")

fsm.addState("Laydown")
fsm.addState("Crouch")
fsm.addState("Sit")
fsm.addState("Stand")

