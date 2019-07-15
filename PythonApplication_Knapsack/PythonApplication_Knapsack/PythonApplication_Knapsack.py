from pyomo.environ import *
from pacman import *


v = {'applepie':8, 'beer':3, 'chocolatecake':6, 'duckmeat':11}
w = {'applepie':5, 'beer':7, 'chocolatecake':4, 'duckmeat':3}

limit = 14

M = ConcreteModel()
M.I = Set(initialize=v.keys())
M.x = Var(M.I, within=Binary)
M.value = Objective(expr=sum(v[i]*M.x[i] for i in M.I), sense=maximize)
M.weight = Constraint(expr=sum(w[i]*M.x[i] for i in M.I) <= limit)


print(v)
print(w)
print(limit)