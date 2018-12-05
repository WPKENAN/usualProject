from scipy.stats import norm
import matplotlib.pyplot as plt
import random
import math

def gibbs(N=500, thin=10):
    pi = [];
    x = 0
    y = 0
    for i in range(N):
        for j in range(thin):
            x = norm.rvs(loc=y, scale=2, size=1, random_state=None)
            y = norm.rvs(loc=x, scale=3, size=1, random_state=None)
            pi.append(x[0]);

    print(pi)
    return pi;
pi=gibbs()

plt.hist(pi, 100, normed=1, facecolor='red', alpha=0.7,label='Samples Distribution')
plt.show();

# import random, math
#
#
# def gibbs(N=50000, thin=1000):
#     x = 0
#     y = 0
#     print
#     "Iter  x  y"
#     for i in range(N):
#         for j in range(thin):
#             x = random.gammavariate(3, 1.0 / (y * y + 4))
#             y = random.gauss(1.0 / (x + 1), 1.0 / math.sqrt(2 * x + 2))
#         print
#         i, x, y
#
#
# gibbs()