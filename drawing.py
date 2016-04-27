import numpy as np
import matplotlib.pyplot as plt

y = np.array([1.0, 1.0, 0.9971584699453552, 0.9797814207650273, 0.9585792349726776, 0.9161748633879782, 0.8499453551912568, 0.7071038251366121, 0.12327868852459016, 0.0, 0.0])
x = np.array([1.0, 0.9801648274898729, 0.4569423103785445, 0.09935046794245006, 0.03935605531498813, 0.016028774968571028, 0.00687945243749127, 0.002688923033943288, 6.98421567257997e-05, 0.0, 0.0])
z = np.cos(x**2)

plt.figure(figsize=(8,4))
plt.plot(x,y,label="$sin(x)$",color="red",linewidth=1)
plt.plot(x,z,"b--",label="$cos(x^2)$")
plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
plt.ylim(-1.2,1.2)
plt.legend()
plt.show()
