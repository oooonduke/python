#!/bin/python3

import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from IPython.display import display, Markdown

def main():
  ch = 1.1e-7 # m2s-1

  t0 = float(input("Initial temperature [10 C] : ") or "10")
  t1 = float(input("Boundary temperature [75 C] : ") or "75")
  xmax = float(input("Thickness [4 cm] : ") or "4") * 0.005
  curvature = float(input("Curvature (0 for slab, 1.0 for cylinder, 2.0 for sphere) [0] : ") or "0")
  accel = float(input("acceleration (type 1 for accuracy) [3] : ") or "3")

  nsec = 100.0 * 2.5 * (xmax / 0.005)**2
  dt = 0.01 * (xmax / 0.005)**2 * (accel)**2
  dx = xmax / 25 * accel
  nx = int(xmax / dx)
  nstep = int(nsec / dt)

  # initialize
  tmp = np.full((nx,), t0)
  tmp[0] = t1
  dtmp = np.empty((nx,))
  os.system("mkdir -p img")
  os.system("rm -f img/*")

  r = np.linspace(xmax, 0, nx, endpoint=False) + dx / 2

  plot_intvl = 200
  for i in range(nstep):
    if (i % plot_intvl == 0):
      plot_snap(tmp, i, nx, xmax, dt, t0, t1)

    # boundary condition tmp[0] = t1, tmp[nx] = tmp[nx-1]
    # see a34p5-8 for different shape
    dtmp[0] = 0.0
    dtmp[1:nx-1] = ch * dt * ((tmp[2:nx] - 2.0 * tmp[1:nx-1] + tmp[0:nx-2]) / (dx * dx) \
      + curvature / r[1:nx-1] * (tmp[0:nx-2] - tmp[2:nx]) / (2 * dx))
    dtmp[nx-1] = ch * dt * ((tmp[nx-1] - 2.0 * tmp[nx-1] + tmp[nx-2]) / (dx * dx) \
      + curvature / r[nx-1] * (tmp[nx-2] - tmp[nx-1]) / dx)
    tmp[:] = tmp[:] + dtmp[:]

  os.system("convert -delay %d -loop 0 ./img/*.png ./img/all.gif" % (15 * accel))
  os.system("rm -f img/*.png")
  print("finish plotting")
  display(Markdown("![](sample.gif)"))



def plot_snap(tmp, i, nx, xmax, dt, t0, t1):
  cdict1 = {'red':   ((0.0, 1.0, 1.0),
                      (0.5, 1.0, 1.0),
                      (0.8, 0.6, 0.6),
                      (1.0, 0.6, 0.6)),
            'green': ((0.0, 0.2, 0.2),
                      (0.5, 0.2, 0.2),
                      (0.8, 0.5, 0.5),
                      (1.0, 0.5, 0.5)),
            'blue':  ((0.0, 0.3, 0.3),
                      (0.5, 0.3, 0.3),
                      (0.8, 0.4, 0.4),
                      (1.0, 0.4, 0.4)) }
  mycm = LinearSegmentedColormap('mycm', cdict1)

  xdim = 10
  data = np.zeros((nx*2,xdim))
  for k in range(xdim):
    data[0:nx,   k] = tmp
    data[nx:2*nx,k] = tmp[::-1]
  fig, ax = plt.subplots(1)
  map1 = ax.imshow(data, cmap=mycm, interpolation="bilinear", aspect="auto")
  map1.set_clim(0, 100.0)
  plt.tick_params(axis="x", which="both", bottom="off", top="off", labelbottom="off")
  plt.tick_params(axis="y", which="both", left="off", right="off", labelleft="off")
  cbar = plt.colorbar(map1)

  levels = np.arange(0, 100, 10)
  extent = (-0.5, xdim-0.5, 0, nx*2-1)
  map2 = ax.contour(data, levels, colors="w", extent=extent) # , origin="lower")
  ax.clabel(map2, fmt="%02d", colors="w")

  plt.title("[%d cm, init %i deg, boundary %i deg] t = %isec" % (xmax*2*100, t0, t1, i*dt))
  plt.savefig("./img/%06i.png" % i)
  plt.close()

main()