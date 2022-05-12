from multiprocessing import Process, Array
import board
import neopixel
import pyaudio
import numpy as np
import time
import wave
from config import *
from util import FrequencyPrinter

import math

# Observation 
# creating initial data values
# of x and y
x = np.linspace(0, 64, 64)
y = np.linspace(0, 64,64)
 
# to run GUI event loop
#plt.ion()
 
# here we are creating sub plots
#figure, ax = plt.subplots(figsize=(10, 8))
#line1, = ax.plot(x, y)
 
# setting title
#plt.title("Geeks For Geeks", fontsize=20)
 
# setting x-axis label and y-axis label
#plt.xlabel("X-axis")
#plt.ylabel("Y-axis")


def getPixelIndex(x,y):
    x = GRID_WIDTH - x -1 if (y % 2 == 1) else x
    return y * GRID_WIDTH +x


# Inspired from https://github.com/IzzyBrand/ledvis/tree/0b51564b47a70eb9d21d5f149e517cbfbcdb0e4f
# 
def sampler(sample_array):
    audio = pyaudio.PyAudio() # create pyaudio instantiation
    wf = wave.open(MUSIC_FILE, 'rb')
    WF_RATE = wf.getframerate()

    stream = audio.open(
            format = audio.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = WF_RATE,
            output=True,
            frames_per_buffer=CHUNK_SIZE
        )
    fp = FrequencyPrinter('Sampler')

    #read data
    data = wf.readframes(CHUNK_SIZE)
    

    # countdown
    for x in range(3):
        print(x)
        time.sleep(1)
    prev_write = time.time() # save for the next loop
    while data != '':
        # actually playing the sound.
        #stream.write(data)

        #Byte Data to Int
        if PRINT_LOOP_FREQUENCY: fp.tick()
        int_data = np.fromstring(data, dtype="int16")
        
        fourier = np.fft.rfft(int_data)
        fourier = np.delete(fourier,len(fourier)-1)
        power = np.log10(np.abs(fourier))**2
        power = np.pad(power,(0,256-len(power)))
        power = np.reshape(power,(16,math.floor(CHUNK_SIZE/ 16)))
        matrix = np.int_(np.average(power,axis=1))
        matrix = np.delete(matrix,len(matrix)-1)

        if sample_array.acquire(False):
            sample_array[0:15] = matrix
            sample_array.release()

        data = wf.readframes(CHUNK_SIZE)

        print(matrix)
        # Sleep for the framerate if neccessary.
        sleep_time = (CHUNK_SIZE / WF_RATE) - (time.time() - prev_write)
        if sleep_time > 0: time.sleep(sleep_time)
        prev_write = time.time() # save for the next loop
    # cleanup stuff.
    stream.close()    
    audio.terminate()

    

def visualize(sample_array):
    # Intialize Strip
    strip = neopixel.NeoPixel(board.D18,150,auto_write=False)
    fp = FrequencyPrinter('Visualize')
    prev_write = time.time() # save for the next loop

    while True:
        if PRINT_LOOP_FREQUENCY: fp.tick()
        for x, intensity in enumerate(sample_array):
            if intensity >= 40:
                intensity = 39
            normalized = int(intensity / 4)
            for y in range(GRID_HEIGHT):
                if y < normalized:
                    strip[getPixelIndex(x,y)] = (255,0,0)
                else:
                    strip[getPixelIndex(x,y)] = (0,0,0)
        
        sleep_time = LED_WRITE_DELAY - (time.time() - prev_write)
        if sleep_time > 0: time.sleep(sleep_time)
        strip.show()
        prev_write = time.time() # save for the next loop
    

# Taken from https://github.com/IzzyBrand/ledvis/tree/0b51564b47a70eb9d21d5f149e517cbfbcdb0e4f
# Used for Multiprocessing
if __name__ == '__main__':
    sample_array    = Array('i', np.zeros(GRID_WIDTH, dtype=int))
    sampler_process    = Process(target=sampler,         name='Sampler',         args=(sample_array,))
    visualizer_process = Process(target=visualize,      name='Visualizer',      args=(sample_array,))

    processes = [sampler_process,  visualizer_process]

    for p in processes: p.start()
    for p in processes: print("Started {} on PID {}".format(p.name, p.pid))
    for p in processes: p.join()

    
    






