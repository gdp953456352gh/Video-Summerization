import numpy 
import matplotlib.pyplot as plt


a = numpy.loadtxt('optical.txt')  


plt.subplot(211)
plt.plot(a)
plt.ylabel('Motion Vector')
plt.title('Motion saliency of World cup 2014')
plt.show()