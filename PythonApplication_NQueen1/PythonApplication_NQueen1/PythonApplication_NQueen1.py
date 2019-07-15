%matplotlib inline
import pandas as pd, matplotlib.pyplot as plt
from itertools import product
from ortoolpy import addvar
from pulp import *
def NQueen(N):
    r = range(N)
    m = LpProblem()
    a = pd.DataFrame([(i, j, addvar(cat=LpBinary))
        for i, j in product(r, r)], columns=['縦', '横', 'x'])
    for i in r:
        m += lpSum(a[a.縦 == i].x) == 1
        m += lpSum(a[a.横 == i].x) == 1
    for i in range(2*N-1):
        m += lpSum(a[a.縦 + a.横 == i].x) <= 1
        m += lpSum(a[a.縦 - a.横 == i-N+1].x) <= 1
    %time m.solve()
    m.solve()
    return a.x.apply(value).reshape(N, -1)

for N in [8, 16, 32, 64, 128]:
    plt.imshow(NQueen(N), cmap='gray', interpolation='none')
    plt.show()