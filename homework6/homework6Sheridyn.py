import numpy as np 
import matplotlib.pyplot as plt
import numericalDiffPackageSheridyn as numDiff

x = np.arange(0, 110, 0.01)
y = np.array([2 * i**2 for i in x])
noise = np.random.randn(len(x)) * 1.5
noisy = y + noise



xToPlot = x[:-2]
yToPlot = [numDiff.derivativeNoisy(x, noisy, i, 1) for i in xToPlot]

for j in range(1, 21, 2):
    xToPlotnew = x[:-j]
    yToPlotnew = [numDiff.derivativeNoisy(x, noisy, i, j) for i in xToPlotnew]
    plt.plot(xToPlotnew, yToPlotnew)

plt.title("Plot 1")
plt.show()




x2 = np.arange(0, 110, 0.01)
y2 = np.array([25 * i for i in x2])
noise2 = np.random.randn(len(x2)) * 1.5
noisy2 = y2 + noise2



xToPlot2 = x2[:-2]
yToPlot2 = [numDiff.derivativeNoisy(x2, noisy2, i, 1) for i in xToPlot2]

for j in range(1, 21, 2):
    xToPlotnew2 = x2[:-j]
    yToPlotnew2 = [numDiff.derivativeNoisy(x2, noisy2, i, j) for i in xToPlotnew2]
    plt.plot(xToPlotnew2, yToPlotnew2)
plt.title("Plot 2")
plt.show()





x3 = np.arange(0, 10, 0.01)
y3 = np.sin(2 * np.pi * x3)
noise3 = np.random.randn(len(x3)) * 0.2
noisy3 = y3 + noise3

xToPlot3 = x3[:-2]
yToPlot3 = [numDiff.derivativeNoisy(x3, noisy3, i, 1) for i in xToPlot3]

for j in range(1, 11, 2):
    xToPlotnew3 = x3[:-j]
    yToPlotnew3 = [numDiff.derivativeNoisy(x3, noisy3, i, j) for i in xToPlotnew3]
    plt.plot(xToPlotnew3, yToPlotnew3)

plt.title("Plot 3")
plt.show()