
import pulp as pp
import numpy as np

# 最適化モデルの定義
mip_model = pp.LpProblem("tsp_mip", pp.LpMinimize)

# ループ回数
N = 100
BigM = 9223372036854775807
# 空の辞書
x = {}
u = {}

# 変数の定義
for i in range(N):
    for j in range(N):
        if i != j:
            x[i, j] = pp.LpVariable("x(%s,%s)"%(i, j), cat="Binary")

for i in range(N):
    u[i] = pp.LpVariable("u(%s)"%(i), cat="Continuous", lowBound=1.0, upBound=(N - 1.0))

# 評価指標（式（１））の定義＆登録
#objective = pp.lpSum(c_[i, j] * x[i, j] for i in range(N) for j in range(N) if i != j)
objective = pp.lpSum(x[i, j] for i in range(N) for j in range(N) if i != j)
mip_model += objective


#　条件式(2)の登録
for i in range(N):
    mip_model += pp.lpSum(x[i, j] for j in range(N) if i != j) == 1

# 条件式(3)の登録
for i in range(N):
    mip_model += pp.lpSum(x[j, i] for j in range(N) if i != j) == 1

# 条件式(4) (MTZ制約)
for i in range(N):
    for j in range(N):
        if i != j:
            mip_model += u[i] + 1.0 - BigM * (1.0 - x[i, j]) <= u[j]


# 最適化の実行
status = mip_model.solve()

# 結果の把握
print("Status: {}".format(pp.LpStatus[status]))
print("Optimal Value [a.u.]: {}".format(objective.value()))