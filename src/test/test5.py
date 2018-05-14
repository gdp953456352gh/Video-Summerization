import numpy 
import matplotlib.pyplot as plt


a = numpy.loadtxt('audio1.txt')  


plt.subplot(211)
plt.plot(a)
plt.ylabel('energy')
plt.title('Audio short-time energy of World cup 2014')
plt.show()