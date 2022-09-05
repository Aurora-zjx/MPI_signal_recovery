# -*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from Config.ConstantList import *
from func_tools.Phantom import generate_random_concentration
from func_tools.Scanner import generate_ori_signal_with_FOV, delete_f0
from func_tools.Projector import projection_with_FOV, sigle_projection
from func_tools.Noise import Harmonic_interference_fixed_phase, Harmonic_interference_varied_phase, gaussian_noise
from func_tools.net_recovery import get_net_input, net_recovery
from func_tools.pFOV_recovery import pFOV_scan
from func_tools.visual import visual_two_signal


if __name__ == "__main__":
    ## 1.生成随机的粒子分布
    Concentration = generate_random_concentration()
    ## 2.生成随机的驱动场
    drive_field = np.zeros(len(t))   #drive field(驱动场)
    d_drive_field = np.zeros(len(t))
    phase = random.randint(0,360)
    # phase = 0
    for k in range(len(t)):
        drive_field[k] = A * math.cos(w * t[k] + phase / 180 * np.pi)
        d_drive_field[k] = -1 * A * w * math.sin(w * t[k] + phase / 180 * np.pi) 

    ## 3.定义FOV大小及pFOV 及噪声强度
    FOV = np.arange(-Xmax, Xmax, step)
    SNR_low = 15
    SNR_high = 20
    SNR = random.randint(SNR_low, SNR_high)
    
    ## 4.生成net的输入信号
    ori_signal,ori_signal_with_noise,input_signal= get_net_input(Concentration,FOV,SNR,drive_field,d_drive_field)   #返回原始信号+带噪信号+带噪和去基频信号
    output_signal = net_recovery(input_signal)

    visual_two_signal(Concentration,ori_signal,ori_signal_with_noise,input_signal,drive_field,d_drive_field,FOV)

    p2 = plt.figure(figsize=(17,27))
    plt.subplot(4,2,1)
    plt.xlabel("x")
    plt.ylabel("c")
    plt.plot(Concentration, 'r')
    plt.title('concentration distribution')

    plt.subplot(4,2,2)   
    plt.xlabel("t")
    plt.ylabel("signal")
    plt.plot(t,ori_signal,'r')
    plt.plot(t,input_signal,'g')
    plt.plot(t,output_signal,'k')
    plt.title('signal_t')

    ## 5.将恢复出的信号投影到图像域进行显示
    # import pdb;pdb.set_trace()  #分别是原信号 加噪+去基频信号 网络恢复信号 的投影结果
    ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(ori_signal,FOV,drive_field,d_drive_field,gradient_strength)
    ImgTan0_normal_noise_withoutf0, normal_u_noise_withoutf0, pointx_noise_withoutf0, dXffp_Amp_noise_withoutf0 = sigle_projection(input_signal.real,FOV,drive_field,d_drive_field,gradient_strength)
    ImgTan0_normal_net_recovery, normal_u_net_recovery, pointx_net_recovery, dXffp_Amp_net_recovery = sigle_projection(output_signal,FOV,drive_field,d_drive_field,gradient_strength)

    plt.subplot(4,2,3)   
    plt.xlabel("x")
    plt.ylabel("ImgTan0_normal")
    plt.plot(pointx[1:], ImgTan0_normal[1:].real,'r')
    # plt.plot(pointx[1:], ImgTan0_normal_noise_withoutf0[1:].real,'g')
    plt.plot(pointx[1:], ImgTan0_normal_net_recovery[1:].real,'k')
    # plt.plot(pointx[1:], ImgTan0_normal[1:].real - ImgTan0_normal_new[1:].real,'b')
    plt.title('ImgTan0_normal')


    ## 6.pFOV扫描 加噪 去噪 pFOV恢复
    plt.subplot(4,2,4)
    plt.xlabel("x")
    plt.ylabel("c")

    pFOV_scan(Concentration,SNR,FOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))

    plt.xlim(0, 100)
    # plt.ylim(-0.0001, 0.0005)
    plt.title('pFOV recovery with interference or gauss_noise')
    print('pFOV粒子分布图(去基频恢复结果)(谐波干扰)/(高斯噪声)绘制完成')

    plt.savefig(save_Path + 'pFOV_recovery.jpg')


    



