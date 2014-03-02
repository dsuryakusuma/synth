import pyaudio
from math import sin, pi as PI
from array import array
import struct
import time
from node import *

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
SAMPLING_RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(frames_per_buffer=CHUNK_SIZE,
                format=FORMAT,
                channels=CHANNELS,
                rate=SAMPLING_RATE,
                output=True)

freq1 = ConstantSource(880)
freq2 = ConstantSource(1)

sine = SineSource()
sine.frequency.bind_stream(freq1.output)

square = SquareSource()
square.frequency.bind_stream(freq2.output)
scale = MultiplierNode()
half = ConstantSource(0.5)
scale.input1.bind_stream(half.output)
scale.input2.bind_stream(square.output)
bias = AdderNode()
bias.input1.bind_stream(half.output)
bias.input2.bind_stream(scale.output)

mul = MultiplierNode()
mul.input1.bind_stream(sine.output)
mul.input2.bind_stream(bias.output)

samples = [0] * SAMPLING_RATE * 5
for i in range(len(samples)):
    value = mul.output.sample(i / SAMPLING_RATE)
    samples[i] = round(value * 64)

sample_buffer = struct.pack('b' * len(samples), *samples)

start = time.time()
stream.write(sample_buffer)
stop = time.time()
print(stop - start)
