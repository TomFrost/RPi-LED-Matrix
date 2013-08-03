#
# Raspberry Pi LED Matrix Animator
#
# This is a sample script to show how to animate a small grid of LEDs
# attached to a Raspberry Pi, and have them react to hardware input.
#
# The LED matrix can be easily made yourself and plugged into a breadboard.
# Follow this excellent tutorial by youtube user 'updowndown' to learn
# how to assemble the LEDs and wire them up to pins on your raspberry pi
# with resistors.
# http://www.youtube.com/watch?v=SD5iW9PdRF8&feature=c4-overview-vl&list=PLhpG9Bht0q6m7E4nD12eeA-xMFUKfvS-8
#
# For the button input, purchase any simple button that fits into your
# breadboard.  Connect one end to pin 1 (3.3V output) and connect the
# other to any available GPIO pin.  In this example, I use pin number 22.
#
# Read through the CONSTANT_VARIABLES at the top of the code and alter
# them accordingly!
#
# This script can be run with Python 2.7 using the latest RPi.GPIO
# library.  The version bundled with Raspbian is perfect.  If you're
# running something else, just `pip install rpi.gpio>=0.5.3a`
#
# This requires sudo privileges to run!  Execute with:
# sudo python -O matrix.pi
# Or, on Arch Linux:
# sudo python2 -O matrix.pi
#
# The -O can be omitted, but provides slightly better performance.
#
import RPi.GPIO as GPIO
import time

"""The number of seconds to wait before switching to the next anode
	when scanning through each column.  Setting this too high will
	create visible flicker in the LEDs, too low will cause them to
	appear dim.
"""
MULTIPLEX_DELAY = 0.002

"""An array of the three anode pins in the 3x3 LED matrix. These should
	be listed from left to right.
"""
ANODES = [12, 16, 18]

"""An array of the three cathode pins in the 3x3 LED matrix. These should
	be listed from top to bottom.
"""
CATHODES = [7, 11, 15]

"""The pin to which the ground side of the switch is connected.  Note
	that the positive side of the switch should be connected to pin
	#1 (3.3V)
"""
INPUT_PIN = 22

"""The number of seconds to spend displaying each frame of the animation.
"""
FRAME_TIME = 0.2

"""An array of animations.  Each animation is, itself, an array of frames.
	Each frame is an array of 3 rows of LEDs.  Each row is an array of 3
	1s or 0s indicating whether that respective LED should be on (1) or
	off (0).

	For example, this frame will display an X:
	[[1, 0, 1],
	[0, 1, 0],
	[1, 0, 1]]
"""
ANIMATIONS = [
	[
		[[1, 1, 1], [0, 0, 0], [0, 0, 0]],
		[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
		[[1, 0, 0], [1, 0, 0], [1, 0, 0]],
		[[0, 0, 1], [0, 1, 0], [1, 0, 0]],
		[[0, 0, 0], [0, 0, 0], [1, 1, 1]],
		[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
		[[0, 0, 1], [0, 0, 1], [0, 0, 1]],
		[[0, 0, 1], [0, 1, 0], [1, 0, 0]]
	],
	[
		[[0, 0, 0], [0, 0, 0], [0, 0, 1]],
		[[0, 0, 0], [0, 1, 1], [0, 1, 0]],
		[[1, 1, 1], [1, 0, 0], [1, 0, 0]]
	],
	[
		[[1, 1, 1], [0, 0, 0], [0, 0, 0]],
		[[0, 0, 0], [1, 1, 1], [0, 0, 0]],
		[[0, 0, 0], [0, 0, 0], [1, 1, 1]],
		[[0, 0, 0], [1, 1, 1], [0, 0, 0]]
	],
	[
		[[1, 1, 1], [0, 0, 1], [0, 0, 1]],
		[[0, 1, 0], [1, 1, 1], [0, 1, 0]],
		[[1, 0, 0], [1, 0, 0], [1, 1, 1]],
		[[0, 1, 0], [1, 1, 1], [0, 1, 0]]
	],
	[
		[[0, 0, 1], [0, 0, 0], [1, 0, 0]],
		[[0, 1, 0], [0, 0, 0], [0, 1, 0]],
		[[1, 0, 0], [0, 0, 0], [0, 0, 1]],
		[[0, 0, 0], [1, 0, 1], [0, 0, 0]]
	]
]

"""Initializes the GPIO pins
"""
def init():
	GPIO.setmode(GPIO.BOARD)
	# Turn off the anodes
	for anode in ANODES:
		GPIO.setup(anode, GPIO.OUT)
		GPIO.output(anode, False)
	# Turn on the cathodes
	for cathode in CATHODES:
		GPIO.setup(cathode, GPIO.OUT)
		GPIO.output(cathode, True)
	# Prepare our input pin
	GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(INPUT_PIN, GPIO.RISING, bouncetime=1000)

"""Sets an array of pin numbers to a boolean value

:param pins: An array of pin numbers
:param setting: A boolean value indicating that the pin is High (True)
	or Low (False)
"""
def set_to(pins, setting):
	for pin in pins:
		GPIO.output(pin, setting)

"""Displays a frame of an animation for a set period of time
	before returning.

:param anim: The index of the target animation from the ANIMATIONS array
:param frame: The index of the frame to be displayed from the specified anim
:param duration: The number of seconds for which the frame should be displayed
	before the function call ends.
"""
def show_frame(anim, frame, duration):
	start_time = time.time()
	while (time.time() - start_time < duration):
		for anode_id in range(0, 3):
			anode = ANODES[anode_id]
			GPIO.output(anode, True)
			for cathode_id in range(0, 3):
				state = not ANIMATIONS[anim][frame][cathode_id][anode_id]
				GPIO.output(CATHODES[cathode_id], state)
			time.sleep(MULTIPLEX_DELAY)
			GPIO.output(anode, False)
			set_to(CATHODES, True)

"""Loops through a single animation until interrupted with a GPIO input
	to the INPUT_PIN

:param anim: The index of the target animation from the ANIMATIONS array
"""
def run_anim(anim):
	cur_frame = 0
	while (not GPIO.event_detected(INPUT_PIN)):
		show_frame(anim, cur_frame, FRAME_TIME)
		cur_frame = (cur_frame + 1) % len(ANIMATIONS[anim])

"""Cycles through all animations in the ANIMATIONS array by displaying the
	first animation, and then incrementing through the rest every time a
	GPIO input is reached on the INPUT_PIN. When the last animation is
	reached, this will loop back to the first and repeat.
"""
def cycle_anims():
	cur_anim = 0
	while (True):
		print("Running animation %d" % (cur_anim))
		run_anim(cur_anim)
		cur_anim = (cur_anim + 1) % len(ANIMATIONS)

# Run the app!
try:
	init()
	cycle_anims()
except:
	set_to(ANODES, False)
	set_to(CATHODES, False)
	GPIO.cleanup()
