import numpy 
import matplotlib.pyplot as plt


a = numpy.loadtxt('valresulthighlight.txt')  


plt.subplot(211)
plt.plot(a)
plt.ylabel('Score')
plt.title('The Rugby Championship South Africa v New Zealand 7th October 2017')
plt.show()