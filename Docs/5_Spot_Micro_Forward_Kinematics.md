# 5) Spot Micro Forward Kinematics

# Introduction

Forward Kinematics is working out where the feet are in 3D space relative to a common point based on the current position of the joints.
Before we get started, here is a little bit more important info that we need to work out the X, Y and Z axis position of the feet.
The common point will be in the centre of the robot.
When referencing the X, Y or Z Axis: 

- **X** is across the robot from the Left hand side to the right hand side with the left being the negative direction relative to the robot’s point of view.
- **Y** is along the length of the robot from the back to the front with the back being negative and the front being positive.
- **Z** is up and down through the robot, with negative being down and positive being up.

**Note: all frames of references are relative to the robots body and not to the ground or gravity.**

The naming convention of variables will start with either A or L, A being used for an Angle and L being used for a length.
The following letters will be used to describe joints:

- **F** is the foot. 
    The part making contact with the ground.
- **W** is the Wrist joint. 
    When used on its own represents the Servo position.
    Lets assume that when the writs joint is such the upper and lower leg sections are aligned with each other, the joint is at 0°.
- **T** is the Top of Arm Joint.
    When used on its own represents the Servo position.
    Lets work on the basis this angle is at 0° when the leg is pointing down.
- **S** is the Shoulder joint.
    When used on its own represents the Servo position.
    Lets assume when the servo is centred, the leg will point straight down and this will be the 0° position.
- **X** is the X-Axis. 
    Relative to the centre of the robot along the Axis as described above.
- **Y** is the Y-Axis. 
    Relative to the centre of the robot along the Axis as described above.
- **Z** is the Z-Axis. 
    Relative to the centre of the robot along the Axis as described above.
- **LWF** = 135 mm  Length between the Wrist joint and the foot.
- **LTW** = 110 mm  Length between the Arms joint and the Wrist joint.
- **LST** = 50 mm    Length between the Shoulder joint and the centre line of the Arm.
- **LYS** = 95 mm     Length between the centre Y plane and the shoulder joint.
- **LXS** = 38 mm    Length between the centre X plane and the shoulder joint.

 Now that all that is out of the way, we should have enough info to create the formula to calculate the various X, Y and Z coordinates of the feet.
Lets work with one foot to start with, the Front Left foot.
The easiest way to work this out is to look at each joint one after the other, We can consider for example the wrist joint being the servo that set a length between the Top of the Arm and the Foot (**LTF**).  In order to work out this length we only need two lengths and an angle, as it happens we have all of those. LWF and LTW are the two side with the output of the Wrist servo being the angle.  With all those, we can use the Law of Cosines to calculate the length LTF.

![Triangle with notations](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1640804830688_1920px-Triangle_with_notations_2.svg.png)


$$c^2 = a^2 + b^2 - 2*a*b*cos(C)$$
$$LTF = \sqrt{LWF^2 + LTW^2 - 2*LWF*LTW*cos(W)}$$
This tells us how far away the foot is from the shoulder, but not the direction, for that we need to know both the angle of the T servo and the angle formed by the LTW and the  LTF, AFW.
The above formula can be transformed to make Cos(C) the result.
$$cos(c) = \frac{a^2 + b^2 - c^2}{2*a*b}$$
While cos(c) will give us a value from an angle, to work out the angle, in Python we can use the acos(value) = angle.
$$AFW = acos(\frac{LTF^2 + LTW^2 - LWF^2}{2*LTF*LTW})$$
This can then be added to the T angle to get a total angle which represents the angle between the vertical plane and the line to the foot from the top of the arm.  Knowing this allows us to use the trigonometry function for a right angle triangle to calculate the Y-Axis position relative to the Top of the Arm.

![](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1641154333970_Right+angle+triangle.jpg)


$$sin(A) = \frac{opposite}{hypotenuse}$$ which we can translate to $$Opposite = sin(A) * hypotenuse$$
In out use case A will be the (AWF + T), and the Hypotenuse will be the LTF this will give us
$$Opposite = sin(AFW + T) * LTF$$
All we need to do then is add the Y-Offset of the front shoulders LYS to get the Y position
$$Y = sin(AFW + T) * LTF + LYS$$
This works for both the front legs, but for the back legs, we will need to subtract the LYS value.
We could start combining part of the formula to get this:
$$Y = sin(acos(\frac{(\sqrt{LWF^2 + LTW^2 - 2*LWF*LTW*cos(W)})^2 + LTW^2 - LWF^2}{2*\sqrt{LWF^2 + LTW^2 - 2*LWF*LTW^2*cos(W)}}) + T) * \sqrt{LWF^2 + LTW^2 - 2*LWF*LTW*cos(W)} + LYS$$Yeah, much easier to look at it in it component formula, besides which, we still need to use the results of some of the previous formula as we continue to calculate the X and Z axis. 🙂 
Before we move on to the next bit, lets calculate out the adjacent value which we will call LTFa.  We are going to need it in the next bit 🙂 
$$LTFa = cos(AFW + T) * LTF$$

So far we have only looked at the position of two of the servos, and we were working on a plane that is not aligned with either the Z or the X Axis. 
When we look at the legs assembly in the X-Z plane, we have a another right angle triangle with the point at the Shoulder, the Top of the arm and the Foot.
The length between the Top of the arm and the Foot when viewed in the X-Z plane is the Ajacent  length from the the calculations above.

![](https://paper-attachments.dropbox.com/s_3312125F65CA3DC01444C81917CB3E917B429E9A33B5A513DF0D3BDF0783359C_1641158083452_Leg+Assy+Triangle.jpg)


What we really need to know is the Length between the Shoulder and the Foot, (LSF) as well as the angle formed between the section between the shoulder and the Top of the arm (LST) and the LSF.  The good news is we know the angle between the LST and the Top of arm and foot sections is 90° so we can use $$LSF^2 = LST^2 + LTFa^2$$ or $$LSF = \sqrt(LST^2 + LTFa^2)$$
The angle at the Shoulder formed by the line LSF and the line LST can be calculated with $$cos(A) = \frac{LST}{LSF}$$ or $$A = acos(\frac{LST}{LSF})$$
When we add that angle to the current Shoulder position, we can now calculate the X and Z position of the foot.
$$X = sin(acos(\frac{LST}{LSF}) + S) * LSF - LSX$$
We subtract the LSX because it’s on the left side of the robot, on the right hand side we would add it.
$$Z = cos(acos(\frac{LST}{LSF}) + S)*LSF$$
So now we know the position of the foot in the X, Y and Z coordinates relative to the center of the robot.

**Just a couple of notes:**
In this example, I used degrees, in Python, most of the functions will be in radians, so we will need to do some conversions.
90° = $$\pi/2$$




