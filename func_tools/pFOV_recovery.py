# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from Config.ConstantList import *
from func_tools.Scanner import generate_ori_signal_with_FOV, delete_f0
from func_tools.Projector import projection_with_FOV, sigle_projection
from func_tools.Noise import gaussian_noise



def pFOV_scan(Concentration,SNR,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,k):

    left = -100
    last_color = random.choice(color_list)
    winner = last_color

    ##初始化 lastline
    right = left + 100
    Concentration_list = Concentration.tolist()
    pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
    pConcentration = np.array(pConcentration)
    ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,k)
    # ori_signal,t,fs,drive_field = generate_ori_signal_with_FOV(pConcentration,pFOV)
    u_ifft = delete_f0(ori_signal)
    ImgTan0_normal, ImgTan0_normal_uifft,normal_u, normal_u_uifft, pointx, dXffp_Amp = projection_with_FOV(ori_signal,u_ifft,pFOV,drive_field,d_drive_field,gradient_strength)
    #ImgTan0, ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(u_ifft,pFOV)
    img_x = range(left,right)

    last_line = ImgTan0_normal_uifft[20:40]
    plt.plot(img_x[20:40],last_line,winner)
    left = left + 5
    ######
    while(left <= 100):
        right = left + 100
        
        if left < 0:
            Concentration_list = Concentration.tolist()
            pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
        elif right > 100:
            Concentration_list = Concentration.tolist()
            pConcentration = Concentration_list[right-100:] + [0] * (right - 100)
        else:
            Concentration_list = Concentration.tolist()
            pConcentration = Concentration_list[left:right]

        pConcentration = np.array(pConcentration)
        ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,k)
        signal_with_noise = gaussian_noise(ori_signal, SNR)             #添加谐波干扰 再去基频
        u_ifft = delete_f0(signal_with_noise)
        ## 将u_ifft去噪 再输入到如下函数中

        ImgTan0_normal, ImgTan0_normal_uifft,normal_u, normal_u_uifft, pointx, dXffp_Amp = projection_with_FOV(ori_signal,u_ifft,pFOV,drive_field,d_drive_field,gradient_strength)
        img_x = range(left,right)

        while winner == last_color:
            winner = random.choice(color_list)

        ## 计算向上平移量
        current_line = ImgTan0_normal_uifft[20:40]
        # import pdb;pdb.set_trace()
        up_shift = np.subtract(last_line[5:20],current_line[:15])
        up_shift_c = sum(up_shift) / len(up_shift)
        # print(up_shift_c)
        plt.plot(img_x[20:40],current_line + up_shift_c,winner)

        last_line = current_line + up_shift_c

        last_color = winner
        left = left + 5


#pFOV 扫描原始信号
def pFOV_scan_ori_signal(Concentration_all,pFOV,sir_low,sir_high,drive_field,d_drive_field):
    left = -100
    right = left + 100
    Concentration_list = Concentration_all.tolist()
    pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
    pConcentration = np.array(pConcentration)
    ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))
    ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(ori_signal,pFOV,drive_field,d_drive_field,gradient_strength)
    #ori_signal,t,fs,drive_field = generate_ori_signal_with_FOV(pConcentration,pFOV)
    #ImgTan0, ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(ori_signal,pFOV)
    last_interval = ImgTan0_normal.tolist()
    left = left + 5

    while(left <= 100):
        sir = random.randint(sir_low, sir_high)
        right = left + 100
        
        if left < 0:
            Concentration_list = Concentration_all.tolist()
            pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
        elif right > 100:
            Concentration_list = Concentration_all.tolist()
            pConcentration = Concentration_list[right-100:] + [0] * (right - 100)
        else:
            Concentration_list = Concentration_all.tolist()
            pConcentration = Concentration_list[left:right]

        pConcentration = np.array(pConcentration)
        ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))
        ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(ori_signal,pFOV,drive_field,d_drive_field,gradient_strength)
        #ori_signal,t,fs,drive_field = generate_ori_signal_with_FOV(pConcentration,pFOV)
        # ori_signal = gaussian_noise(ori_signal, sir)
        #ImgTan0, ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(ori_signal,pFOV)
        img_x = range(left,right)


        plt.plot(img_x[20:40],ImgTan0_normal[20:40].real,'r')
        # print(img_x[20:40])
        left = left + 5

#pFOV 扫描去基频信号
def pFOV_scan_uifft(Concentration_all,pFOV,drive_field,d_drive_field):
    left = -100
    last_color = random.choice(color_list)
    winner = last_color
    while(left <= 100):
        right = left + 100
        
        if left < 0:
            Concentration_list = Concentration_all.tolist()
            pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
        elif right > 100:
            Concentration_list = Concentration_all.tolist()
            pConcentration = Concentration_list[right-100:] + [0] * (right - 100)
        else:
            Concentration_list = Concentration_all.tolist()
            pConcentration = Concentration_list[left:right]

        pConcentration = np.array(pConcentration)
        #ori_signal,t,fs,drive_field = generate_ori_signal_with_FOV(pConcentration,pFOV)
        #u_ifft = delete_f0(ori_signal)
        #ImgTan0, ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(u_ifft,pFOV)
        
        ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))
        u_ifft = delete_f0(ori_signal)
        ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(u_ifft.real,pFOV,drive_field,d_drive_field,gradient_strength)
        img_x = range(left,right)

        while winner == last_color:
            winner = random.choice(color_list)
        plt.plot(img_x[20:40],ImgTan0_normal[20:40].real,winner)

        last_color = winner
        left = left + 5

#pFOV 扫描去基频信号并恢复
def pFOV_scan_and_recovery(Concentration_all,pFOV,drive_field,d_drive_field,sir_low,sir_high):
    left = -100
    last_color = random.choice(color_list)
    winner = last_color

    ##初始化 lastline
    right = left + 100
    Concentration_list = Concentration_all.tolist()
    pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
    pConcentration = np.array(pConcentration)
    #ori_signal,t,fs,drive_field = generate_ori_signal_with_FOV(pConcentration,pFOV)
    #u_ifft = delete_f0(ori_signal)
    #ImgTan0, ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(u_ifft,pFOV)
    ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))
    u_ifft = delete_f0(ori_signal)
    ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(u_ifft.real,pFOV,drive_field,d_drive_field,gradient_strength)
    img_x = range(left,right)

    last_line = ImgTan0_normal[20:40]
    plt.plot(img_x[20:40],last_line,winner)
    left = left + 5
    ######
    while(left <= 100):
        right = left + 100
        if sir_low == 0 and sir_high == 0:
            sir = 0
        else:
            sir = random.randint(sir_low, sir_high)

        if left < 0:
            Concentration_list = Concentration_all.tolist()
            pConcentration = [0] * abs(left) + Concentration_list[:100-abs(left)]
        elif right > 100:
            Concentration_list = Concentration_all.tolist()
            pConcentration = Concentration_list[right-100:] + [0] * (right - 100)
        else:
            Concentration_list = Concentration_all.tolist()
            pConcentration = Concentration_list[left:right]

        pConcentration = np.array(pConcentration)
        ori_signal = generate_ori_signal_with_FOV(pConcentration,pFOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))
        if sir != 0:
            ori_signal = gaussian_noise(ori_signal, sir)             #添加谐波干扰 再去基频
        u_ifft = delete_f0(ori_signal)
        ImgTan0_normal, normal_u, pointx, dXffp_Amp = sigle_projection(u_ifft.real,pFOV,drive_field,d_drive_field,gradient_strength)
        #ori_signal,t,fs,drive_field = generate_ori_signal_with_FOV(pConcentration,pFOV)
        #u_ifft = delete_f0(ori_signal)
        #ImgTan0, ImgTan0_normal, normal_u, pointx, dXffp_Amp = projection_with_FOV(u_ifft,pFOV)
        img_x = range(left,right)

        while winner == last_color:
            winner = random.choice(color_list)

        ## 计算向上平移量
        current_line = ImgTan0_normal[20:40]
        # import pdb;pdb.set_trace()
        up_shift = np.subtract(last_line[5:20],current_line[:15])
        # print(up_shift)
        up_shift_c = sum(up_shift) / len(up_shift)
        # print(up_shift_c)
        plt.plot(img_x[20:40],current_line + up_shift_c,winner)

        last_line = current_line + up_shift_c

        last_color = winner
        left = left + 5

