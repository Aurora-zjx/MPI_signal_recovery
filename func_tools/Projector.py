# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.fftpack import fft, ifft


def projection_with_FOV(u,u_ifft,FOV,drive_field,d_drive_field,gradient_strength):
    u = u.real
    u_ifft = u_ifft.real
    Xffp = drive_field[:]/gradient_strength  
    dXffp = d_drive_field[:]/gradient_strength
    dXffp_Amp = []
    for i in range(len(dXffp)):
        dXffp_Amp.append(math.sqrt(dXffp[i]**2))
    normal_u = np.divide(u,dXffp_Amp) 
    normal_u_uifft = np.divide(u_ifft,dXffp_Amp)      
    Xffp = np.array(Xffp)


    # 因为相位的不同 不能直接拿0:100信号去投影
    # 循环移位调整信号 
    normal_u = normal_u.tolist()
    normal_u_uifft = normal_u_uifft.tolist()
    Xffp = Xffp.tolist()
    if normal_u[-1] < 0 and normal_u[0] < 0:  #循环左移
        while(normal_u[len(normal_u)-1] < 0):
            shift_u = normal_u[1:] + normal_u[:1]
            normal_u = shift_u

            shift_uifft = normal_u_uifft[1:] + normal_u_uifft[:1]
            normal_u_uifft = shift_uifft

            shift_Xffp = Xffp[1:] + Xffp[:1]
            Xffp = shift_Xffp
    else:                    #循环右移
        while(normal_u[len(normal_u)-1]>0):
            shift_u = normal_u[len(normal_u)-1:] + normal_u[:len(normal_u)-1]
            normal_u = shift_u

            shift_uifft = normal_u_uifft[len(normal_u_uifft)-1:] + normal_u_uifft[:len(normal_u_uifft)-1]
            normal_u_uifft = shift_uifft

            shift_Xffp = Xffp[len(Xffp)-1:] + Xffp[:len(Xffp)-1]
            Xffp = shift_Xffp
        
    normal_u = np.array(normal_u)  
    normal_u_uifft = np.array(normal_u_uifft)  
    Xffp = np.array(Xffp)


    pointx = FOV
    # ImgTan0 = griddata(Xffp[0:100], u[0:100], pointx, method='nearest')
    ImgTan0_normal = griddata(Xffp[0:100], normal_u[0:100], pointx, method='nearest')
    ImgTan0_normal_uifft = griddata(Xffp[0:100], normal_u_uifft[0:100], pointx, method='nearest')

    return ImgTan0_normal, ImgTan0_normal_uifft,normal_u, normal_u_uifft, pointx, dXffp_Amp

#取正的一部分去投影
def sigle_projection(u,FOV,drive_field,d_drive_field,gradient_strength):
    # u = u.real
    Xffp = drive_field[:]/gradient_strength  
    dXffp = d_drive_field[:]/gradient_strength
    dXffp_Amp = []
    for i in range(len(dXffp)):
        dXffp_Amp.append(math.sqrt(dXffp[i]**2))
    normal_u = np.divide(u,dXffp_Amp) 
    Xffp = np.array(Xffp)


    # 因为相位的不同 不能直接拿0:100信号去投影
    # 循环移位调整信号 
    normal_u = normal_u.tolist()
    Xffp = Xffp.tolist()
    if normal_u[-1] < 0 and normal_u[0] < 0:  #循环左移
        while(normal_u[len(normal_u)-1] < 0):
            shift_u = normal_u[1:] + normal_u[:1]
            normal_u = shift_u

            shift_Xffp = Xffp[1:] + Xffp[:1]
            Xffp = shift_Xffp
    else:                    #循环右移
        while(normal_u[len(normal_u)-1]>0):
            shift_u = normal_u[len(normal_u)-1:] + normal_u[:len(normal_u)-1]
            normal_u = shift_u

            shift_Xffp = Xffp[len(Xffp)-1:] + Xffp[:len(Xffp)-1]
            Xffp = shift_Xffp
        
    normal_u = np.array(normal_u)  
    Xffp = np.array(Xffp)


    pointx = FOV
    # ImgTan0 = griddata(Xffp[0:100], u[0:100], pointx, method='nearest')
    ImgTan0_normal = griddata(Xffp[0:100], normal_u[0:100], pointx, method='nearest')

    return ImgTan0_normal, normal_u, pointx, dXffp_Amp


# def projection_with_FOV(u,FOV,drive_field,d_drive_field,gradient_strength):
#     Xffp = drive_field[:]/gradient_strength  
#     dXffp = d_drive_field[:]/gradient_strength
#     dXffp_Amp = []
#     for i in range(len(dXffp)):
#         dXffp_Amp.append(math.sqrt(dXffp[i]**2))
#     normal_u = np.divide(u,dXffp_Amp)     
#     Xffp = np.array(Xffp)
#     pointx = FOV
    
    
#     ImgTan0 = griddata(Xffp[0:100], u[0:100], pointx, method='nearest')
#     ImgTan0_normal = griddata(Xffp[0:100], normal_u[0:100], pointx, method='nearest')

#     return ImgTan0_normal, normal_u, pointx, dXffp_Amp
