'''
作者:Jairus Chan
程序:多项式曲线拟合算法
'''

import math
import numpy as np

def val(f,ax):
    "val(f,ax):f(ax)"
    ay=[]
    for x in ax:
        y=0
        for i in range(len(f)-1,-1,-1):
            y=y*x+f[i]
        ay+=[y]
    return np.array(ay)

def fit(xa,ya,order):
    "fit(xa,ya,order)"
    matA=[]
    for i in range(0,order+1):
        matA1=[]
        for j in range(0,order+1):
            tx=0.0
            for k in range(0,len(xa)):
                dx=1.0
                for l in range(0,j+i):
                    dx=dx*xa[k]
                tx+=dx
            matA1.append(tx)
        matA.append(matA1)

    #print(len(xa))
    #print(matA[0][0])
    matA=np.array(matA)

    matB=[]
    for i in range(0,order+1):
        ty=0.0
        for k in range(0,len(xa)):
            dy=1.0
            for l in range(0,i):
                dy=dy*xa[k]
            ty+=ya[k]*dy
        matB.append(ty)

    matB=np.array(matB)

    return np.linalg.solve(matA,matB)
