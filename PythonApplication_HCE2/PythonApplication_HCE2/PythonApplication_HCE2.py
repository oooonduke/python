#coding: utf-8

import numarray
import numarray.linear_algebra as la

L = 0.1  #長さ[m]
M = 10   #分割数
dx = L/M #空間刻み[m]

dt = 1.0 #時間刻み[s]
N = 100  #時間ステップ数

#温度伝導率(鉄)
alpha = 80.2/(7874.0*440.0)

gamma = dt/dx**2
a = alpha*gamma

#初期条件(温度273.15K)
T = numarray.array([[273.15,] for i in range(M+1)])
#境界条件
T[0][0] = 300.0  #温度固定
T[M][0] = T[M-1][0] #断熱

#行列の作成
A = numarray.array([[0. for i in range(M+1)] for j in range(M+1)])
for i in range(1,M):
    A[i][i-1] = -a
    A[i][i]   = 1+2*a
    A[i][i+1] = -a
#境界条件
A[0][0] = 1.   #一定温度
A[M][M]   = 1. #断熱

#Aの逆行列
A_inv = la.inverse(A)

f = open('output','w')

for j in range(1,N):
    preT = T

    T = numarray.dot(A_inv, preT)
    T[0][0] = 300.0
    T[M][0] = T[M-1][0]

    #計算結果をファイルへ出力
    f.write('# t=%ss\n'%(j*dt))
    for i in range(M+1):
        f.write('%s, %s\n'%(i*dx,T[i][0]))
    f.write('\n\n')

f.close()
