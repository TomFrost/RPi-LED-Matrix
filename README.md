# RPi LED Matrix Animator

## Description

This is a sample Python script to show how to animate a small grid of LEDs attached to a Raspberry Pi, and have them react to hardware input.

## The Hardware

The LED matrix can be easily made yourself and plugged into a breadboard.  You'll need 9 LEDs and a soldering iron.
Follow [this excellent tutorial](http://www.youtube.com/watch?v=SD5iW9PdRF8&feature=c4-overview-vl&list=PLhpG9Bht0q6m7E4nD12eeA-xMFUKfvS-8) by youtube user 'updowndown' to learn how to assemble the LEDs and wire them up to pins on your raspberry pi with resistors.

For the button input, purchase any simple normally-closed button that fits into your breadboard.  Connect one end to pin 1 (3.3V output) and connect the other to any available GPIO pin.  In this example, I use pin number 22.

## The Setup

Read through the UPPERCASE_VARIABLES at the top of `matrix.py` and alter them accordingly!  This is how the script knows where to find your LEDs and your button.  You can also play with the animation and multiplexing speeds here.

## The Execution

This script can be run with Python 2.7 using the latest RPi.GPIO library.  The version bundled with Raspbian is perfect.  If you're running something else, just run:

	pip install rpi.gpio>=0.5.3a

This script requires sudo privileges to run!  Execute with:

	sudo python -O matrix.pi

The -O can be omitted, but should provide slightly better performance.  If you're using Arch Linux, use 'python2' and 'pip2' in place of the above.

**REMEMEBER:** You should never run someone else's code with sudo powers unless you understand exactly what it does.  Please take the time to read the Python code and confirm that it doesn't do anything nefarious before you run it!

## The License

This code is licensed under [WTFPL](http://www.wtfpl.net/) (Warning, strong language).  Really, just do whatever you want with this code, and don't blame me if you break stuff :).

## Credits

Written by Tom Shawver for my own, very easily-amused enjoyment.
