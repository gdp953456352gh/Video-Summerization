import matplotlib.pyplot as plt

data = [5, 20, 15, 25, 10]
a= len(data)
data.append(4)
a=data[0:3]
plt.bar(range(len(a)), a)
plt.show()

