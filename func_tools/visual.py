# -*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from Config.ConstantList import *
from func_tools.Projector import projection_with_FOV

def visual_two_signal(Concentration,ori_signal,ori_signal_with_noise,u_ifft,drive_field,d_drive_field,FOV):
    ImgTan0_normal, ImgTan0_normal_uifft,normal_u, normal_u_uifft, pointx, dXffp_Amp = projection_with_FOV(ori_signal,u_ifft,FOV,drive_field,d_drive_field,gradient_strength)
    
    plt.figure(figsize=(25,25))
    #绘制原始粒子分布  接收信号+滤除基频后的  ffp的轨迹及amp
    plt.subplot(3,2,1)
    plt.xlabel("x")
    plt.ylabel("c")
    plt.plot(Concentration, 'r')
    plt.title('concentration distribution')
    
    plt.subplot(3,2,2)
    plt.xlabel("t")
    plt.ylabel("ori_signal")
    plt.plot(t[:100],ori_signal[:100], 'r')
    plt.plot(t[:100],u_ifft[:100].real, 'g')
    plt.plot(t[:100],ori_signal_with_noise[:100], 'k')
    plt.title('ori_signal')

    plt.subplot(3,2,3)
    plt.xlabel("t")
    plt.ylabel("drive_field")   #产生激励信号的驱动场
    plt.plot(t,drive_field, 'g')
    plt.title('drive_field')

    plt.subplot(3,2,4)
    plt.xlabel("t")
    plt.ylabel("dXffp_Amp")    #归一化所除的ffp的速度
    dXffp = d_drive_field[:]/gradient_strength
    dXffp_Amp = []
    for i in range(len(dXffp)):
        dXffp_Amp.append(math.sqrt(dXffp[i]**2))
    plt.plot(t,dXffp_Amp, 'r')
    plt.title('dXffp_Amp')

    #验证是否可以恢复出原始的粒子分布图

    plt.subplot(3,2,5)
    plt.xlabel("t")
    plt.ylabel("normal_u")    #归一化所除的ffp的速度
    plt.plot(t,normal_u, 'r')
    plt.plot(t,normal_u_uifft, 'g')
    plt.plot(t,normal_u - normal_u_uifft, 'b')
    plt.title('normal_u')

    plt.subplot(3,2,6)
    plt.xlabel("pointx")
    plt.ylabel("ImgTan0_normal")    #归一化所除的ffp的速度
    plt.plot(pointx[1:],ImgTan0_normal[1:], 'r')
    plt.plot(pointx[1:],ImgTan0_normal_uifft[1:], 'g')
    plt.plot(pointx[1:],ImgTan0_normal[1:] - ImgTan0_normal_uifft[1:], 'b')
    plt.title('ImgTan0_normal')


    plt.savefig(save_Path + 'input_signal.jpg')

