import wave
import pylab as pl
import numpy as np
import math
# method 1: absSum
def calVolume(waveData, frameSize, overLap):
    wlen = len(waveData)
    step = frameSize - overLap
    frameNum = int(math.ceil(wlen*1.0/step))
    volume = np.zeros((frameNum,1))
    for i in range(frameNum):
        curFrame = waveData[np.arange(i*step,min(i*step+frameSize,wlen))]
        curFrame = curFrame - np.median(curFrame) # zero-justified
        volume[i] = np.sum(np.abs(curFrame))
    return volume

# method 2: 10 times log10 of square sum
def calVolumeDB(waveData, frameSize, overLap):
    wlen = len(waveData)
    step = frameSize - overLap
    frameNum = int(math.ceil(wlen*1.0/step))
    volume = np.zeros((frameNum,1))
    for i in range(frameNum):
        curFrame = waveData[np.arange(i*step,min(i*step+frameSize,wlen))]
        curFrame = curFrame - np.mean(curFrame) # zero-justified
        volume[i] = 10*np.log10(np.sum(curFrame*curFrame))
    return volume
# ============ test the algorithm =============
# read wave file and get parameters.
sum=0
avg=0
c=[]
fw = wave.open('123.wav','r')
params = fw.getparams()
print(params)
nchannels, sampwidth, framerate, nframes = params[:4]
strData = fw.readframes(nframes)
waveData = np.fromstring(strData, dtype=np.int16)
waveData = waveData*1.0/max(abs(waveData))  # normalization
fw.close()

# calculate volume
frameSize = 256
overLap = 128
volume11 = calVolume(waveData,frameSize,overLap)
volume12 = calVolumeDB(waveData,frameSize,overLap)
print volume11[1]
print volume12[10000:10100]

'''for i in range(0, len(volume12)-2069, 2069):
    for j in range(0,2069):
        sum=sum+volume12[i+j]
    avg=sum/2069
    c.append(avg)
    sum=0
    avg=0    
mat = np.array(c)
np.savetxt("resultreplay.txt", mat);  '''
# plot the wave
'''time = np.arange(0, nframes)*(1.0/framerate)
time2 = np.arange(0, len(volume11))*(frameSize-overLap)*1.0/framerate
#pl.subplot(311)
#time1=np.array(time)
#waveData1=np.array(waveData)
pl.subplot(312)
pl.plot(time2, volume11)
pl.ylabel("absSum")
pl.subplot(313)
pl.plot(time2, volume12, c="g")
pl.ylabel("Decibel(dB)")
pl.xlabel("time (seconds)")
pl.show()'''