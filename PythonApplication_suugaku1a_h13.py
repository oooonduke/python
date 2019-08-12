#センター試験数学ⅠＡ　平成１３年度
#Basic言語
'''
010 rem 元プログラム
100 INPUT "X=";X
110 INPUT "N=";N
120 Y=1
140 IF N-2*INT(N/2)=0 THEN GOTO 160
150 Y=Y*X
160 N=INT(N/2)
170 IF N=0 THEN GOTO 190
175 X=X*X
180 GOTO 140
190 PRINT "Y=";Y
200 END
'''

#プログラム作者注この問題はpow関数のコーディングを求めている。
#X ^ N = Y の形式で累乗を求める。
x = int(input("X= "))
n = abs(int(input("N= ")))
y = 1

while True:
    if(n-2*int(n/2) is not 0):
        y = int(y) * int(x)
    n = int(n/2)
    x = int(x) * int(x)
    if n == 0:
        break

print('Y= %d ' % y)
