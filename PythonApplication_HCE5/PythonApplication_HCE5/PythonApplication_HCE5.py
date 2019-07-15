##https://qiita.com/damyarou/items/c7c206a1393ef328be68

##########################################
# 2DFEM unsteady heat conduction analysis
##########################################
import numpy as np
import sys
import time

############################
# Write input data
############################
def PRINP_H4(fnameW,npoin,nele,kot,koc,delta,niii,n1out,n2out,ae,x,tempe0,nokt,nekc,node):
    fout=open(fnameW,'w')
    # print out of input data
    print('{0:>5s} {1:>5s} {2:>5s} {3:>5s} {4:>5s} {5:>15s} {6:>5s} {7:>5s} {8:>5s}'
    .format('npoin','nele','nsec','kot','koc','delta','niii','n1out','n2out'),file=fout)
    print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d} {5:15.7e} {6:5d} {7:5d} {8:5d}'
    .format(npoin,nele,nsec,kot,koc,delta,niii,n1out,n2out),file=fout)
    print('{0:>5s} {1:>15s} {2:>15s} {3:>15s} {4:>15s} {5:>15s}'
    .format('sec','Ak','Ac','Arho','Tk','Al'),file=fout)
    for i in range(0,nsec):
        print('{0:5d} {1:15.7e} {2:15.7e} {3:15.7e} {4:15.7e} {5:15.7e}'
        .format(i+1,ae[0,i],ae[1,i],ae[2,i],ae[3,i],ae[4,i]),file=fout)
    print('{0:>5s} {1:>15s} {2:>15s} {3:>15s} {4:>5s}'
    .format('node','x','y','tempe0','Tfix'),file=fout)
    for i in range(0,npoin):
        kot1=0
        for k in range(0,kot):
            if nokt[k]-1==k: kot1=1
        lp=i+1
        print('{0:5d} {1:15.7e} {2:15.7e} {3:15.7e} {4:5d}'
        .format(lp,x[0,i],x[1,i],tempe0[i],kot1),file=fout)
    if 0<koc:
        #nekc[0,k]: element
        #nekc[1mk]: node to define a side
        print('{0:>5s} {1:>5s} {2:15s}'.format('nek0','nek1','alphac'),file=fout)
        for k in range(0,koc):
            print('{0:5d} {1:5d} {2:15.7e}'
            .format(nekc[0,k],nekc[1,k],alphac[k]),file=fout)

    print('{0:>5s} {1:>5s} {2:>5s} {3:>5s} {4:>5s} {5:>5s}'
    .format('elem','i','j','k','l','sec'),file=fout)
    for ne in range(0,nele):
        print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d} {5:5d}'
        .format(ne+1,node[0,ne],node[1,ne],node[2,ne],node[3,ne],node[4,ne]),file=fout)
    fout.close()


##############################
# [N] matrix
##############################
def NMAT_H4(ne,node,x,a,b):
    dnk=np.zeros([4,4],dtype=np.float64)
    dnc=np.zeros([4,4],dtype=np.float64)
    i=node[0,ne]-1
    j=node[1,ne]-1
    k=node[2,ne]-1
    l=node[3,ne]-1
    #[dN/da][dN/db]
    dn1a=-0.25*(1.0-b)
    dn2a= 0.25*(1.0-b)
    dn3a= 0.25*(1.0+b)
    dn4a=-0.25*(1.0+b)
    dn1b=-0.25*(1.0-a)
    dn2b=-0.25*(1.0+a)
    dn3b= 0.25*(1.0+a)
    dn4b= 0.25*(1.0-a)
    #Jacobi matrix & det(J)
    J11=dn1a*x[0,i]+dn2a*x[0,j]+dn3a*x[0,k]+dn4a*x[0,l]
    J12=dn1a*x[1,i]+dn2a*x[1,j]+dn3a*x[1,k]+dn4a*x[1,l]
    J21=dn1b*x[0,i]+dn2b*x[0,j]+dn3b*x[0,k]+dn4b*x[0,l]
    J22=dn1b*x[1,i]+dn2b*x[1,j]+dn3b*x[1,k]+dn4b*x[1,l]
    detJ=J11*J22-J12*J21
    #[dN/dx][dN/dy]
    dn1x=( J22*dn1a-J12*dn1b)/detJ
    dn2x=( J22*dn2a-J12*dn2b)/detJ
    dn3x=( J22*dn3a-J12*dn3b)/detJ
    dn4x=( J22*dn4a-J12*dn4b)/detJ
    dn1y=(-J21*dn1a+J11*dn1b)/detJ
    dn2y=(-J21*dn2a+J11*dn2b)/detJ
    dn3y=(-J21*dn3a+J11*dn3b)/detJ
    dn4y=(-J21*dn4a+J11*dn4b)/detJ
    dnk[0,0]=dn1x*dn1x+dn1y*dn1y
    dnk[0,1]=dn1x*dn2x+dn1y*dn2y
    dnk[0,2]=dn1x*dn3x+dn1y*dn3y
    dnk[0,3]=dn1x*dn4x+dn1y*dn4y
    dnk[1,0]=dn2x*dn1x+dn2y*dn1y
    dnk[1,1]=dn2x*dn2x+dn2y*dn2y
    dnk[1,2]=dn2x*dn3x+dn2y*dn3y
    dnk[1,3]=dn2x*dn4x+dn2y*dn4y
    dnk[2,0]=dn3x*dn1x+dn3y*dn1y
    dnk[2,1]=dn3x*dn2x+dn3y*dn2y
    dnk[2,2]=dn3x*dn3x+dn3y*dn3y
    dnk[2,3]=dn3x*dn4x+dn3y*dn4y
    dnk[3,0]=dn4x*dn1x+dn4y*dn1y
    dnk[3,1]=dn4x*dn2x+dn4y*dn2y
    dnk[3,2]=dn4x*dn3x+dn4y*dn3y
    dnk[3,3]=dn4x*dn4x+dn4y*dn4y
    #[N]
    nm1=0.25*(1.0-a)*(1.0-b)
    nm2=0.25*(1.0+a)*(1.0-b)
    nm3=0.25*(1.0+a)*(1.0+b)
    nm4=0.25*(1.0-a)*(1.0+b)
    dnc[0,0]=nm1*nm1
    dnc[0,1]=nm1*nm2
    dnc[0,2]=nm1*nm3
    dnc[0,3]=nm1*nm4
    dnc[1,0]=nm2*nm1
    dnc[1,1]=nm2*nm2
    dnc[1,2]=nm2*nm3
    dnc[1,3]=nm2*nm4
    dnc[2,0]=nm3*nm1
    dnc[2,1]=nm3*nm2
    dnc[2,2]=nm3*nm3
    dnc[2,3]=nm3*nm4
    dnc[3,0]=nm4*nm1
    dnc[3,1]=nm4*nm2
    dnc[3,2]=nm4*nm3
    dnc[3,3]=nm4*nm4
    return dnk,dnc,detJ

##############################
# Element coefficient matrix
##############################
def SM_H4(ne,node,x,ae):
    ekm=np.zeros([4,4],dtype=np.float64)
    ecm=np.zeros([4,4],dtype=np.float64)
    m=node[4,ne]-1
    Ak  =ae[0,m] #Ak   : Heat conductivity coefficient
    Ac  =ae[1,m] #Ac   : Specific heat
    Arho=ae[2,m] #Arho : Unit weight
    Tk  =ae[3,m] #Tk   : Maximum temperature rize
    Al  =ae[4,m] #Al   : Heat release rate
    for kk in range(0,4):
        if kk==0:
                a=-0.5773502692
                b=-0.5773502692
        if kk==1:
                a= 0.5773502692
                b=-0.5773502692
        if kk==2:
                a= 0.5773502692
                b= 0.5773502692
        if kk==3:
                a=-0.5773502692
                b= 0.5773502692
        dnk,dnc,detJ=NMAT_H4(ne,node,x,a,b)
        ekm=ekm+Ak*dnk*detJ
        ecm=ecm+Arho*Ac*dnc*detJ
    return ekm,ecm

##############################
# Element heat transfer matrix
##############################
def HTMAT_H4(ne,kchen,node,x,alpc):
    ht=np.zeros([4,4],dtype=np.float64)
    vn=np.zeros(4,dtype=np.float64)
    if kchen==0:
        i=node[0,ne]-1
        j=node[1,ne]-1
    if kchen==1:
        i=node[1,ne]-1
        j=node[2,ne]-1
    if kchen==2:
        i=node[2,ne]-1
        j=node[3,ne]-1
    if kchen==3:
        i=node[3,ne]-1
        j=node[0,ne]-1
    s=np.sqrt((x[0,j]-x[0,i])**2+(x[1,j]-x[1,i])**2)
    for kk in range(0,2):
        if kchen==0 and kk==0:
            a=-0.5773502692
            b=-1.0
        if kchen==0 and kk==1:
            a= 0.5773502692
            b=-1.0
        if kchen==1 and kk==0:
            a= 1.0
            b=-0.5773502692
        if kchen==1 and kk==1:
            a= 1.0
            b= 0.5773502692
        if kchen==2 and kk==0:
            a=-0.5773502692
            b= 1.0
        if kchen==2 and kk==1:
            a= 0.5773502692
            b= 1.0
        if kchen==3 and kk==0:
            a=-1.0
            b=-0.5773502692
        if kchen==3 and kk==1:
            a=-1.0
            b= 0.5773502692
        #[N]
        vn[0]=0.25*(1.0-a)*(1.0-b)
        vn[1]=0.25*(1.0+a)*(1.0-b)
        vn[2]=0.25*(1.0+a)*(1.0+b)
        vn[3]=0.25*(1.0-a)*(1.0+b)
        for i in range(0,4):
            for j in range(0,4):
                ht[i,j]=ht[i,j]+0.5*s*alpc*vn[i]*vn[j]
    return ht

##############################
# Heat generation rate vector
##############################
def FQVEC_H4(ne,node,x,dotq):
    fq=np.zeros(4,dtype=np.float64)
    vn=np.zeros(4,dtype=np.float64)
    for kk in range(0,4):
        i=node[0,ne]-1
        j=node[1,ne]-1
        k=node[2,ne]-1
        l=node[3,ne]-1
        if kk==0:
            a=-0.5773502692
            b=-0.5773502692
        if kk==1:
            a= 0.5773502692
            b=-0.5773502692
        if kk==2:
            a= 0.5773502692
            b= 0.5773502692
        if kk==3:
            a=-0.5773502692
            b= 0.5773502692
        #[dN/da][dN/db]
        dn1a=-0.25*(1.0-b)
        dn2a= 0.25*(1.0-b)
        dn3a= 0.25*(1.0+b)
        dn4a=-0.25*(1.0+b)
        dn1b=-0.25*(1.0-a)
        dn2b=-0.25*(1.0+a)
        dn3b= 0.25*(1.0+a)
        dn4b= 0.25*(1.0-a)
        #Jacobi matrix & det(J)
        J11=dn1a*x[0,i]+dn2a*x[0,j]+dn3a*x[0,k]+dn4a*x[0,l]
        J12=dn1a*x[1,i]+dn2a*x[1,j]+dn3a*x[1,k]+dn4a*x[1,l]
        J21=dn1b*x[0,i]+dn2b*x[0,j]+dn3b*x[0,k]+dn4b*x[0,l]
        J22=dn1b*x[1,i]+dn2b*x[1,j]+dn3b*x[1,k]+dn4b*x[1,l]
        detJ=J11*J22-J12*J21
        #[N]
        vn[0]=0.25*(1.0-a)*(1.0-b)
        vn[1]=0.25*(1.0+a)*(1.0-b)
        vn[2]=0.25*(1.0+a)*(1.0+b)
        vn[3]=0.25*(1.0-a)*(1.0+b)
        fq=fq+dotq*vn*detJ
    return fq

##########################
# Heat transfer vector
##########################
def HTVEC_H4(ne,kchen,node,x,alpc,tc):
    fc=np.zeros(4,dtype=np.float64)
    vn=np.zeros(4,dtype=np.float64)
    if kchen==0:
        i=node[0,ne]-1
        j=node[1,ne]-1
    if kchen==1:
        i=node[1,ne]-1
        j=node[2,ne]-1
    if kchen==2:
        i=node[2,ne]-1
        j=node[3,ne]-1
    if kchen==3:
        i=node[3,ne]-1
        j=node[0,ne]-1
    s=np.sqrt((x[0,j]-x[0,i])**2+(x[1,j]-x[1,i])**2)
    for kk in range(0,2):
        if kchen==0 and kk==0:
            a=-0.5773502692
            b=-1.0
        if kchen==0 and kk==1:
            a= 0.5773502692
            b=-1.0
        if kchen==1 and kk==0:
            a= 1.0
            b=-0.5773502692
        if kchen==1 and kk==1:
            a= 1.0
            b= 0.5773502692
        if kchen==2 and kk==0:
            a=-0.5773502692
            b= 1.0
        if kchen==2 and kk==1:
            a= 0.5773502692
            b= 1.0
        if kchen==3 and kk==0:
            a=-1.0
            b=-0.5773502692
        if kchen==3 and kk==1:
            a=-1.0
            b= 0.5773502692
        #[N]
        vn[0]=0.25*(1.0-a)*(1.0-b)
        vn[1]=0.25*(1.0+a)*(1.0-b)
        vn[2]=0.25*(1.0+a)*(1.0+b)
        vn[3]=0.25*(1.0-a)*(1.0+b)
        fc=fc+0.5*s*alpc*tc*vn
    return fc


############################
# Main routine
############################
start=time.time()
args = sys.argv
#fnameR=args[1] # input data file
#fnameT=args[2] # Temperature fixed node data
#fnameW=args[3] # output data file
fnameR="inp_div20_model.txt" # input data file
fnameT="inp_div20_thist.txt" # Temperature fixed node data
fnameW="out_div20.txt" # output data file



f=open(fnameR,'r')
text=f.readline()
text=text.strip()
text=text.split()
npoin =int(text[0])   # Number of nodes
nele  =int(text[1])   # Number of elements
nsec  =int(text[2])   # Number of sections
kot   =int(text[3])   # Number of nodes with given temperature
koc   =int(text[4])   # Number of sides with heat transfer boundary
delta =float(text[5]) # Time increment
nod=4                 # Number of nodes per element
nfree=1               # Degree of freedom per node
n=nfree*npoin

x     =np.zeros([2,npoin],dtype=np.float64)  # Coordinates of nodes
ae    =np.zeros([5,nsec],dtype=np.float64)   # Section characteristics
node  =np.zeros([nod+1,nele],dtype=np.int)   # Node-element relationship
nokt  =np.zeros(kot,dtype=np.int)            # Nodes with given temperature
nekc  =np.zeros([2,koc],dtype=np.int)          # Elements and sides with heat transfer boundary
tempe0=np.zeros(n,dtype=np.float64)          # Initial temperature of nodes
alphac=np.zeros(koc,dtype=np.float64)        # Heat transfer rate of sides of element
ir    =np.zeros(nod*nfree,dtype=np.int)      # Work vector for matrix assembly
Tinp  =np.zeros(kot,dtype=np.float64)        # Temperature of given temperature node
Tcin1 =np.zeros(koc,dtype=np.float64)        # Temperature of heat transfer boundary node (previous)
Tcin2 =np.zeros(koc,dtype=np.float64)        # Temperature of heat transfer boundary node (current)

# section characteristics
for i in range(0,nsec):
    text=f.readline()
    text=text.strip()
    text=text.split()
    ae[0,i]=float(text[0]) #Ak    : Heat conductivity coefficient
    ae[1,i]=float(text[1]) #Ac    : Specific heat
    ae[2,i]=float(text[2]) #Arho  : Unit weight
    ae[3,i]=float(text[3]) #Tk    : Maximum temperature rize
    ae[4,i]=float(text[4]) #Al    : Heat release rate
# element-node
for i in range(0,nele):
    text=f.readline()
    text=text.strip()
    text=text.split()
    node[0,i]=int(text[0]) #node_1
    node[1,i]=int(text[1]) #node_2
    node[2,i]=int(text[2]) #node_3
    node[3,i]=int(text[3]) #node_4
    node[4,i]=int(text[4]) #section characteristic number
# node coordinates
for i in range(0,npoin):
    text=f.readline()
    text=text.strip()
    text=text.split()
    x[0,i] =float(text[0])   # x-coordinate
    x[1,i] =float(text[1])   # y-coordinate
    tempe0[i]=float(text[2]) # Initial temperature of node
# boundary conditions
if 0<kot:
    for i in range(0,koh):
        text=f.readline()
        text=text.strip()
        text=text.split()
        nokt[i]=int(text[0])
if 0<koc:
    for i in range(0,koc):
        text=f.readline()
        text=text.strip()
        text=text.split()
        nekc[0,i]=int(text[0])
        nekc[1,i]=int(text[1])
        alphac[i]=float(text[2])
# Nodes for all time temperature output
text=f.readline()
text=text.strip()
text=text.split()
n1out=int(text[0])
if 0<n1out:
    n1node=np.zeros(n1out,dtype=np.int) # node for all time temperature output
    text=f.readline()
    text=text.strip()
    text=text.split()
    for i in range(0,n1out):
        n1node[i]=int(text[i])
# Frequency for all nodes temperature output
text=f.readline()
text=text.strip()
text=text.split()
n2out=int(text[0])
if 0<n2out:
    n2step     =np.zeros(n2out,dtype=np.int) # time step for all nodes temperature output
    temperature=np.zeros([n2out,npoin],dtype=np.float64) # memory of temperature
    text=f.readline()
    text=text.strip()
    text=text.split()
    for i in range(0,n2out):
        n2step[i]=int(text[i])
f.close()

# Assembly of permeability matrix, [k] is calculated using {h1}
gk1=np.zeros([n,n],dtype=np.float64)  # Global stiffness matrix
gk2=np.zeros([n,n],dtype=np.float64)  # Global stiffness matrix
for ne in range(0,nele):
    ekm,ecm=SM_H4(ne,node,x,ae)
    ck1=-0.5*ekm+ecm/delta
    ck2= 0.5*ekm+ecm/delta
    i=node[0,ne]-1
    j=node[1,ne]-1
    k=node[2,ne]-1
    l=node[3,ne]-1
    ir[3]=l; ir[2]=k; ir[1]=j; ir[0]=i
    for i in range(0,nod*nfree):
        it=ir[i]
        for j in range(0,nod*nfree):
            jt=ir[j]
            gk1[it,jt]=gk1[it,jt]+ck1[i,j]
            gk2[it,jt]=gk2[it,jt]+ck2[i,j]
    #Treatment of heat transfer boundary
    if 0<koc:
        for k in range(0,koc):
            if ne==nekc[0,k]-1:
                if nekc[1,k]-1==node[0,ne]-1: kchen=0
                if nekc[1,k]-1==node[1,ne]-1: kchen=1
                if nekc[1,k]-1==node[2,ne]-1: kchen=2
                if nekc[1,k]-1==node[3,ne]-1: kchen=3
                alpc=alphac[k]
                ht=HTMAT_H4(ne,kchen,node,x,alpc) # Heat transfer matrix
                ht=0.5*ht
                for i in range(0,nod*nfree):
                    it=ir[i]
                    for j in range(0,nod*nfree):
                        jt=ir[j]
                        gk2[it,jt]=gk2[it,jt]+ht[i,j]
                        gk1[it,jt]=gk1[it,jt]-ht[i,j]
# Setting initial temperatures of nodes
tempe=tempe0
# Setting initial temperatures for heat transfer boundaries
if 0<koc:
    for k in range(0,koc):
        ne=nekc[0,k]-1
        if nekc[1,k]-1==node[0,ne]-1:
            ia=node[0,ne]-1
            ja=node[1,ne]-1            
        if nekc[1,k]-1==node[1,ne]-1:
            ia=node[1,ne]-1
            ja=node[2,ne]-1
        if nekc[1,k]-1==node[2,ne]-1:
            ia=node[2,ne]-1
            ja=node[3,ne]-1
        if nekc[1,k]-1==node[3,ne]-1:
            ia=node[3,ne]-1
            ja=node[1,ne]-1
        Tcin1[k]=0.5*(tempe[ia]+tempe[ja])

# Read file for temperature time histories of given temperature nodes
ft=open(fnameT,'r')
dat_Tinp=ft.readlines()
ft.close()

# Print out of input data
niii=len(dat_Tinp)+1
PRINP_H4(fnameW,npoin,nele,kot,koc,delta,niii,n1out,n2out,ae,x,tempe0,nokt,nekc,node)

#====================================
# Start of Time history calculation
#====================================
iii=0
ttime=delta*float(iii)
fout=open(fnameW,'a')
if 0<n1out:   
    # print out of initial temperatures
    ss='{0:>5s} {1:>15s}'.format('iii','ttime')
    for i in range(0,n1out):
        sn='Node_'+str(n1node[i])
        ss=ss+' {0:>15s}'.format(sn)
    print(ss,file=fout)
    ss='{0:5d} {1:15.7e}'.format(iii,ttime)
    for i in range(0,n1out):
        ss=ss+' {0:15.7e}'.format(tempe[n1node[i]-1])
    print(ss,file=fout)

for text in dat_Tinp:
    iii=iii+1
    ttime=delta*float(iii)

    text=text.strip()
    text=text.split()
    if kot==0 and koc==0:
        lp=int(text[0]) # step
    if 0<kot and koc==0:
        lp=int(text[0]) # step
        i=0
        for k in range(0,kot):
            i=i+1; Tinp[k]=float(text[i]) # Given temperature
    if kot==0 and 0<koc:
        lp=int(text[0]) # step
        i=0
        for k in range(0,koc):
            i=i+1; Tcin2[k]=float(text[i]) # Given temperature
    if 0<kot and 0<koc:
        lp=int(text[0]) # step
        i=0
        for k in range(0,kot):
            i=i+1; Tinp[k]=float(text[i]) # Given temperature
        for k in range(0,koc):
            i=i+1; Tcin2[k]=float(text[i]) # Given temperature

    ftvec=np.zeros(n,dtype=np.float64)
    reac =np.zeros(n,dtype=np.float64)
    for ne in range(0,nele):
        # Heat generation rate vector
        m=node[4,ne]-1
        Ak  =ae[0,m] #Ak   : Heat conductivity coefficient
        Ac  =ae[1,m] #Ac   : Specific heat
        Arho=ae[2,m] #Arho : Unit weight
        Tk  =ae[3,m] #Tk   : Maximum temperature rize
        Al  =ae[4,m] #Al   : Heat release rate
        dotq=Arho*Ac*Tk*Al*np.exp(-Al*(ttime-0.5*delta))
        fq=FQVEC_H4(ne,node,x,dotq)
        i=node[0,ne]-1
        j=node[1,ne]-1
        k=node[2,ne]-1
        l=node[3,ne]-1
        ir[3]=l; ir[2]=k; ir[1]=j; ir[0]=i
        for i in range(0,nod*nfree):
            it=ir[i]
            ftvec[it]=ftvec[it]+fq[i]
        # Heat transfer vector
        if 0<koc:
            for k in range(0,koc):
                if ne==nekc[0,k]-1:
                    if nekc[1,k]-1==node[0,ne]-1: kchen=0
                    if nekc[1,k]-1==node[1,ne]-1: kchen=1
                    if nekc[1,k]-1==node[2,ne]-1: kchen=2
                    if nekc[1,k]-1==node[3,ne]-1: kchen=3
                    alpc=alphac[k]
                    tc=0.5*(Tcin1[k]+Tcin2[k])
                    fc=HTVEC_H4(ne,kchen,node,x,alpc,tc)
                    for i in range(0,nod*nfree):
                        it=ir[i]
                        ftvec[it]=ftvec[it]+fc[i]
    reac=ftvec+np.dot(gk1,tempe)
    _gk2=gk2
    if 0<kot:
        for k in range(0,kot):
            iz=nokt[k]-1
            reac[iz]=0.0
            for i in range(0,n):
                reac[i]=reac[i]-Tinp[k]*_gk2[i,iz]
                _gk2[i,iz]=0.0
            _gk2[iz,iz]=1.0
    # solution of simultaneous linear equations
    if iii==1: inv_gk2=np.linalg.inv(_gk2)
    tempe = np.dot(inv_gk2, reac)
    del ftvec, reac
    if 0<kot:
        for k in range(0,kot):
            tempe[nokt[k]-1]=Tinp[k]
    if 0<koc:
        for k in range(0,koc):
            Tcin1[k]=Tcin2[k]

    # print out of node temperatures at specified nodes 
    if 0<n1out:
        ss='{0:5d} {1:15.7e}'.format(iii,ttime)
        for i in range(0,n1out):
            ss=ss+' {0:15.7e}'.format(tempe[n1node[i]-1])
        print(ss,file=fout)
    # Memory of temperature
    if 0<n2out:
        for i in range(0,n2out):
            if n2step[i]==iii:
                temperature[i,:]=tempe[:]
#====================================
# End of Time history calculation
#====================================

# Print out of all node temperatures at specified times
if 0<n2out:
    ss='{0:>5s}'.format('node')
    st='t=0.0'
    ss=ss+' {0:>15s}'.format(st)
    for i in range(0,n2out):
        ttime=float(n2step[i])*delta
        st='t='+str(ttime)
        ss=ss+' {0:>15s}'.format(st)
    print(ss,file=fout)
    for i in range(0,npoin):
        ss='{0:5d}'.format(i+1)
        ss=ss+' {0:15.7e}'.format(tempe0[i])
        for j in range(0,n2out):
            ss=ss+' {0:15.7e}'.format(temperature[j,i])
        print(ss,file=fout)

dtime=time.time()-start
print('n={0}  time={1:.3f}'.format(n,dtime)+' sec')
fout=open(fnameW,'a')
print('n={0}  time={1:.3f}'.format(n,dtime)+' sec',file=fout)
fout.close()
