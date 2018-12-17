import numpy as np
import matplotlib.pyplot as plt

def qsample():
    return np.random.rand() * 4.


def p(x):
    return 0.3 * np.exp(-(x - 0.3) ** 2) + 0.7 * np.exp(-(x - 2.) ** 2 / 0.3)


def q(x):
    return 0.5


def importance(nsamples):
    samples = np.zeros(nsamples, dtype=float)
    w = np.zeros(nsamples, dtype=float)

    for i in range(nsamples):
        samples[i] = qsample()
        w[i] = p(samples[i]) / q(samples[i])

    return samples, w


def sample_discrete(vec):
    u = np.random.rand()
    start = 0
    for i, num in enumerate(vec):
        if u > start:
            start += num
        else:
            return i - 1
    return i


def importance_sampling(nsamples):
    samples, w = importance(nsamples)
    #     print samples
    final_samples = np.zeros(nsamples, dtype=float)
    w = w / w.sum()
    #     print w
    for j in range(nsamples):
        final_samples[j] = samples[sample_discrete(w)]
    return final_samples


x = np.arange(0, 4, 0.01)
x2 = np.arange(-0.5, 4.5, 0.1)
realdata = 0.3 * np.exp(-(x - 0.3) ** 2) + 0.7 * np.exp(-(x - 2.) ** 2 / 0.3)
box = np.ones(len(x2)) * 0.8
box[:5] = 0
box[-5:] = 0
plt.plot(x, realdata, 'g', lw=6)
plt.plot(x2, box, 'r--', lw=6)

# samples,w = importance(5000)
final_samples = importance_sampling(5000)
plt.hist(final_samples, normed=1, fc='c')
plt.show()