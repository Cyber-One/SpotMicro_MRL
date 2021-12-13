# SpotMicro_MRL
This dog looks similar to the Boston Dynamic four legged robot named spot.
This version was created by KDY0523 and named Spotmicro after the Boston Dynamics robot.

Already there have been other creators out there modifying the design to change or add features, so you know I will be looking at those as well.
In the original design, an ArduinoMega 2560 was used to run Spotmicro, however there are mods to allow the use of a Raspberry Pi, so this is the way I will be going :-)

The Parts list.md file contains a list of the different locations and creators where I found these files and the files I used from those uploads.

The system will be running on My Robot Lab (MRL), available from http://myrobotlab.org/

## Installing
The file, Setting Up MRL on a Raspberry Pi.md has a list of instructions for setting up MRL on a Raspberry Pi.
In the soon to be released video, I show setting up with a Raspberry Pi 3B but the instructions also work with the Raspberry Pi 4B.
Onve MRL is installed on the Raspberry Pi, copy the Spot folder into the MRL folder along with the start_sopt.sh file.
Change the permissions of the start_spot.sh file to allow anyone to execute the file.

## Getting started
The start_spot.sh file is a shell command that will start MyrobotLab in a Java environment and then start the Spot/Start.py
Start.py is the starting point for the Spot program in MRL and is fully commented to help NOOB's learn more about the python programming side of MRL in an easy to follow script.
For the NOOB, the start the system, open a terminal window and change to the MRL folder.
Next run ./start_spot.sh

## Configuring Spot Micro 
If your not really interested in learning to program, and just want to run spot, you will need to setup the configurations.
In the Spot/1_Configuration folder, you will find a number of files.
Each of these files holds a different part of the system configuration.

### 1_Sys_Config.py 
holds all the system based configurations.
Here you will set the bots name and how the Web based Graphical User Interface works.

