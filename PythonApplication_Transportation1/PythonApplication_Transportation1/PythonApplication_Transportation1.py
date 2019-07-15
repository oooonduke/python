import numpy as np, pandas as pd
from itertools import product
from pulp import *
np.random.seed(1)
nw, nf = 3, 4
pr = list(product(range(nw),range(nf)))
供給 = np.random.randint(30, 50, nw)
需要 = np.random.randint(20, 40, nf)
輸送費 = np.random.randint(10, 20, (nw,nf))
####################################################################
m1 = LpProblem()
v1 = {(i,j):LpVariable('v%d_%d'%(i,j), lowBound=0) for i,j in pr}
m1 += lpSum(輸送費[i][j] * v1[i,j] for i,j in pr)
for i in range(nw):
    m1 += lpSum(v1[i,j] for j in range(nf)) <= 供給[i]
for j in range(nf):
    m1 += lpSum(v1[i,j] for i in range(nw)) >= 需要[j]
m1.solve()
{k:value(x) for k,x in v1.items() if value(x) > 0}

{(0, 0): 28.0,
 (0, 1): 7.0,
 (1, 2): 31.0,
 (1, 3): 5.0,
 (2, 1): 22.0,
 (2, 3): 20.0}
####################################################################
a = pd.DataFrame([(i,j) for i, j in pr], columns=['倉庫', '工場'])
a['輸送費'] = 輸送費.flatten()
a[:3]
m2 = LpProblem()
a['Var'] = [LpVariable('v%d'%i, lowBound=0) for i in a.index]
m2 += lpDot(a.輸送費, a.Var)
for k, v in a.groupby('倉庫'):
    m2 += lpSum(v.Var) <= 供給[k]
for k, v in a.groupby('工場'):
    m2 += lpSum(v.Var) >= 需要[k]
m2.solve()
a['Val'] = a.Var.apply(value)
a[a.Val > 0]
print(a)