# Spot Micro Operating System

## Setting up the Raspberry Pi.

We will need a MicroSD card to hold the Operating System. (OS) I suggest a 32GB class 3, but a class 1 will work.
The last version releast was Buster, the most recent is Bullseye.
In either case you will need to use a flash program to copy it to the MicroSD card.
You can use the Raspberry Pi Imager https://www.raspberrypi.com/software/ or another imager, 
I used BalenaEtcher https://www.balena.io/etcher/
Using either program flash your chosen OS to the MicroSD Card.
After flashing, remove and re-insert the microSD card. 
In a windows system, it will ask you to format the card (DONT, cancel the request.)
You will find it will give you two new drives, the one you want is boot, the other is not accessable in windows, and windows will want to format it.
Opening the boot drive you will find a number of files, we only want to touch one of those files. :-)
Using Notpad++ or Notepad, edit the config.txt file.

Scroll down the file until you find the following lines

#hdmi_force_hotplug=1
#hdmi_group=1
#hdmi_mode=1

The lines may be seperated by other line, but we need them to be like the following.

hdmi_force_hotplug=1
hdmi_group=2     
hdmi_mode=82

Note the # are removed
Next find the three lines

#Enable DRM VC4 V3D driver on top of the dispmanx display stack
dtoverlay=vc4-fkms-v3d
max_framebuffers=2

Now add # in fron of the send two lines

#dtoverlay=vc4-fkms-v3d
#max_framebuffers=2

Now save this file.
This will allow us to connect with VNC later and get a resolution greater than 640x480.

Next we need to add two files.

Create a new file called ssh.
Make sure the file has no extention like txt or bat, it must have no extention, this file does not need any thing in it, it just has to exist.
When the Raspberry Pi boots for the first time, when it finds this file name present, it will enable SSH so we can connect to  it over the network.

Next we need to create a second file, this time it will have content. :-)
The file must be named wpa_supplicant.conf
It will have the folling text in it.

country=AU
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
scan_ssid=1
ssid="your_wifi_ssid"
psk="your_wifi_password"
}

You will need to change the your_wifi_ssid and the your_wifi_password to match your own WiFi network.
Also make sure the country is set for your country, I'm in Australia, so it's AU, in the USA make it US and in the UK, make it UK.
When editing this file, use notpad or better still Notepad++, do not use word or wordpad.

Save the file and tell windows to eject the drive, when windows tells you to, remove the MicroSD Card.

You can now install it in the Raspberry Pi.

Now for the next challenge :-)
Once your Raspberry Pi has booted up, you will need to find it on the network.
If your lucky, you can ping rasperrypi.local and it will return an address with a ping time.
If this works, your all set for the next step, if not, you will need to find a network scanning program.
On my mobile phone, I use Fing, then see if you can find the new device there.

Assuming you can find the Raspberry Pi, we will need to connect to it using SSH.
On a windows machine, I use Putty.
https://www.putty.org/
When you start Putty,  it will ask for the address, just type in raspberrypi.local, or the IP address you found, make sure SSH is selected and click on Open.
If all goes well, you will get the prompt:
login as:
enter pi
when asked for a password, enter
raspberry
That should log you in.
Now for the fun stuff :-)
We need to setup the Raspberry Pi so we can access it from VNC, by default, this is disabled.
To do this we need to run the config program as the super user.
Ender the following line
sudo raspi-config
This will start the Rasperry pi Config program.  Take care while in this program.
Using the arrow keys, scroll down to the Interface Options and press enter.
On the next screen, scroll down to the VNC line and press enter.
You will be asked, Would you like the VNC Server to be enabled?
Select yes with the arrows or tab key and press enter.
It will then tell you the VNS Server is enabled, press enter.
At this point you can tab until <Finish> is highlighted or you can enable the other interface options we are going to use, like the camera, I2C, TTL Serial and the GPIO.

After you have exited, it may give you the option to reboot, answer yes.
Allow the Raspberry Pi some time to reboot, then you can log in using VNC
If you don’t have VNC installed on your computer, then check out this tutorial: https://www.softwarert.com/setup-realvnc-server-on-pc/
When you first connect with VNC, it will guide you through the first use setup, this can take some time, but remember to skip the network setup sectio as you have already done it.

## Setting up Java 11.

MyRobotLab (MRL) reqires Java 11 to be installed on the Raspberry Pi before it will run.
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install openjdk-11-jdk

Java 11 tends to use the HDMI port for it’s audio interface regardless of what you set in the main OS desktop,  But this can be fixed. 😄 
sudo nano /etc/java-11-openjdk/sound.properties
Add to following to the file
javax.sound.sampled.Clip=com.sun.media.sound.DirectAudioDeviceProvider
javax.sound.sampled.Port=com.sun.media.sound.PortMixerProvider
javax.sound.sampled.SourceDataLine=com.sun.media.sound.DirectAudioDeviceProvider
javax.sound.sampled.TargetDataLine=com.sun.media.sound.DirectAudioDeviceProvider

This next step is only needed if you installed the Bullseye version of the Raspbian OS.
git clone https://github.com/WiringPi/WiringPi.git
cd WiringPi
./build
cd ..


## Installing MyRobotLab

Download the latest MyRobotLab from:
http://myrobotlab.org/
using the web browser thats installed with Raspbian.
Click on the link latest to download MRL, near the top left hand side, at the time this document was created that was 1.1.694.

![MyRobotLab web site](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1641116633602_Download_MRL.png)


This will download the myrobotlab.zip into the downloads folder.
Using the “File Manager” navigate to:
/home/pi/Downloads
This is where you will find the myrobotlab.zip you just downloaded.
Right click on the file and select extract all here.
This will create a new folder, you can rename this folder if you like to something that is easier to type.  I like “MRL” 🙂 
Next I cut the MRL folder from download and paste it into the pi folder.
open a terminal window, black icon in the top left corner of the screen.
type in the following:
cd MRL
./myrobotlab.sh
This will start the installation process of MyRobotlab.
This will also take a bit of time, about 1.5 hours on a Raspi 4 and about 2 hours on a Raspi 3.
Whe the install is finished, it willl start the web browser and open the WebGUI interface to MRL

