Robot Dog, Part 8.
In the first seven videos we built a robot dog based on the Boston Dynamics Spot, only smaller.
Now that we have finished building the hardware side of our robot dog, it is time to setup the program side.

We are using a Raspberry Pi, in this video it was a Raspberry Pi 3B, but you can optionally use a Raspberry Pi 4B with as much as 8G of Ram (Recommended)
We will also need a MicroSD card to hold the Operating System. (OS)
The last version releast was Buster, the most recent is Bullseye.
In either case you will need to use a flash program to copy it to the MicroSD card.
You can use the Raspberry Pi Imager https://www.raspberrypi.com/software/ or another imager, 
I used BalenaEtcher https://www.balena.io/etcher/
Using either program flash your chosen OS to the MicroSD Card.
After flashin, remove and re-insert the microSD card, In a windows system, it will ask you to format the card (DONT, cancel the request.)
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
When you start Putty, 
it will ask for the address, 
just type in raspberrypi.local, 
or the IP address you found, 
make sure SSH is selected and click on Open.
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

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install openjdk-11-jdk

sudo nano /etc/java-11-openjdk/sound.properties
Add to following to the file
javax.sound.sampled.Clip=com.sun.media.sound.DirectAudioDeviceProvider
javax.sound.sampled.Port=com.sun.media.sound.PortMixerProvider
javax.sound.sampled.SourceDataLine=com.sun.media.sound.DirectAudioDeviceProvider
javax.sound.sampled.TargetDataLine=com.sun.media.sound.DirectAudioDeviceProvider


git clone https://github.com/WiringPi/WiringPi.git
cd WiringPi
./build
cd ..

Download the latest MyRobotLab from:
http://myrobotlab.org/

Please Like, Subscribe and ring the notification bell to be alerted when the next video is released.
It also a form of support that costs you nothing, but does help the channel a lot.

Also please consider joining my VIP's GoLucky and Louwrens Burger and my other Patreons Lmorales45 and Ratchet in supporting the channel on Patreon.
https://www.patreon.com/Cyber_One

You can also support MyRobotLab at
https://www.patreon.com/myrobotlab

Maybe drop into the Cyber_One Discord server for a chat :-)
https://discord.gg/WzrBUTkthQ

You can join the MyRobotLab Discord server with the following link.
https://discord.gg/XygZbWwsCq

I have a number of Play-Lists that may also interest you:
Fred's modified Inmoov Robot Head created in the Fred's Head Series.
https://www.youtube.com/playlist?list=PLgXTfFM40HqEbnFfhaLPmLv_RS1ZRCilI
Fred's Head, a better stand. (This series)
https://youtube.com/playlist?list=PLgXTfFM40HqHV5EPKPULJDfbuXK1KUeeS
The Inmoov Walking Robot Series.
https://youtube.com/playlist?list=PLgXTfFM40HqEMwg9rJ078INRYWDCG66B3
Fred's Static Leg build and attach series, now finished.
https://youtube.com/playlist?list=PLgXTfFM40HqHhaHpmX4HQO9xJAz-pAsOm
The Creality CR10S5 3D Printer Series.
https://youtube.com/playlist?list=PLgXTfFM40HqH2fJ3Wsu2wX90h1_V4uI5n
The Cocoon Create Touch 3D Printer Series.
https://youtube.com/playlist?list=PLgXTfFM40HqHJlvRuSbhYUvdWBraW9tri
My Industrial videos.
https://youtube.com/playlist?list=PLgXTfFM40HqFNvDBGjblVrEkl3jrQKMDE
And finally some of my unboxing videos.
https://youtube.com/playlist?list=PLgXTfFM40HqFXHXRLBa9tsLhRQGcORZQO

See you in the next video :-).
