# joystickgremlin_vpcleds
Plugin to Joystick Gremlin to enable control over Virpil control panel LEDs

# Instructions for use
Download the VPC_LEDs.py file and then put it somewhere safe on your PC.

I'm assuming you have setup vjoy (install this first) and Joystick Gremlin appropriately (you can google for how to do this online).

Now in plugins in Joystick gremlin, choose the VPC_LEDs.py file you downloaded.

Next, create an instance, rename it using the pencil button and click on the cog.

First select 'button' to be the button you want to activate your LED colour change(s).

Now, select 'LED Device' and press any button on that device.

Next, choose the relevant LED numbers (space separated for multiple LEDs) based on the guide in the header of the VPC_LEDs.py text.

(It's possible you may need to experiment to find the right LED numbers for your particular setup if you have an unusual hardware setup).

If you want a delay in milliseconds before actioning a deactivate LEDs change of colour again, then set this value, otherwise, leave it at zero.

Tick change on activation, optionally change on deactivation too.

Choose your colours; experimentation is key here, the possible values 0, 1, 2, 3 for blue, green and red on both activation and deactivation.

If you want a momentary button to be stateful then tick the retain state button and set colour values for the second state press.

Repeat the creation of an instance and setup for each button press on your device that you want.

Now save your profile, go into options in Joystick Gremlin and set it up to auto turn on the profile etc if you want that on launch.  Do NOT tick the checkbox for launching with start of windows - it will crash; this is an issue with Joystick Gremlin and I can't do anything about that.

Now quit Joystick Gremlin, also from the system tray if need be; worst case reboot if necessary.

Now when everything is prepped, you can launch JG as normal prior to running a game and everything should be setup.

Hope this helps...

Oliver aka Cmdr ASmallFurryRodent
