import numpy as np
from scipy.ndimage import map_coordinates

kappa_list = np.loadtxt('kappa_list.txt', dtype=float)
gamma_list = np.loadtxt('gamma_list.txt', dtype=float)
s_list     = np.loadtxt('s_list.txt', dtype=float)
log10_mu   = np.loadtxt('log10_mu.txt', dtype=float)

#data = np.load('data/mpd_grid.npy')
data = np.load('data/mpd_grid_inpaint.npy')

Nbins = 400
log10_mu_index = np.arange(Nbins)

def macromodel_to_index(kappa, gamma, s):
    kappa_index = (kappa - kappa_list[0]) / 0.01
    gamma_index = (gamma - gamma_list[0]) / 0.01
    s_index     = (s - s_list[0])
    
    return kappa_index, gamma_index, s_index

def get_coordinates(kappa_index, gamma_index, s_index):
    kappa_index = kappa_index * np.ones_like(log10_mu_index)
    gamma_index = gamma_index * np.ones_like(log10_mu_index)
    s_index     = s_index     * np.ones_like(log10_mu_index)
    
    return np.asarray([log10_mu_index, kappa_index, gamma_index, s_index])

def get_mpd(kappa, gamma, s):
    kappa_index, gamma_index, s_index = macromodel_to_index(kappa, gamma, s)
    coords = get_coordinates(kappa_index, gamma_index, s_index)
    p_mu = map_coordinates(data, coords, order=0)
    
    return log10_mu, p_mu