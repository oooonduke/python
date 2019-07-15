#https://qiita.com/itisyuu/items/9dc192b6c1ce9f808518

import pulp

prob = pulp.LpProblem('CalcFood', pulp.LpMinimize)
list =[(0.2, 0.1, 0.3, 300), (0.3, 0.1, 0.3, 400), (0.2, 0.4, 0.1, 150), (0.1, 0.4, 0.4, 300), (0.4, 0.3, 0.4, 500)]


x = []
for i in range(len(list)):
    x.append(pulp.LpVariable('x[%s]'%i, 0, 5, 'Integer'))

prob1 = 0
for j in range(len(list)):
    prob1 += (list[j][3] * x[j])  
prob += prob1



prob1 = 0
prob2 = 0
prob3 = 0
for i in range(len(list)):
    prob1 += list[i][0] * x[i]
    prob2 += (list[i][1] * x[i])
    prob3 += (list[i][2] * x[i])
print(prob1)
prob += prob1 >=2.0  # 制約条件　赤
prob += prob2 >=1.0  # 制約条件　緑
prob += prob3 >=3.0  # 制約条件　黄


print(prob)

status = prob.solve()
print(pulp.LpStatus[status])

for i in range(len(x)):
    print("x[", i, "]", pulp.value(x[i]))
