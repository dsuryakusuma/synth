import pyaudio

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(frames_per_buffer=CHUNK_SIZE,
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE)

buffer = [0] * CHUNK_SIZE
for i in range(buffer):
    buffer[i] = 
stream.write(, num_frames, exception_on_underflow)
