import sys
from utils import get_mpd
import matplotlib.pyplot as plt

kappa = float(sys.argv[1])
gamma = float(sys.argv[2])
s     = float(sys.argv[3])

log10_mu, p_mu = get_mpd(kappa, gamma, s*100)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

ax.plot(log10_mu, p_mu, label='GERLUMPH interpolated')

ax.legend()

plt.show()