import numpy as np
from transforms import decay
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"]=(8, 8)
plt.rcParams['figure.dpi'] = 80

BETA_INIT = 1
T_MIN = 0
T_MAX = 100

# Plot a single decay trajectory
rho = 0.9
beta = BETA_INIT

Xs = list(range(T_MIN, T_MAX))
Ys = []

for t in range(T_MIN, T_MAX):
    beta = decay(rho, BETA_INIT, t / (T_MAX - 1))
    Ys.append(beta)

plt.plot(Xs, Ys)
plt.title('Rho = {}'.format(rho))
plt.show()

# Plot mutltiple trajectory shapesd (values for rho)
N = 20
RHOs = np.linspace(0, 1, N)

Xs = np.array((range(T_MIN, T_MAX))) / T_MAX
Ys = []
plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.turbo(np.linspace(0, 1, len(RHOs)))))

# Generate values
for RHO in RHOs:

    Y = []
    beta = BETA_INIT

    for t in range(T_MIN, T_MAX):
        beta = decay(RHO, BETA_INIT, t / (T_MAX - 1))
        Y.append(beta)

    Ys.append(Y)

# Plot
for i, Y in enumerate(Ys):
    plt.plot(Xs, Y, label='rho = {}'.format(round(RHOs[i], 2)))

plt.legend(loc='center right')
plt.ylabel('Parameter value')
plt.xlabel('Progress (t/T)')
plt.title('Decay algorithm Rosokha & Younge (2019) for initial value of {} and rho in [0,1]'.format(BETA_INIT))
plt.show()