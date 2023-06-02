import matplotlib.pyplot as plt
import numpy as np

# open poi.txt file and read the content
with open('./runs/tmp/poi/poi.txt', 'r') as f:
    content = f.readlines()

# read only first 200 lines
content = content[0:200]

content = [x.strip() for x in content]
content = [x.split(',') for x in content]
content = [[float(x) for x in y] for y in content]

data = np.array(content)
x,y = data.T

print(x)

plt.scatter(x,y)
plt.show()
