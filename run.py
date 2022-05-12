from multiprocessing import Process, Array
#from graphics import *
import board
import neopixel

import pyaudio
import numpy as np
from struct import unpack
import time
import wave
from config import *
#from visualizer import vis_list
#from strips import Strips
from util import FrequencyPrinter, CircularBuffer

#import matplotlib.pyplot as plt
import math

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




def sampler_old(sample_array):
    '''
    Sample the ADC as in continous mode and write into the shared array as a circular buffer.
    The index that has been most recently written is stored in the last slot in the array
    '''

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format=FORMAT, rate=SAMPLING_FREQ, channels=NUM_CHANNELS, \
                        input_device_index=DEVICE_INDEX, input=True, \
                        frames_per_buffer=CHUNK_SIZE)

    fp = FrequencyPrinter('Sampler')
    while True:
        if PRINT_LOOP_FREQUENCY: fp.tick()

        try:
            data = stream.read(CHUNK_SIZE)
        except IOError:
            print ('Stream overflow!')
            stream.close()
            stream = audio.open(format=FORMAT, rate=SAMPLING_FREQ, channels=NUM_CHANNELS, \
                        input_device_index=DEVICE_INDEX, input=True, \
                        frames_per_buffer=CHUNK_SIZE)
        int_data = np.fromstring(data, dtype="int16")
        # print stream.get_read_available()

        # attempts a non-blocking write to the sample array
        if sample_array.acquire(False):
            sample_start = sample_array[-1]
            sample_end = sample_start + CHUNK_SIZE

            if sample_end < SAMPLE_ARRAY_SIZE - 1:
                sample_array[sample_start:sample_end] = int_data # write the newest sample to the array
                sample_array[-1] = sample_end # store the most recent index last in the array
            # else:
            #     print 'dropped'

            sample_array.release()

    # here I was saving some sample data for testing offline
    # a = np.array(samples)
    # print 'Saving', a.shape, 'samples'
    # np.save("sample_30s_3.txt", np.array(samples), allow_pickle=True)

def getPixelIndex(x,y):
    x = GRID_WIDTH - x -1 if (y % 2 == 1) else x
    return y * GRID_WIDTH +x

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
    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)

        int_data = np.fromstring(data, dtype="int16")
        if PRINT_LOOP_FREQUENCY: fp.tick()

        fourier = np.fft.rfft(int_data)
        fourier = np.delete(fourier,len(fourier)-1)
        #print(fourier)
        power = np.log10(np.abs(fourier))**2
        #print(power)
        power = np.reshape(power,(16,math.floor(CHUNK_SIZE/ 16)))
        #print(power)
        matrix = np.int_(np.average(power,axis=1))
        matrix = np.delete(matrix,len(matrix)-1)

        if sample_array.acquire(False):
            sample_array[0:14] = matrix
            sample_array.release()

        data = wf.readframes(CHUNK_SIZE)
    # cleanup stuff.
    stream.close()    
    audio.terminate()

    

def visualize(sample_array):
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
    
        
if __name__ == '__main__':
    sample_array    = Array('i', np.zeros(GRID_WIDTH, dtype=int))
    sampler_process    = Process(target=sampler,         name='Sampler',         args=(sample_array,))
    visualizer_process = Process(target=visualize,      name='Visualizer',      args=(sample_array))

    processes = [sampler_process,  visualizer_process]

    for p in processes: p.start()
    for p in processes: print("Started {} on PID {}".format(p.name, p.pid))
    for p in processes: p.join()

    
 
# updating data values
#line1.set_ydata(matrix)

# drawing updated values
#figure.canvas.draw()

# This will run the GUI event
# loop until all UI events
# currently waiting have been processed
#figure.canvas.flush_events()
#time.sleep((1))
    






