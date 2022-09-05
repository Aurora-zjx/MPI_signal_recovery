# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.fftpack import fft, ifft


def Langevin(H):
    lv = np.zeros(len(H))
    dlv = np.zeros(len(H))
    for i in range(len(H)):
        if abs(H[i]) < 1e-10:
            lv[i] = 0
            dlv[i] = 1/3
        else:
            lv[i] = math.cosh(H[i]) / math.sinh(H[i]) - 1 / H[i]
            dlv[i] = 1 / (H[i]**2) - 1/ (math.sinh(H[i])**2)
    return lv, dlv


def generate_ori_signal_with_FOV(Concentration,FOV,t,drive_field,d_drive_field,gradient_strength,m,B1,k):
    H = np.zeros((len(FOV), len(t)))
    dlv = np.zeros((len(FOV), len(t)))
    lv = np.zeros((len(FOV), len(t)))
    dM = np.zeros((len(FOV), len(t)))
    gradient_field = gradient_strength * FOV
    for i in range(len(t)):
        H[:, i] = drive_field[i] - gradient_field
        lv[:, i], dlv[:, i] = Langevin(k * H[:, i])
        dM[:, i] = m * Concentration * dlv[:, i] * d_drive_field[i]

    u = B1 * np.sum(dM, axis=0) * 1e8

    return u





def delete_f0(ori_signal):
    u_all = np.tile(ori_signal, 5000)
    u_fft = fft(u_all)

    u_fft[5000] = 0
    u_fft[1000000-5000] = 0

    # u_fft[10000] = 0
    # u_fft[1000000-10000] = 0
    # u_fft[15000] = 0
    # u_fft[1000000-15000] = 0

    u_ifft = ifft(u_fft)
    return u_ifft[:200]


