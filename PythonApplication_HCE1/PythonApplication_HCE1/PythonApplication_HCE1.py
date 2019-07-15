#coding: utf-8

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
T = [273.15 for i in range(M+1)]

#境界条件
T[0] = 300.0  #温度固定
T[M] = T[M-1] #断熱

f = open('output','w')

for j in range(1,N):
    for i in range(1,M):
        preT = T

        #陽解法による差分式
        T[i] = a*preT[i+1]+(1-2*a)*preT[i]+a*preT[i-1]
        T[0] = 300.0
        T[M] = T[M-1]

    #計算結果をファイルへ出力
    f.write('# t=%ss\n'%(j*dt))
    for i in range(M+1):
        f.write('%s, %s\n'%(i*dx,T[i]))
    f.write('\n\n')

f.close()
