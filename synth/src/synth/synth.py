import pyaudio
from math import sin, pi as PI
from array import array
import struct
import time

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLING_RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(frames_per_buffer=CHUNK_SIZE,
                format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLING_RATE,
                output=True)

samples = [0] * SAMPLING_RATE
for i in range(len(samples)):
    samples[i] = round(sin(i / SAMPLING_RATE * PI * 2 * 880) * 64)

sample_buffer = struct.pack('h' * len(samples), *samples)

start = time.time()
stream.write(sample_buffer)
stop = time.time()
print(stop - start)
