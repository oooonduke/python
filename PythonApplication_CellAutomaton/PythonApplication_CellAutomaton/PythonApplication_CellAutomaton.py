# -*- coding: utf-8 -*-
"""
traffic.pyプログラム
セルオートマトンに基づく交通流シミュレーション
ルールと初期状態から，時間発展を計算する
使い方　c:\>python traffic.py < (初期状態ファイル名)
"""
# モジュールのインポート
import sys  # sys.exit()の利用に必要

# 定数
N = 50      # セルの最大個数
R = 8       # ルール表の大きさ
MAXT = 50   # 繰り返しの回数
RULE = 184  # ルール番号（184に固定）

# 下請け関数の定義
# setrule()関数
def setrule(rule, ruleno):
    """ルール表の初期化"""
    # ルール表の書き込み
    for i in range(0, R):
        rule[i] = ruleno % 2
        ruleno = ruleno // 2  # 左シフト
# setrule()関数の終わり

# initca()関数
def initca(ca):
    """セルオートマトンへの初期値の読み込み"""
    # 初期値を読み込む
    line = input("caの初期値を入力してください:")
    print()
    # 内部表現への変換
    for no in range(len(line)):
        ca[N - 1 - no] = int(line[no])
# initca()関数の終わり

# putca()関数
def putca(ca):
    """caの状態の出力"""
    for no in range(N - 1, -1, -1):
        if ca[no] == 1:
            outputstr = "-"
        else:
            outputstr = " "
        print("{:1s}".format(outputstr), end="")
    print()
# putca()関数の終わり

# nextt()関数
def nextt(ca, rule):
    """caの状態の更新"""
    nextca = [0 for i in range(N)]  # 次世代のca
    # ルールの適用
    for i in range(1, N - 1):
        nextca[i] = rule[ca[i + 1] * 4 + ca[i] * 2 + ca[i - 1]]
    # caの更新
    for i in range(N):
        ca[i] = nextca[i]
# nextt()関数の終わり

# メイン実行部
# 流入率の初期化
flowrate = int(input("流入率を入力してください:"))
print()
if flowrate <= 0:
        print("流入率が正しくありません(", flowrate, ")")
        sys.exit()
# ルール表の初期化
rule = [0 for i in range(R)]  # ルール表の作成
setrule(rule, RULE)           # ルール表をセット
# セルオートマトンへの初期値の読み込み
ca = [0 for i in range(N)]    # セルの並び
initca(ca)                    # 初期値読み込み

# 時間発展の計算
for t in range(1, MAXT):
    nextt(ca, rule)     # 次の時刻に更新
    if (t % flowrate) == 0:
         ca[N - 2] = 1  # 自動車の流入
    print("t=", t, "\t", end="")     
    putca(ca)           # caの状態の出力
# traffic.pyの終わり

