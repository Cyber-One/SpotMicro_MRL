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

#################################################################
# Setup the Froward Kinematics routines.                        #
#################################################################
execfile(RuningFolder+'/Life/ForwardKinematics.py')

#################################################################
# Setup the Inverse Kinematics routines.                        #
#################################################################
execfile(RuningFolder+'/Life/InverseKinematics.py')



