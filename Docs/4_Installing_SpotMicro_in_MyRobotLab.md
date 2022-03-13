# 4) Installing SpotMicro in MyRobotLab

# Download SpotMicro_MRL

Before we get too carried away, we will need to install the SpotMicro_MRL program.
Open a new terminal window and enter the following command:
git clone https://github.com/Cyber-One/SpotMicro_MRL.git
This will create a new folder named SpotMicro_MRL and download all the files I created for the Spot Micro program. 🙂 
In the SpotMicro_MRL folder there is both the program and this documentation.

## Copy the SpotMicro_MRL into the MRL folder

using the file manager, change into the SpotMicro_MRL folder, select the Spot.sh file and the Spot folder, right click and select copy.
Change to the MRL folder and pate into that folder.
Before you can start spot the the shell script, you will first need to change the Spot.sh file permissions to allow anyone to execute it.
There are two way you can do this.
Using the file manager, right click on the file and select properties, then click on the Permissions tab, in the access control section at the bottom for the execute, drop down the list and change it from nobody to Anyone. 
The other method is within a terminal window, change into the MRL folder and execute the following line:
chmod a+x Spot.sh
This will add the execute permission to the owner, the group and everyone else.


## Starting SpotMicro_MRL

Open a terminal window and  change into the MRL folder.
Use the following command in the terminal to start the Spot program:
./Spot.sh
**Note, make sure you have shut down any other instances of MRL running before you do this. 🙂**
The ./ tells Linux that the program we want to run is in the current folder.
Spot.sh is a shell script which is required to start the MRL program and launch the SpotMicro start.py program in MRL.


