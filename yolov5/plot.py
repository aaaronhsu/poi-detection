import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

# open poi.txt file and read the content
with open('./runs/tmp/poi/poi.txt', 'r') as f:
    content = f.readlines()

# read only first 200 lines
# content = content[0:20]

content = [x.strip() for x in content]
content = [x.split(',') for x in content]
content = [[float(x) for x in y] for y in content]

data = np.array(content)
x,y = data.T

# x = cos(t) 
# y = sin(t)

# x, y
def squared_dist(t, x, y):
    return (x - np.cos(t))**2 + (y - np.sin(t))**2

minimum = optimize.fmin(squared_dist, 0, (2,3))
print(minimum[0])

# plt.scatter(x,y)
# plt.show()
