# 7 Spot Micro Plane’s of Reference
In the forward and inverse kinematics, I noted that the X, Y and Z coordinates in reference to the centre of the robot and not the ground, what I may not have mentioned, is there are a number of planes of reference we can and will use. 
To make more sense of this, lets list the planes and make sure we have a good reference of what each of these planes are and how they relate to each other.
Planes of Reference is created but 3 flat plates or plane’s all perpendicular to each other with a common point of intersection being the origin.
We use the origin in most cases as the point to make measurements from in 3D space

# Robot Plane of Reference, (RPoR)

This one an the name suggests this is based on the robot its self.
In the case of Spot, its origin is cantered in the middle of the robot with the XY plane passing through the middle of each of the shoulder pivots with the front of the robot in the +Y axis, the back of the robot in the -Y axis and the left of the robot in the -X axis and the right in the +X axis. The bottom of the robot is in the -Z axis and the top in the +Z axis
Note that these + and - axis do not change are the robot is rotated in 3D space.
This is convenient for the kinematics as the various joints are attached to the body of the robot.

# Ground Plane of Reference, (GPoR)

Not surprisingly, this is where the ground, table or what ever the robot is standing on is located.
Normally, this would be in the robots -Z axis Plane of Reference, but this is not always the case, on occasion I have found this in the robots +Z axis Plane of Reference, normally after the robot has fallen over.

# Feet Plane of Reference, (FPoR)

Now for some confusion, there are in fact 4 Feet Planes of Reverence.
Each of the planes are made using 3 of the 4 feet. 
To help identify each of the 4 Feet Planes of Reference, we will call them: 

- FPFL Feet Plane Front Left made up of the Front Left, Front Right and Back Left feet.
- FPFR Feet Plane Front Right made up of the Front Left, Front Right and Back Right feet.
- FPBL Feet Plane Back Left made up for the Front Left, Back Left and Back Right feet. 
- FPBR Feet Plane Back Right made up of the Front Right, Back Left and Back Right feet.

In theory, when all the feet are at the same Z level, then all the Feet Planes of References are all level with each other. 
We will also call the Feet Plane of Reference that is in alignment with the Ground Plane of Reference the Primary Feet Plane of Reference.
Each of the triangles that make up the planes has a centre point, and we need to keep the inertial centre of mass within the Feet Plane that matches the Ground Plane of Reference in order to maintain the robots balance.  
When we keep the robots centre of mass within the triangle of the Primary Feet Plane of Reference, this is known as Static Balancing.
If we can keep the Inertial centre of mass within the triangle of the Primary Feet Plane of Reference while the robots centre of mass falls out side this triangle, then we are using Dynamic Balancing.

# Centre of Mass Plane of Reference, (CoMPoR)

Just to add to the confusion here, we have the centre of the robot at the origin of 0,0,0. 
But your robot might have extra equipment attached on the top at the front such as an Arm, Lidar sensor or a camera.  
This additional load will move the point of balance away from the centre of origin.
This also move the point of balance in the direction of the additional load.
In most cases, we will reference the Origin of the centre of mass relative the the robots origin, an offset you can use.

# Inertial Plane of Reference, (IPoR)

In theory we should be able to make the robot walk using Static Balancing, but if the Ground Plane of Reference is not in line with Gravity, then the robot will still fall over.
The Inertial Plane of Reference is a combination Gravity and Inertia.
There is always an accelerating force applied to the robot, even when it is fully powered down.
This is normally in the downward direction and in known as gravity.
There are devices such as the MPU6050 that can sense the magnitude and direction of this acceleration. 
Using this device, we know, for the most part, which way is down.
As a result we can use this to help confirm which of our 4 Feet Planes of Reference is the Primary one.
Just a note, the origin for this plane of reference is technically located in the middle of the IMU, in our case the centre of the MPU6050 chip

# Using the Planes of Reference.

Something to be aware of, in each case I have described where each of these planes of reference have the origin, but the orientation between each of the planes can also be vastly different.
We can in a number of cases combine different planes of reference, such as the COM and the Inertial Planes of reference.
In this case we would use the CoMPoR as the Origin and the IPoR as the Orientation to create the Inertial Centre of Mass.
So how does knowing all this help us?
In our case, we know the position of the feet in relation to the RPoR and we can use the IMU to get the orientation, but how do we know if we are moving the feet to be out of balance?
We need to first convert the feet X, Y and Z positions for the RPoR to the CoMPoR/IPoR.
This conversion is not that hard for the offset.
Just subtract off the current feet X, Y, Z coordinates and now they are relative to the CeMPoR right!
Well that’s half of it.
Now we need to rotate the coordinates.
This is not as hard as you might think.
Lets work in one plane at a time, 2D maths is easier to work out 🙂 
Lets first work out the distance between the foot we are working on and the CoMPoR.
This is simple Pythagoras theory.
Lets call the front left foot X, Y and Z coordinates:
FLX, FLY and FLZ.  (Same as used in the program)
This is in the RPoR and is the results of the Forward Kinematics calculations based on the servo positions for that leg.
comX, comY and comZ are the offset values for the Centre of Mass from the robots origin.
comFLX = FLX - comX
comFLY = FLY - comY
comFLZ = FLZ - comZ
Now that we have those new coordinates, lets get the X-Z axis length and call FLXZL.
$$FLXZL = \sqrt{comFLX^2 + comFLZ^2}$$
$$FLYZL = \sqrt{comFLY^2 + comFLZ^2}$$
Now we got the easy ones out of the way we need to work out the angles between the robots plane and the line to the foot from the centre of mass.
$$FLXA = Sin^-1(\frac{comFLX}{FLXZL})$$
$$FLYA = Sin^-1(\frac{comFLY}{FLYZL})$$
Now that we have the angle between the foot and the body, we can now add the angles from the IMU unit
The IMU supplies the angle in the form of Pitch Roll and Yaw.
In our calculations, we are going to ignore the Yaw value.
The other thing of note, the values supplied are always in radians.
$$FLimuXA = FLXA + imuRoll$$
$$FLimuYA = FLYA + imuPitch$$
Now that we have our new angle for the line to the foot, we can recalculate is position relative to the combined CoM and Inertial Orientation.
$$imuFLX = Sin(FLimuXA ) * FLXZL$$
$$imuFLY = Sin(FLimuYA ) * FLYZL$$
$$imuFLZ = Cos(FLimuYA)*FLYZL = Cos(FLimuXA)*FLXZL$$ 

# Where is the Ground?

So we worked out how to calculate the position of the feet in relation to the Centre of Mass and the inertial Orientation, but how does that help us in our quest to balance and walk.
Before we can walk or balance, we need to know where the ground is.
This can be done by looking at a combination of the feet in relation to the ICoM plane.
This X-Y point of this plane will fall within the boundary of at least 3 feet unless the robot is falling over.
If for example, we draw a line between the Front Left foot and the Back Right foot, it could be described by an equation $$Y = (a*X) + b$$
In this case the *b* is the thing of importance to us. 
the variable *b* represents the point the line crosses the Y-Axis.
In this case, if we wanted to lift the Front Right foot, we would want the ICoM to be on the lower left side of that line between the Front Left and Back Right, that is the b value would need to be positive.
So how do we work this out?
Lets start by working out the slope of the line.
$$a = \frac{imuFLY - imuBRY}{imuFLX - imuBRX}$$
Now that we have the slope *a* we can now use one of the feet coordinates to find the Y Intercept *b*.
Lets first transpose the full slope equation to make *b* the focus
$$b = Y - (a*X)$$
So now we can plug in our foot locations to get
$$b = imuBRY - (a*imuBRX)$$
If b is positive then we can lift the Back Left foot, if its negative, we can lift the Front Right foot.
If its one of the other two feet we want to lift, then calculate for the Front Right and Back Left.


