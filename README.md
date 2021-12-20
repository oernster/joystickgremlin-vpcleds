# joystickgremlin_vpcleds
Plugin to Joystick Gremlin to enable control over Virpil control panel LEDs

# Version 2.6.0

# Features: 
1) Change one or more LED colours on activation or deactivation of a button, optionally with timeout.
2) Momentary button LED state control e.g. landing gear lights when your game only has a single button but you want to set LEDs to one colour until you press it again to switch back.
3) You can now configure blinking between LED colour states continually with a timer setting and also choose whether you want to 
use a momentary button or a hold button for the purpose.

# Demo
Here's a downloadable video of a demo of my Virpil Gear with this plugin all configured nicely:
https://www.dropbox.com/s/w5uh86u9rxxtww7/20211129_170955.mp4?dl=0

# Instructions for use
Download the VPC_LEDs.py file and then put it somewhere safe on your PC.

I'm assuming you have setup vjoy (install this first) and Joystick Gremlin appropriately (you can google for how to do this online).

1) In plugins in Joystick gremlin, choose the VPC_LEDs.py file you downloaded.

2) Create an instance, rename it using the pencil button and click on the cog.

a) Select 'button' to be the button you want to activate your LED colour change(s).

b) Select 'LED Device' and press any button on that device to choose the box on which your target LED(s) will change.  (If you want LEDs on different boxes to change based on the same button press then you'll need to create a new instance for each box and configure it accordingly).

c) Choose the relevant LED numbers (space separated for multiple LEDs) based on the guide in the header of the VPC_LEDs.py text.
(It's possible you may need to experiment to find the right LED numbers for your particular setup if you have an unusual hardware setup).

d) If you want a delay in milliseconds before actioning a deactivate LEDs change of colour again, then set this value, otherwise, leave it at zero.

e) Tick change on activation, optionally change on deactivation too.

f) Choose your colours; experimentation is key here, the possible values 0, 1, 2, 3 for blue, green and red on both activation and deactivation.

g) If you want a momentary button to be stateful then tick the retain state button and set colour values for the second state press.

h) You can also define the ability to blink between primary and secondary LED colour states and set a timer for this; note that the deactivation LED colour(s) are separate from these 2 sets of LED colours.  Ensure you choose the correct button type as the check box for this; either hold/momentary button in the relevant blink checkbox.  The activated LED timer will be ignored in this scenario.

3) Repeat the creation of an instance and setup for each button press on your device that you want.

4) Save your profile, go into options in Joystick Gremlin and set it up to auto turn on the profile etc. if you want that on launch.  Do NOT tick the checkbox for launching with start of windows - I've found it crashes on launch if you do; possibly a Joystick Gremlin bug.

5) Quit Joystick Gremlin, also from the system tray if need be; worst case reboot if necessary.

6) Now when everything is prepped, you can launch JG as normal prior to running a game and everything should be setup.

o7

Oliver aka Cmdr ASmallFurryRodent

# FAQ
Q) Why can't the plugin see my Virpil device?

A) You are probably using a USB hub instead of plugging directly into your computer.  If you must use a hub, you need to use a powered USB hub or Virpil devices will not be effectively useable.  If you cannot afford a powered USB hub but still need range from your computer, perhaps consider a USB female to USB male extender cable of a suitable length.

