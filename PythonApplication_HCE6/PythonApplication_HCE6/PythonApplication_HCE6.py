#***************************************
# make 2D temperature history for FEM
#***************************************
import matplotlib.pyplot as plt
import sys
import numpy as np

#Main routine
param=sys.argv
fnameR="inp_div20_thist.txt"
#fnameR=param[1]
#fnameW=param[2]

# Data input
fin=open(fnameR,'r')
text=fin.readline()
text=fin.readline()
text=text.strip()
text=text.split()
npoin=int(text[0])
nele =int(text[1])
nsec =int(text[2])
kot  =int(text[3])
koc  =int(text[4])
delta=float(text[5])
niii =int(text[6])
n1out=int(text[7])
n2out=int(text[8])
nod=4

node =np.zeros([nod+1,npoin],dtype=np.int)
x    =np.zeros(npoin,dtype=np.float64)
y    =np.zeros(npoin,dtype=np.float64)
tvec1=np.zeros([niii,n1out],dtype=np.float64)
tvec2=np.zeros([npoin,n2out+1],dtype=np.float64)
time1=np.zeros(niii,dtype=np.float64)
time2=np.zeros(n2out+1,dtype=np.float64)
pnode=np.zeros(n1out,dtype=np.int)

text=fin.readline()
for i in range(0,nsec):
    text=fin.readline()
text=fin.readline()
for i in range(0,npoin):
    text=fin.readline()
    text=text.strip()
    text=text.split()
    x[i]=float(text[1])
    y[i]=float(text[2])
if 0<koc:
    text=fin.readline()
    for i in range(0,koc):
        text=fin.readline()
text=fin.readline()
for ne in range(0,nele):
    text=fin.readline()
    text=text.strip()
    text=text.split()
    node[0,ne]=int(text[1]) #node_1
    node[1,ne]=int(text[2]) #node_2
    node[2,ne]=int(text[3]) #node_3
    node[3,ne]=int(text[4]) #node_4
    node[4,ne]=int(text[5]) #section number
if 0<n1out:
    text=fin.readline()
    text=text.strip()
    text=text.split()
    for j in range(0,n1out):
        pnode[j]=float(text[j+2].replace('Node_',''))
    for i in range(0,niii):
        text=fin.readline()
        text=text.strip()
        text=text.split()
        time1[i]=float(text[1])
        for j in range(0,n1out):
            tvec1[i,j]=float(text[2+j])
if 0<n2out:
    text=fin.readline()
    text=text.strip()
    text=text.split()
    for j in range(0,n2out+1):
        time2[j]=float(text[j+1].replace('t=',''))
    for i in range(0,npoin):
        text=fin.readline()
        text=text.strip()
        text=text.split()
        for j in range(0,n2out+1):
            tvec2[i,j]=float(text[1+j])
fin.close()

xmin=np.min(time1)
xmax=np.max(time1)
ymin=np.min(tvec1)
ymax=np.max(tvec1)
ymin=0.0
ymax=60.0

fnameF='_fig_tem_his.png'
fig = plt.figure()
ax1=plt.subplot(111)
ax1.set_xlim([xmin,xmax])
ax1.set_ylim([ymin,ymax])
ax1.set_xlabel('Time (hour)')
ax1.set_ylabel('Temperature ($^\circ$C)')
xx=time1
for iii in range(0,n1out):
    lxp=str('{0:.1f}'.format(x[pnode[iii]-1]))
    lyp=str('{0:.1f}'.format(y[pnode[iii]-1]))
    ls='Node_'+str(pnode[iii])+' (x,y)=('+lxp+','+lyp+')'
    yy=tvec1[:,iii]
    ax1.plot(xx,yy,'-',label=ls)
ax1.grid(linestyle='-',color='#aaaaaa')
ax1.legend(loc='upper right',numpoints=1,prop={'family':'monospace','size':12})
plt.savefig(fnameF, bbox_inches="tight", pad_inches=0.2)
plt.clf()
