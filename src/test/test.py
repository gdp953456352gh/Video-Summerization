import numpy 

data=[1,2,2,3,4,4,5]
mylist = []
for item in data:
    mylist.append(item)
mat = numpy.array(mylist)
numpy.savetxt("result.txt", mat);  
a = numpy.loadtxt('result.txt')  
print a[1]