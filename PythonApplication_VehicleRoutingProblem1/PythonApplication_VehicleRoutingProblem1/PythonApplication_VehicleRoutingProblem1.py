import pulp
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt
num_client = 15 #顧客数（id=0,1,2,...14と番号が振られていると考える。id=0はデポ。）
capacity = 50   #トラックの容量
randint = np.random.randint

seed = 10
# 各顧客のx,y座標と需要（どのくらいの商品が欲しいか）をDataFrameとして作成
df = pd.DataFrame({"x":randint(0,100,num_client),
                   "y":randint(0,100,num_client),
                   "d":randint(5,40,num_client)})
#0番目の顧客はデポ（拠点）とみなす。なので、需要=0, 可視化の時に真ん中に来るよう、
#x,yを50に。
df.ix[0].x = 50
df.ix[0].y = 50
df.ix[0].d = 0
# costは顧客数✖️顧客数の距離テーブル。np.arrayで保持。
cost = create_cost()
# subtoursはデポ（id=0)を除いた顧客の全部分集合。これがなんの役に立つかは後ほど。
subtours = []
for length in range(2,num_client):
     subtours += itertools.combinations(range(1,num_client),length)

# xは顧客数✖️顧客数のbinary変数Array。Costテーブルと対応している。1ならばその間をトラックが走ることになる。
# num_vは必要なトラック台数変数。
x = np.array([[pulp.LpVariable("{0}_{1}".format(i,j),0,1,"Binary")
               for j in range(num_client)]
              for i in range(num_client)])
num_v = pulp.LpVariable("num_v",0,100,"Integer")

#問題の宣言と目的関数設定。目的関数は、総距離最小化。
problem = pulp.LpProblem('vrp_simple_problem', pulp.LpMinimize)
problem += pulp.lpSum([x[i][j]*cost[i][j]
                       for i in range(num_client)
                      for j in range(num_client)])

# 顧客1から顧客1に移動といった結果は有り得ないので除外
for t in range(num_client):
    problem += x[t][t] == 0

# 顧客から出て行くアーク（トラック）と入っていくアーク（トラック）はそれぞれ必ず１本
for t in range(1,num_client):
    problem += pulp.lpSum(x[:,t]) == 1
    problem += pulp.lpSum(x[t,:]) == 1

# デポ（ここでは、id=0)に入ってくるアーク（トラック）と出て行くアーク（トラック）の本数は必ず一緒。
problem += pulp.lpSum(x[:,0]) == num_v
problem += pulp.lpSum(x[0,:]) == num_v

# ここは肝。上記までの制約だと、デポに戻らない孤立閉路が出来てしまう。ここでやっているのは、
# subtour eliminate制約。さらに、需要も見て、ここでCapacity制約も追加している。興味がある
# 方は、subtour eliminateで検索してください。
for st in subtours:
    arcs = []
    demand = 0
    for s in st:
        demand += df_dpsts["d"][s]
    for i,j in itertools.permutations(st,2):
        arcs.append(x[i][j])
    print(len(st) - np.max([0,np.ceil(demand/capacity)]))
    problem += pulp.lpSum(arcs) <= np.max([0,len(st) - np.ceil(demand/capacity)])

#計算及び結果の確認
status = problem.solve()
print("Status", pulp.LpStatus[status])
for i in range(num_client):
    for j in range(num_client):
        print(i,j,x[i][j].value())

output_image(G,x)
