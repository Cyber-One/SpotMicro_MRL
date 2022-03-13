# 2) Spot Micro Hardware

# Hardware Build.

I printed most of the parts using a transparent PLA, but you can use what ever material you prefer.
We will start the build with the legs.  I’ve produced 7 videos showing how i built this robot and there will be links below along with a list of all the parts I used.

## Left Front Leg.

Start by mounting the first servo into the part L_wrist_mg.stl you can install one of the foot.stl flexiable part on to the end of the wrist, this is the lower part of the leg.
This is the Wrist Servo. This servo is held in place by 2 x M4 x 20mm long screws with hex nuts at the top and 2 x M4 x 25mm long screws with hex nuts at the bottom.
You will need to modify one of the servo horns supplied with the servo with four arms to have only the one arm in order to fit the space for it in the L_arm_mg.stl.
The original instructions was to glue this into place, but I may yet plastic weld this into place using a 3D Pen.
I used a servo tester to set the position of the servo, in the video for the left leg, I set this to max position 2200uS and fitted it with the leg folded all the way, in hind sight, I should have gon e the other way, set the servo tester to 800uS and fitted it with the leg straight. 
I will be using MRL to drive the servo via a PCA9685 and it can driver the servo a bit further than the servo tester can, having the spare movement space past the straight could be an advantage.
Next mount a F526 bearing to the knob on the other side of the wrist inline with the servo output shaft.  Run the servo wire in the groove for it and fit the L_arm_cover.stl, this is then secured with the M3 x 20mm long screw.
Next install the 4 M4 square nuts into the slots provided where the second servo will be installed, you need to do this before installing the servo as you can’t get to them once the servo is in place. We hold the nuts in by installing the second servo.  This by the way is pushed in from the side and is known as the Arm Servo.  The Arm Servo is held in place with the 4 x M4 x 20mm long screws.
I did find a cover that can go over this side entry, however it needs to be glued or welded in place, and at this point in time, I don’t know if I will need to change the servos out again 🙂 
You will need another 4 way servo horn to install into the L_arm_joint_mg.stl.  Again the designer suggested that this be glued into place.  This is another version of the arm covers that has support for another bearing and a matching arm _joint.
Using the servo tester set to midway or 1500uS, the L_arm_joint_mg.stl has a knob on the side for another bearing, this needs to be at the upper part with the side running parrallel the the arm then fit it to the Arm Servo and secure it with the screw. 
This is not how I did it in the video, but I learned a bit more later 🙂 
Next install the final servo for the front left leg with the output shaft opposite and inline with the knob for the bearing. This servo is the Shoulder Servo.
The servo is secured in place with 4 x M4 x 20mm long screws and hex nuts.
That complets the Front Left leg.

## Rest of the Legs.

The rest of the legs are basically the same as the front left leg, however the right legs have the prefix R instead of L.
Another note, the back legs have the arm_joint.stl’s swapped, that is the left one goes on the right side and vice versa.

## Body of the robot.

For this next part you will need the 2 x I_shoulder_mg.stl parts, the 2 x R_side_plate.stl and the rpi3b_plate.stl.
To make it a bit easier for myself, I assembled one of the R_side_plate.stl plates with the two I_shoulder_mg.stl, the flat side of the I_shoulder_mg.stl face into the middle of the bot with the narrower bits being the bottom.  
The R_side_plate.stl has provision on the bottom side for a mounting plate to slot into it.
Next mount all the electronic hardware onto the rpi3b_plate.stl.  
I also wired most of the connection to the various parts at this time as well and fitted the two batteries to the under side using the two battery_holder_X2.stl’s.
Slide the rpi3b_plate.stl into the provided slot and fit the second R_side_plate.stl. 
The side plates are held in place with the 4 x M3 x 10mm long screws and the M3 square nuts for each side.
The save me a bit of hassle, I welded the square nuts in place before assembly.

## The Stand.

Now is a good time to build the stand.
each of the legs SM2StandLeg.stl has two parts two to them, these are connected together, we need two of these assemblies.
The second file have the two connecting spars and 4 feet for the legs.
Once assembled you can site the body of the robot on it.

## The Front Shoulders.

One of the O_shoulder.stl parts is the the fron shoulders, in this part we with two 6 arm servo horns.  To the two front legs, we need to fit the F526ZZ flanged bearings.  The bearings will then fit into the matching holes on the front of the body.  With the servo tester connected to both the shoulder servos of the left and right front legs, and set to the midway position of 1500uS, fit the O_shoulder.stl with the 6 arm horns to the two servos.
Make sure while fitting the horns that the legs are pointing straight down.
Use 4 x M3  to attach this O_shoulder.stl to the I_shoulder.stl.
I plastic welded the nuts in place to make it easier to fit.

## The Head.

Installed in the head (F_cover.stl) are two HC-04 Ultra-Sonic Range Finder modules, these are mounted at an angle such the are pointed down a bit and so as to cross the signals about 30mm infront of the head.  Also mounted in the head is a Raspi Camera modulewhich is centered about 500 mm in front of the robot when it is standing.   There is also provision for 4 x 5mm LED’s, at this point I have not installed any, but that may change in the future.
I plastic welded the Ultra-Sonic sensor mounts and the Raspi mount into the head and connected the wires prior to mounting the F_cover.stl to the body.  This is then held in place by 4 x M5 x 12mm long screws, again I plastic weld the square nuts in first.

## The Back Shoulders.

This is a bit more complicated because we need to mount a SMPS or two here first.
I sat the SMPS in the top and used a 2.5mm drill bit to mark the two mounting holes, then moved the SMPS out of the way and drilled the two holes all the way though.
The screws I have on hand are not going to be long enough by a long shot here, and I need the head of the screws to be below the surface, to I counter bored the holes with a 5mm drill bit stopping about 3-4mm from the bottom. This allowed me to used the 2 x M2.5 12mm long stand off with M2.5 male thread one end and female on the other with the threaded end pointing down.
Later I changed this to a pair of standoffs that were female threaded at each end.
I also drilled a hole in line with where the voltage adjustment pot is on the SMPS.
It’s best to attach power to the inputs on the SMPS before you install them and set the output voltage, but sometimes you do need to fine tune then once installed.
**NOTE: These small SMPS come preset to out put 12.0V from the factory, so set it before connecting it to your Raspi**
I then after soldering wires to the moduel placed it onto the stand off and capped it with the 2 x M2.5 screws.
Initially I fitted a second SMPS, but upgrading to the HV servos means I don’t need it, yet.
Now that the SMPS is installed, time to mount the back legs.
This process is almost identical to the front legs.
Install the 6 way horns into the O_shoulder.stl, attach the two shoulder servo to the servo tester and set the servo tester to the midway position, 1500uS, add the two F526ZZ bearings and assembly it togeter with the legs pointing straight down.
Secure with the 4 x M3 x 10mm long screws and we are done this bit.

## The Back Cover.


## The Wiring Diagrams.
![](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1641088160212_SpotMicro_bb.jpg)


