"""
                                                                                   Version 2.2.0 (20211127)
Joystick Gremlin plugin for changing Virpil device's LED colors.
It uses Virpil's software to talk to your devices.

You can send aUEC tips in Star Citizen to IsaacHeron. Or gift me a Carrack :D
Contact me in SC, E:D, on the Virpil forums or /r/HOTAS Discord (IsaacHeron everywhere). Isaac-H on Reddit.

Enhancements by Oliver Ernster aka Cmdr ASmallFurryRodent for faster LED responses and improved delay handling.
Also made it a class and did some refactoring to make the code more elegant.
NEW: Added stateful button momentary presses so you can, for example, press a momentary button to set landing 
gear LEDs and they will stay on until you press the button again; basically, sometimes you don't want it to 
timeout or immediately turn off.  Also NEW: Blinking LED(s) capability added.
I can be contacted on /r/HOTASDiscord or in a lot of E:D discords.

Or thank the original script author, Painter, on whose plugin this one is based.


>>> >>                                                                                               << <<<
>>> >>>        Use at your own risk! No one else but you is responsible if something breaks!        <<< <<<
>>> >>                                                                                               << <<<


Fly safe! o7



****************
  Installation
****************

- Save this file to your disk

- Edit the path to the Virpil LED tool below in the code (line 171).
-- Search for "pathToProgram" in this file and change the path to the one on your system. (Use forward slashes.)
-- The LED tool is part of Virpil's software (at least as of January 2021) and is located in that install directoy.

- Add this plugin to Joystick Gremlin (JG)
-- Open JG and go to the last tab "Plugins"
-- Click "Add Plugin" at the window's bottom, navigate to this file and open it
-- You should see this plungin in the list

- Configuring a LED
-- Click the "+" button to add a plugin instance to your JG config, rename via the pencil button
-- Click the cogwheel button to change the settings of this instance
-- (see below for options)
-- Save the JG config

>>> NOTE - BUG:
  JG seems to have a bug where you can only change the settings once without reloading.
  When going back to the configuration of an earlier instance, not all values will be loaded.
>>> WORKAROUND:
  Add and configure all the instances you need exactly once, don't go back to a previous one!
  Save the JG config and immediately reload it. Now all plugin instance settings should display correctly and are editable
  once (before save and reload).



*************************
  CONFIGURATION OPTIONS
*************************

The labels have tooltips in JG, so read those, too.

MODE
  This is the JG mode, not a Virpil one. If you don't use JG modes, don't change this.
  JG changes a mode first, if bound to a button that also changes the LED color. At least in my testing.
  Using modes might not behave as expected, do some testing of your own.

BUTTON
  Click the button and JG asks for input from one of your device's hardware buttons.
  This button (switch, encoder, etc.) triggers the LED change.

LED DEVICE
  Same as above, but this time the pressed button indicates the device the LED is located on.
  The pressed button doesn't matter, we are only interested in the device!

LED NUMBERS
  This is the good stuff. A space seperated list of all LED IDs that will be changed. You can just input one ID of course.
  The IDs don't correspond to the button names on the device and also are different from the IDs used by Virpil's config tool.
  See the list below for ID numbers you need to use in this plugin. If you use a device not listed there, experiment.
  E.g. the LEDs of buttons B1, B2 and B3 on Control Panel #1 use IDs 16, 13 and 15. Yes, in that order...

DELAY (MS)
  Minimum time im milliseconds the color will be changed/shown for.
  Delays the following color changes by the set amount of ms and might freeze/delay virtual Gremlin input.
  Keep at default of 1ms if possible.

CHANGE ON INPUT DE/ACTIVATION
  Changes the LED to the set color when the input is released/pressed. You can use both options or only one at a time.

DE/ACTIVATION: RED/GREEN/BLUE
  The color values for the de/activation change.
  You define the RGB color brightness for each of the colors by setting a value.
  The Virpil LED tool allows one of four values for each color: 
    Off: 0 - 0% in Virpil config tool
    Low: 1 - 30%
    Mid: 2 - 60%
    Max: 3 - 100%

TOGGLE RETAIN STATE OF LEDS UNTIL PRESSED AGAIN
  Changes the LED to the activation color when the input is pressed. On second press of the button, state 2 colour values will be used.

STATE 2: RED/GREEN/BLUE
  The color values for state 2 of a momentary button press.
  You define the RGB color brightness for each of the colors by setting a value.
  The Virpil LED tool allows one of four values for each color: 
    Off: 0 - 0% in Virpil config tool
    Low: 1 - 30%
    Mid: 2 - 60%
    Max: 3 - 100%



***********
  LED IDs
***********

These IDs are for devices used in the stand-alone USB mode. If you daisy-chain devices via the AUX port you have to find out
on your own what the correct IDs or the secondary device's LEDs are.


Stick (Alpha)

	LED ID: 1


Throttle (CM2; CM3 should be the same)

	B1 LED ID: 5
	B2 LED ID: 6
	B3 LED ID: 7
	B4 LED ID: 8
	B5 LED ID: 9
	B6 LED ID: 10


Control Panel #1

	B1 LED ID: 16
	B2 LED ID: 13
	B3 LED ID: 15
	B4 LED ID: 12
	B5 LED ID: 14
	B6 LED ID: 11

	B7 LED ID: 8
	B8 LED ID: 9
	B9 LED ID: 10
	B10 LED ID: 5
	B11 LED ID: 6
	B12 LED ID: 7


Control Panel #2


- Aircraft LEDs
	Top         LED ID: 9
	Middle      LED ID: 10
	Flaps left  LED ID: 11
	Gear left   LED ID: 12
	Gear middle LED ID: 13
	Gear right  LED ID: 14
	Flaps right LED ID: 15

- Note: if using aux to connect your CPv2 to your CM3 the aircraft LED IDs are: 29-35
- Thought I haven't tested them, I suspect the other LEDs on the panel are also higher numbers;
recomment you experiment.

- Button LEDs
	B1 LED ID: 6
	B2 LED ID: 5
	B3 LED ID: 8
	B4 LED ID: 7

	B5 LED ID: 21
	B6 LED ID: 18
	B7 LED ID: 20
	B8 LED ID: 17
	B9 LED ID: 19
	B10 LED ID: 16




*** *** end of documentation *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***

"""
from datetime import datetime, timedelta
from time import sleep
import subprocess
import os
import sys
import threading
import logging

import gremlin
from gremlin.user_plugin import *


log_filename = 'vpc_leds.log'
current_dir = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(filename=os.path.join(current_dir, log_filename), level=logging.DEBUG)

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ###               Path to Virpil LED program VPC_LED_Control.exe                ### ###
### ###           Use forward slashes ("/") instead of backslashes ("\")!           ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


pathToProgram = "C:/Program Files (x86)/VPC Software Suite/tools/VPC_LED_Control.exe"


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ###   Enjoy the blinkenlights!  ### 

buttonPress = PhysicalInputVariable(
		"Button",
		"Button that triggers the color change.",
		[gremlin.common.InputType.JoystickButton]
)

ledDeviceInput = PhysicalInputVariable(
		"LED Device",
		"The device with the LED to be changed. Press ANY button on that device.",
		[gremlin.common.InputType.JoystickButton]
)

mode = ModeVariable("Mode", "The mode in which to use this mapping")
		# mode.value defaults to earliest in alphabet, not to current instance name nor to root mode

ledNumbers = StringVariable(
			"LED numbers",
			"LEDs to be lit, space seperated list.\nDoes NOT correspond to the button numbers on the device\nor VPC Config tool! See plugin code for details!",
)

displayDelay = IntegerVariable(
		"Delay (ms)",
		"Minimum time im milliseconds the color will be changed/shown for.\nDelays the following color changes by the set amount of ms\nand might freeze/delay virtual Gremlin input.\nKeep at default 1ms if possible.",
		500,
	0,
	25000
)

changeOnActivation = BoolVariable(
		"Change on input activation",
		"Changes the color to the values below when the input is pressed.\nNOTE: Might not show correctly or even reset when using the cogwheel to edit another instance.\nAdd an LED, configure, and save profile. Reload before making changes.",
		True
)

colourRed = IntegerVariable(
		"Activation: Red",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

colourGreen = IntegerVariable(
		"Activation: Green",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

colourBlue = IntegerVariable(
		"Activation: Blue",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

changeOnDeactivation = BoolVariable(
		"Change on input deactivation",
		"Changes the color to the values below when the input is released.\nNOTE: Might not show correctly or even reset when using the cogwheel to edit another instance.\nAdd an LED, configure, and save profile. Reload bedfre making changes.",
		False
)

defaultRed = IntegerVariable(
		"Deactivation: Red",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

defaultGreen = IntegerVariable(
		"Deactivation: Green",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

defaultBlue = IntegerVariable(
		"Deactivation: Blue",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

ledState = BoolVariable(
		"Retain state of LEDs until pressed again",
		"Keeps LEDs in activation colour state until primary button pressed again to revert to second state.  (Deactivation will be ignored)",
		False
)

blink = BoolVariable(
		"Blink between LED colour states until deactivated",
		"Switch between state 1 (activation colour) and state 2 (state 2 colour) until deactivated or state button pressed again.",
		False
)

blinkTimer = IntegerVariable(
		"Blink Timer (ms)",
		"Time im milliseconds between blink state changes of LED colours.",
		2000,
	2000,
	25000
)

state2ColourRed = IntegerVariable(
		"State 2: Red",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

state2ColourGreen = IntegerVariable(
		"State 2: Green",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)

state2ColourBlue = IntegerVariable(
		"State 2: Blue",
		"Color intensity (Off: 0; Low: 1; Mid: 2; Max: 3)",
		0,
	0,
	3
)


class MThreading(object):
    def __init__(self):
        self.threads = []

    def _run_thread(self, fn, *args, **kwargs):
        #self.threads = [t for t in self.threads if t.is_alive()]
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        self.threads.append(thread)


MT = MThreading()


class LEDHandler(object):
	def __init__(self):
		gremlin.util.log( "in LEDHandler contructor" )
		self.ledStateDict = {}
		
	def init(self, event, vjoy, joy):
		gremlin.util.log( "in init" )
		self.event = event
		self.vjoy = vjoy
		self.joy = joy
		self.cv = ["00", "40", "80", "FF"]
		self.deviceDict = {}
		self.colourStack = 0
		
	def handle_led_state(self, blinking=False):
		gremlin.util.log( "in handle_led_state" )
		if ledState:
			if ledNumbers in self.ledStateDict.keys():
				if self.ledStateDict[ledNumbers]["state"] == 1: 
					self.ledStateDict[ledNumbers] = { "state": 2,
												 "red": state2ColourRed,
												 "green": state2ColourGreen,
												 "blue": state2ColourBlue,
												 "blinking": blinking }
				elif self.ledStateDict[ledNumbers]["state"] == 2: 
					self.ledStateDict[ledNumbers] = { "state": 1,
												 "red": colourRed,
												 "green": colourGreen,
												 "blue": colourBlue,
												 "blinking": blinking }
			else:
				self.ledStateDict[ledNumbers] = { "state": 1,
											"red": colourRed,
											"green": colourGreen,
											"blue": colourBlue,
											"blinking": blinking }
			self.colourRed = self.ledStateDict[ledNumbers]["red"]
			self.colourGreen = self.ledStateDict[ledNumbers]["green"]
			self.colourBlue = self.ledStateDict[ledNumbers]["blue"]
		else:
			self.colourRed = colourRed
			self.colourGreen = colourGreen
			self.colourBlue = colourBlue

	def change_leds(self, vID, pID, ledNumbers):
		gremlin.util.log( "in change_leds")
		self.handle_led_state(blinking=False)
		ledArray = ledNumbers.value.split()
		for ledNumber in ledArray:
			self.doColour(vid=vID, pid=pID, led=ledNumber,
				r=self.cv[ self.colourRed.value ], g=self.cv[ self.colourGreen.value ], b=self.cv[ self.colourBlue.value ])

	def pause(self, timer, thisTime, nextColourTime):
		gremlin.util.log( "in pause")
		if timer > 0:
			nextColourTime = datetime.utcnow() + timedelta(milliseconds=timer)
		while thisTime < nextColourTime:
			sleep( 0.01 )
			thisTime = datetime.utcnow()

	def process_led_changes(self, vID, pID, ledNumbers, timer):
		gremlin.util.log( "in process_led_changes" )
		ledArray = ledNumbers.value.split()
		thisTime = datetime.utcnow()
		nextColourTime = datetime.utcnow()
		self.stop_blinking = False
		if self.event.is_pressed and changeOnActivation.value:
			self.change_leds(vID, pID, ledNumbers)
		self.pause(timer, thisTime, nextColourTime)
		# self.stop_blinking = True
		if blink.value:
			while not self.stop_blinking:
				self.change_leds(vID, pID, ledNumbers)
				self.pause(blinkTimer.value, thisTime, nextColourTime)
		if not self.event.is_pressed and changeOnDeactivation.value and not blink.value:
			for ledNumber in ledArray:
				self.doColour(vid=vID, pid=pID, led=ledNumber,
					r=self.cv[ defaultRed.value ], g=self.cv[ defaultGreen.value ], b=self.cv[ defaultBlue.value ])

	def handle_led_scenario(self, vID, pID, ledNumbers):
		gremlin.util.log( "in handle_led_scenario" )
		if not blink.value:
			timer = displayDelay.value
			self.process_led_changes(vID, pID, ledNumbers, timer)
			return
		else:
			timer = blinkTimer.value
			self.process_led_changes(vID, pID, ledNumbers, timer)				
		ledArray = ledNumbers.value.split()
		for ledNumber in ledArray:
			self.doColour(vid=vID, pid=pID, led=ledNumber,
				r=self.cv[ defaultRed.value ], g=self.cv[ defaultGreen.value ], b=self.cv[ defaultBlue.value ])

	def colour_main(self):
		gremlin.util.log( "in colour_main" )
		self.buGuid = f"{ledDeviceInput.device_guid}"
		if self.buGuid not in self.deviceDict:
			# run once, or if device has been added at run time
			self.list_devices()

		vID = self.deviceDict[ self.buGuid ][ 'vID' ]
		pID = self.deviceDict[ self.buGuid ][ 'dID' ]
	
		self.handle_led_scenario(vID, pID, ledNumbers)		
	
	def doColour(self, vid, pid, r, g, b, led="01"):
		gremlin.util.log( "in do_colour" )
		if self.colourStack > 0:
			# getting too complex
			return
		self.colourStack += 1
		
		run = f"{pathToProgram} {vid} {pid} {led} {r} {g} {b}"
		
		# gremlin.util.log( f"run -> { run }" )
		subprocess.Popen( run, creationflags=subprocess.CREATE_NEW_CONSOLE )
		self.colourStack -= 1

	def list_devices(self):
		gremlin.util.log( "in list_devices" )
		devs = gremlin.joystick_handling.physical_devices()
		for d in devs:
			dGuid = f"{ d.__dict__['device_guid'] }"
			vID = f"{d.__dict__['vendor_id']:04x}"
			dID = f"{d.__dict__['product_id']:04x}"
			self.deviceDict[ dGuid ]= { 'vID': vID, 'dID' : dID }


bPress = buttonPress.create_decorator(mode.value)
lh = LEDHandler()

@bPress.button(buttonPress.input_id)
def myColour(event, vjoy, joy):
	lh.init(event, vjoy, joy)
	MT._run_thread(lh.colour_main)


# EOF