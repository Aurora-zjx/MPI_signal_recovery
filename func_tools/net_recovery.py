# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import torch
import torch
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from Config.ConstantList import *
from func_tools.Scanner import generate_ori_signal_with_FOV, delete_f0
from func_tools.Noise import gaussian_noise


def get_net_input(Concentration,FOV,SNR,drive_field,d_drive_field):
    ## 1.在FOV内生成原始信号
    ori_signal = generate_ori_signal_with_FOV(Concentration,FOV,t,drive_field,d_drive_field,gradient_strength,m,B1,miu0 * m / (k_B * T))
    ## 2.给生成信号添加高斯噪声
    ori_signal_with_noise = gaussian_noise(ori_signal, SNR)
    ## 3.丢失基频信息
    u_ifft = delete_f0(ori_signal_with_noise)

    # visual_two_signal(Concentration,ori_signal,ori_signal_with_noise,u_ifft,drive_field,d_drive_field)

    return ori_signal,ori_signal_with_noise,u_ifft

def net_recovery(input_signal):
    input_signal = input_signal.real
    device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')
    model_path = '/home/zjx/Documents/net/signal_unet/checkpoints/one_loss/best.pth'
    try:
        model = torch.load(model_path)
        model = model.to(device)
        input_signal = input_signal.to(device)
        input_signal = input_signal.unsqueeze(1)
        with torch.no_grad():
            test_result = model(input_signal)
        test_result = test_result.reshape(test_result.size()[1], -1)
        test_result = test_result.cpu().numpy()
        test_result = test_result.tolist()
        result = test_result[0]
    except:
        model = torch.load(model_path,map_location='cpu')
        device = torch.device('cpu')
        model = model.to(device)
        input_signal = torch.from_numpy(input_signal)
        input_signal = input_signal.unsqueeze(0)
        input_signal = input_signal.unsqueeze(1)
        with torch.no_grad():
            test_result = model(input_signal)
    
        test_result = test_result.cpu().numpy()
        test_result = test_result.tolist()
        result = test_result[0][0]

    # import pdb;pdb.set_trace()

    return result
