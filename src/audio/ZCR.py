import math
import wave
import numpy as np
import pylab as pl

def ZeroCR(waveData,frameSize,overLap):
    wlen = len(waveData)
    step = frameSize - overLap
    frameNum = math.ceil(wlen/step)
    frameNum1=int(frameNum)
    zcr = np.zeros((frameNum1,1))
    for i in range(frameNum1):
        curFrame = waveData[np.arange(i*step,min(i*step+frameSize,wlen))]
        #To avoid DC bias, usually we need to perform mean subtraction on each frame
        #ref: http://neural.cs.nthu.edu.tw/jang/books/audiosignalprocessing/basicFeatureZeroCrossingRate.asp
        curFrame = curFrame - np.mean(curFrame) # zero-justified
        zcr[i] = sum(curFrame[0:-1]*curFrame[1::]<=0)
    return zcr

# ============ test the algorithm =============
# read wave file and get parameters.
fw = wave.open('123.wav','rb')
params = fw.getparams()
print(params)
nchannels, sampwidth, framerate, nframes = params[:4]
print(params)
str_data = fw.readframes(nframes)
wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, 1
#wave_data = wave_data.T
fw.close()

# calculate Zero Cross Rate
frameSize = 256
overLap = 0
zcr = ZeroCR(wave_data,frameSize,overLap)

# plot the wave
time = np.arange(0, len(wave_data)) * (1.0 / framerate)
time2 = np.arange(0, len(zcr)) * (len(wave_data)/len(zcr) / framerate)
pl.subplot(211)
pl.plot(time, wave_data)
pl.ylabel("Amplitude")
pl.subplot(212)
pl.plot(time2, zcr)
pl.ylabel("ZCR")
pl.xlabel("time (seconds)")
pl.show()