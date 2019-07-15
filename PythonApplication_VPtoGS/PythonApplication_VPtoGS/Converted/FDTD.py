""" From "COMPUTATIONAL PHYSICS", 3rd Ed, Enlarged Python eTextBook  
    by RH Landau, MJ Paez, and CC Bordeianu
    Copyright Wiley-VCH Verlag GmbH & Co. KGaA, Berlin;  Copyright R Landau,
    Oregon State Unv, MJ Paez, Univ Antioquia, C Bordeianu, Univ Bucharest, 2015.
    Support by National Science Foundation"""

# FDTD.py  FDTD solution of Maxwell's equations in 1-D

from visual import *
xmax=201
ymax=100
zmax=100
scene = canvas(x=0,y=0,width= 800, height= 500, title= 'E: cyan, H: red. Periodic BC',forward=vector(-0.6,-0.5,-1))
Efield = curve(x=list(range(0,xmax)),color=color.cyan,radius=1.5,canvas=scene)
Hfield = curve(x=list(range(0,xmax)),color=color.red, radius=1.5,canvas=scene)
vplane= curve(pos=[(-xmax,ymax),(xmax,ymax),(xmax,-ymax),(-xmax,-ymax), (-xmax,ymax)],color=color.cyan)
zaxis=curve(pos=[(-xmax,0),(xmax,0)],color=color.magenta)
hplane=curve(pos=[(-xmax,0,zmax),(xmax,0,zmax),(xmax,0,-zmax),(-xmax,0,-zmax), (-xmax,0,zmax)],color=color.magenta)
ball1 = sphere(pos = vector(xmax+30, 0,0), color = color.black, radius = 2)
# time switch
ts = 2                          
beta = 0.01
# init E 
Ex = zeros((xmax,ts),float)      
# init H 
Hy = zeros((xmax,ts),float)      
Exlabel1 = label( text = 'Ex', pos = vector(-xmax-10, 50,0), box = 0 )
Exlabel2 = label( text = 'Ex', pos = vector(xmax+10, 50,0), box = 0 )
Hylabel  = label( text = 'Hy', pos = vector(-xmax-10, 0,50), box = 0 )
zlabel   = label( text = 'Z',  pos = vector(xmax+10, 0,0), box = 0 )   
ti=0                                

def inifields():
    k = arange(xmax)
    Ex[:xmax,0] = 0.1*sin(2*pi*k/100.0)
    Hy[:xmax,0] = 0.1*sin(2*pi*k/100.0)
    
# screen coordinates
def plotfields(ti):                         
    k = arange(xmax)
# world to screen coords
    Efield.x = 2*k-xmax                     
    Efield.y = 800*Ex[k,ti]
    Hfield.x = 2*k-xmax                           
    Hfield.z = 800*Hy[k,ti]   
        
# initial field
inifields()                                 
plotfields(ti)
while True:
    rate(600)
    Ex[1:xmax-1,1] = Ex[1:xmax-1,0] + beta*(Hy[0:xmax-2,0]-Hy[2:xmax,0])
    Hy[1:xmax-1,1] = Hy[1:xmax-1,0] + beta*(Ex[0:xmax-2,0]-Ex[2:xmax,0])
# BC
    Ex[0,1]        = Ex[0,0]        + beta*(Hy[xmax-2,0]  -Hy[1,0]) 
    Ex[xmax-1,1]   = Ex[xmax-1,0]   + beta*(Hy[xmax-2,0]  -Hy[1,0])  
# BC
    Hy[0,1]        = Hy[0,0]        + beta*(Ex[xmax-2,0]  -Ex[1,0]) 
    Hy[xmax-1,1]   = Hy[xmax-1,0]   + beta*(Ex[xmax-2,0] - Ex[1,0]) 
    plotfields(ti)                                       
# New->old
    Ex[:xmax,0] = Ex[:xmax,1]                            
    Hy[:xmax,0] = Hy[:xmax,1]                                  

