## Hardware

- Raspberry Pi
- 16ft of Ws2818b LED Strips

## Libraries used

- Pyaudio
- NeoPixel
- Numpy
- Wave

## Resources Used and Code Cited

- [LED Visualizer](https://www.youtube.com/watch?v=aQKX3mrDFoY&t=505s)

- [Spectrum Analyzer](https://www.youtube.com/watch?v=aQKX3mrDFoY&t=505s)

- [Pyaudio Docs](https://people.csail.mit.edu/hubert/pyaudio/docs/)

- [Wave Docs](https://docs.python.org/3/library/wave.html)

- [RGB Matrix](https://www.hackster.io/gatoninja236/raspberry-pi-audio-spectrum-display-1791fa)

- [Fourier Transform Basics](https://towardsdatascience.com/fourier-transform-everybody-does-it-f763c60f598e)

- [Numpy Docs](https://numpy.org/doc/stable/index.html)

- [Neopixels](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage)

# Day 1

I came in the studio today wanting to test to test out the led and the raspberry pi. I scrounge around the studio for a micro sd card, boot it with the latest version of raspberry pi, connect everything to one of the computer setups in the room and boot on pi.
I then attempt to get led lights on using the neopixel library.
I have a couple issues, the neopixel library didn’t seem to be turning on the first led.
It was also completely unpredictable and when I would set a pixel to a value, different pixels would come on every time.
I realized, the leds I bought were properly not ws2812b led even though they were advertised as them, and used some other system.
There were these microchips on the leds doing some processing and I would have to return and buy different ones.

https://magpi.raspberrypi.com/articles/neopixels-python

# Day 2

I have the new leds, and they work properly. I’m using the neopixels api currently to mess with the leds and have it plugged into a 5v, ground, and data pin. (GPIO 18).
I’m currently messing around if I can’t chain these pins or not.

# Day 3

Started researching how to process the sound and get amplitudes of frequencies out of that.
My goal is to split the frequency band into a lot of different waves.
I found a project that I’ll be basing mine off of using a one dimensional array.

I'm also been researching a lot about FFT and how they work.
I still can't fully process what going on but I'll be watching videos.

# Day 4

I start learning how to read the wav file and sampling it using pyaudio. I take these individual samples and attempt to plot them in matplotlib.
I eventually am able to get a basic FFT setup going and able to print out matrix arrays.
I use numpy to perform a fourrier transform and shape the data to match the LED grid.

# Day 5

It's getting close to the deadline, so I should start soldering and getting final preparations ready.
I decide on doing a 15x10 LED grid and cut my 150pixel led strip into 15 pixels strip. I solder them together
with the help of a friend and test each connection with a voltmeter. After I confirm soldering was good,
I implement the finishing touches and program the fourier transform and a seperate visualize array.

I'm having a lot of issues with pyaudio and processing data. I try the multiprocessing approach but it doesn't speed up the processing at all. I then realize, its pyaudios fault and raspberry PI just has a lot of issues with audio drivers. After spending a good couple hours, the final demo just has me starting the music at the same time as the code, but on any other machines, it would work.
