import os
import sys
import numpy as np
from utils import get_mpd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import time

path_to_histograms = '../bayesian_microlensing/data/histograms/'
files = os.listdir(path_to_histograms)

ks_test   = []
aux_s     = []
aux_macro = []
time_all  = []

for file in files:
    aux = file[:-4]
    _, kappa, _, gamma, _, s = aux.split('_')
    kappa = float(kappa)
    gamma = float(gamma)
    s     = float(s)
    
    ## load Luke's mpds

    mu_macro = 1 / ((1 - kappa)**2 - gamma**2)

    log_mu, p_log_mu = np.load('../bayesian_microlensing/data/histograms/' + file).T
    ## normalize p
    p_log_mu = p_log_mu / np.sum(p_log_mu)
    ## normalize to mu_macro
    log_mu = log_mu  - np.log10(mu_macro)
    
    time_start = time.time()
    log10_mu, p_mu = get_mpd(kappa, gamma, s*100)
    time_end   = time.time()
    time_all.append(time_end - time_start)
    if np.sum(p_mu) == 0 or np.any(np.isnan(p_mu)):
        continue
    
    f_gerlumph = interp1d(log10_mu, np.cumsum(p_mu), bounds_error=False, fill_value='extrapolate')
    f_luke     = interp1d(log_mu, np.cumsum(p_log_mu), bounds_error=False, fill_value='extrapolate')
    value = np.max(np.abs(f_luke(log_mu) - f_gerlumph(log_mu)))
    ks_test.append(value)
    aux_s.append(s)
    aux_macro.append(mu_macro)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle(file)
    
    ax1.plot(log_mu, p_log_mu, label='Luke')
    ax1.plot(log10_mu, p_mu, label='GERLUMPH interpolated')
    
    text = 'ks test = ' + str(value)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax1.text(0.05, 0.95, text, transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)

    ax1.legend()
    
    ax2.plot(log_mu, f_luke(log_mu), '-x', label='Luke')
    ax2.plot(log_mu, f_gerlumph(log_mu), '.', label='GERLUMPH')
    ax2.legend()
    
    plt.savefig('figures/' + aux + '.png')
    plt.close()

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.suptitle('KS-test values')

ax.hist(ks_test, bins=np.linspace(0, 1, 50))
ax.set_xlabel('KS-test')
ax.set_ylabel('Counts')
plt.savefig('figures/ks_test.png')
plt.close()

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.suptitle('KS-test values (mu_macro vs s)')

sc = ax.scatter(aux_macro, aux_s, c=ks_test, vmin=0, vmax=1)
cb = fig.colorbar(sc)
ax.set_xscale('log')
ax.set_xlabel('mu_macro')
ax.set_ylabel('smooth matter fraction (s)')
cb.set_label('KS-test')
plt.savefig('figures/ks_test_macro_s.png')
plt.close()

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
fig.suptitle('Computation time')
ax.hist(time_all, bins=np.linspace(0, 0.0005, 50))
ax.set_xlabel('time [s]')
ax.set_ylabel('Counts')
plt.savefig('figures/time.png')
plt.close()