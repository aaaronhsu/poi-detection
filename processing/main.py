import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

# open poi.txt file and read the content
with open("yolov5/runs/tmp/poi/poi.txt") as f:
    content = f.readlines()

# read only first 200 lines
# content = content[0:20]

content = [x.strip() for x in content]
content = [x.split(",") for x in content]
content = [[float(x) for x in y] for y in content]

data = np.array(content)
x, y = data.T

# x = cos(t)
# y = sin(t)

# x, y
# def squared_dist(t, x, y):
#     return (x - np.cos(t))**2 + (y - np.sin(t))**2

# minimum = optimize.fmin(squared_dist, 0, (2,0))
# print(minimum[0])
# print(squared_dist(minimum[0], 2, 0))

# plt.scatter(x,y)

# t_param = np.linspace(0, 2*np.pi, 1000)

# radius = 200
# x_trans = 600
# y_trans = 2000
# x_param = np.sin(t_param) * radius + x_trans
# y_param = np.cos(t_param) * radius + y_trans

# avg_loss = 0
# for i in range(x.shape[0]):
#     x_val = x[i]
#     y_val = y[i]

#     avg_loss += squared_dist(optimize.fmin(squared_dist, 0, (x_val, y_val))[0], x_val, y_val)

# avg_loss /= x.shape[0]

# print("loss", avg_loss)

# plt.plot(x, y)
# plt.plot(x_param, y_param, color='red')

# plt.xlim(0, 1000)
# plt.ylim(700, 1500)


# plt.show()
