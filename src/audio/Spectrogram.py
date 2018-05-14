import wave
import numpy as np
import matplotlib.pyplot as plt

fw = wave.open('123.wav','r')
soundInfo = fw.readframes(-1)
soundInfo = np.fromstring(soundInfo,np.int16)
f = fw.getframerate()
fw.close()

plt.subplot(211)
plt.plot(soundInfo)
plt.ylabel('Amplitude')
plt.title('Wave from and spectrogram of 123.wav')

plt.subplot(212)
plt.specgram(soundInfo,Fs = f, scale_by_freq = True, sides = 'default')
plt.ylabel('Frequency')
plt.xlabel('time(seconds)')
plt.show()