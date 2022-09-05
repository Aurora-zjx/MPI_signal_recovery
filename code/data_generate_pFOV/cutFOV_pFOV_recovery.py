# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))
from Config.ConstantList import *
from func_tools.Phantom import generate_set_concentration
from func_tools.Scanner import generate_ori_signal_with_FOV, delete_f0
from func_tools.Projector import sigle_projection, projection_with_FOV
from func_tools.Noise import Harmonic_interference_fixed_phase, Harmonic_interference_varied_phase, gaussian_noise
from func_tools.net_recovery import get_net_input, net_recovery
from func_tools.pFOV_recovery import pFOV_scan_ori_signal, pFOV_scan_uifft, pFOV_scan_and_recovery
from func_tools.visual import visual_two_signal

'''
采用pFOV扫描的方式恢复原有的粒子分布
（这里的pFOV大小等于FOV大小 通过裁减区间长度来代替pFOV）
'''
'''
还存在问题没有调试完
'''

if __name__ == "__main__":

    
    ## 1.产生设定的粒子分布
    Concentration_all = generate_set_concentration()
    ## 2.生成随机的驱动场
    drive_field = np.zeros(len(t))   #drive field(驱动场)
    d_drive_field = np.zeros(len(t))
    # phase = random.randint(0,360)
    phase = 0
    for k in range(len(t)):
        drive_field[k] = A * math.cos(w * t[k] + phase / 180 * np.pi)
        d_drive_field[k] = -1 * A * w * math.sin(w * t[k] + phase / 180 * np.pi) 


    ## 3.定义FOV大小及pFOV 及噪声强度
    sir_low = 15
    sir_high = 20

    ##   设置FOV大小为(-0.01,0.01) step=0.0002 共100个点
    ##   设置pFOV大小为(-0.002,0.002) step=0.0002 共20个点
    FOV = np.arange(-0.01,0.01,0.0002)
    pFOV = np.arange(-0.01,0.01,0.0002)

    ## 4.产生原始的接收信号
    ori_signal = generate_ori_signal_with_FOV(Concentration_all,FOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))

    ## 5.将产生的信号投影
    #ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(ori_signal,FOV,drive_field,d_drive_field,gradient_strength)
    ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(ori_signal,FOV,drive_field,d_drive_field,gradient_strength)

    ## 6.去基频 并投影
    u_ifft = delete_f0(ori_signal)
    #ImgTan0_normal_new, normal_u_new, pointx_new, dXffp_Amp_new = sigle_projection(u_ifft.real,FOV,drive_field,d_drive_field,gradient_strength)
    ImgTan0_normal_new, normal_u_new, pointx_new, dXffp_Amp_new = projection_with_FOV(u_ifft,FOV,drive_field,d_drive_field,gradient_strength)

##region 绘制前一部分结果
    p1 = plt.figure(figsize=(17,27))
    plt.subplot(4,2,1)  #浓度分布
    plt.xlabel("x")
    plt.ylabel("c")
    plt.plot(Concentration_all,'g')
    plt.title('concentration distribution')
    print('粒子浓度图绘制完成')

    plt.subplot(4,2,2)   
    plt.xlabel("t")
    plt.ylabel("signal")
    plt.plot(t[:100],ori_signal[:100],'r')
    plt.plot(t[:100],u_ifft[:100],'g')
    plt.title('signal_t')

    plt.subplot(4,2,3)   
    plt.xlabel("x")
    plt.ylabel("ImgTan0_normal")
    plt.plot(pointx[1:], ImgTan0_normal[1:].real,'r')
    plt.plot(pointx[1:], ImgTan0_normal_new[1:].real,'g')
    plt.plot(pointx[1:], ImgTan0_normal[1:].real - ImgTan0_normal_new[1:].real,'b')
    plt.title('ImgTan0_normal')
    print('理想粒子分布图绘制完成')
##endregion


    ## 7.未丢失基频 采用pFOV扫描
    plt.subplot(4,2,4)
    plt.xlabel("x")
    plt.ylabel("c")

    pFOV_scan_ori_signal(Concentration_all,pFOV,sir_low,sir_high,drive_field,d_drive_field)
    
    plt.xlim(-50, 145)
    plt.ylim(-0.0001, 0.0005)
    plt.title('ideal concentration distribution pFOV')
    print('pFOV未去基频图绘制完成')

    ## 8.丢失基频 采用pFOV扫描
    plt.subplot(4,2,5)
    plt.xlabel("x")
    plt.ylabel("c")

    pFOV_scan_uifft(Concentration_all,pFOV,drive_field,d_drive_field)

    plt.title('pFOV with different color')
    print('pFOV粒子分布图(去基频)绘制完成')


    ## 9.丢失基频 采用pFOV扫描并恢复
    plt.subplot(4,2,6)
    plt.xlabel("x")
    plt.ylabel("c")
    pFOV_scan_and_recovery(Concentration_all,pFOV,drive_field,d_drive_field,0,0)
    plt.ylim(-0.0001, 0.0005)
    plt.title('pFOV recovery')
    print('pFOV粒子分布图(去基频恢复结果)绘制完成')

    ## 10.丢失基频+添加噪声 采用pFOV扫描并恢复
    plt.subplot(4,2,7)
    plt.xlabel("x")
    plt.ylabel("c")
    pFOV_scan_and_recovery(Concentration_all,pFOV,drive_field,d_drive_field,sir_low, sir_high)
    plt.ylim(-0.0001, 0.0005)
    plt.title('pFOV recovery with interference or gauss_noise')
    print('pFOV粒子分布图(去基频恢复结果)(谐波干扰)/(高斯噪声)绘制完成')

    plt.savefig(save_Path + 'pFOV_recovery/' +'pFOV_recovery_cutFOV.jpg')





