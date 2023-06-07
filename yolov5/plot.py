import matplotlib.pyplot as plt
import numpy as np

# open poi.txt file and read the content
with open("./runs/tmp/poi/poi.txt", "r") as f:
    content = f.readlines()

content = [x.strip() for x in content]
content = [x.split(",") for x in content]
content = [[float(x) for x in y] for y in content]

data = np.array(content)
x, y = data.T


def calculate_r_squared(x_values, y_values, parametric_equation):
    # Calculate the predicted y values using the parametric equation
    y_predicted = parametric_equation(x_values)

    # Calculate the mean of the observed y values
    y_mean = np.mean(y_values)


minimum = optimize.fmin(squared_dist, 0, (2, 0))
print(minimum[0])
print(squared_dist(minimum[0], 2, 0))

plt.scatter(x, y)

t_param = np.linspace(0, 2 * np.pi, 1000)

radius = 200
x_trans = 600
y_trans = 2000
x_param = np.sin(t_param) * radius + x_trans
y_param = np.cos(t_param) * radius + y_trans

avg_loss = 0
for i in range(x.shape[0]):
    x_val = x[i]
    y_val = y[i]

    avg_loss += squared_dist(
        optimize.fmin(squared_dist, 0, (x_val, y_val))[0], x_val, y_val
    )

avg_loss /= x.shape[0]

print("loss", avg_loss)

plt.plot(x, y)
plt.plot(x_param, y_param, color="red")

plt.xlim(0, 1000)
plt.ylim(700, 1500)


plt.show()


def idk_what_function_this_is(y_values, y_predicted, y_mean):
    # Calculate the total sum of squares (SST)
    sst = np.sum((y_values - y_mean) ** 2)

    # Calculate the sum of squares of residuals (SSE)
    sse = np.sum((y_values - y_predicted) ** 2)

    # Calculate the coefficient of determination (R^2)
    r_squared = 1 - (sse / sst)

    return r_squared


def parametric_equation(x):
    t = np.arccos(x)
    return np.sin(t)


x = x / np.max(np.abs(x))

# Calculate the R^2 value
r_squared = calculate_r_squared(x, y, parametric_equation)

# Print the result
print("R^2 value:", r_squared)
# plt.scatter(x,y)
# plt.show()
