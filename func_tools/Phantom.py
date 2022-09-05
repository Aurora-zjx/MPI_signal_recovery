# -*- coding: utf-8 -*-

import numpy as np
import random
import math
from scipy.interpolate import griddata
from scipy.fftpack import fft, ifft


def generate_random_concentration():
    Concentration = np.zeros(100) # 粒子分布浓度  初始化
    Concentration_num = random.randint(1,6)
    ori_serial = range(0,100)
    already_have_list = []
    Concentration_i = 0
    while(1):  
        C_center = random.choice(ori_serial)
        if C_center not in already_have_list:
            left = max(0,C_center - random.randint(0,8))
            right = min(100,C_center + random.randint(0,8))
            Concentration[left:right] = random.randint(1,2)
            new_list = range(left,right)
            already_have_list.extend(new_list)
            Concentration_i = Concentration_i + 1
        if Concentration_i == Concentration_num:
            break
    return Concentration


def generate_set_concentration():
    Concentration_all = np.zeros(100) # 粒子分布浓度  初始化
    Concentration_all[0:5] = 0  #5
    Concentration_all[5:6] = 1  #1
    Concentration_all[6:10] = 0  #4
    Concentration_all[10:11] = 1  #1
    Concentration_all[11:19] = 0  #8
    Concentration_all[19:20] = 1   #1
    Concentration_all[20:32] = 0   #12
    Concentration_all[32:33] = 1   #1
    Concentration_all[33:49] = 0   #16
    Concentration_all[49:50] = 1   #1
    Concentration_all[50:70] = 0   #20
    Concentration_all[70:71] = 1   #1
    Concentration_all[71:95] = 0   #24
    Concentration_all[95:96] = 1   #1
    Concentration_all[96:100] = 0   #4

    return Concentration_all
