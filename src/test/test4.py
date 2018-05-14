import numpy 

a = numpy.loadtxt('replay7mins.txt')  
b=numpy.ndarray.tolist(a)
c=[]
sum=0
avg=0
for i in range(0, len(b)-90, 90):
    for j in range(0,90):
        sum=sum+b[i+j]
    avg=sum/90
    c.append(avg)
    sum=0
    avg=0    
mat = numpy.array(c)
numpy.savetxt("resultreplay.txt", mat);  
print c[0:10]