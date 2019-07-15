
import axelrod as axl

players = (axl.Cooperator(), axl.Random())
#players = ( axl.Cooperator(), axl.Alternator())
match = axl.Match(players, turns=1)
results = match.play()
print(results)

listx = list(results[0])

if len(listx) == 2:
    akokuw = listx[0]
    bkokuw = listx[1]
    akoku = str(akokuw).strip()
    bkoku = str(bkokuw).strip()
#print(str(akoku) == 'C')
#print(bkoku)

scores = match.scores()
scoresx = list(scores[0])

if len(scoresx) == 2:
    ascore = scoresx[0]
    bscore = scoresx[1]
    if akoku == 'C' and bkoku == 'C':  #協力協力
        ascore = 10
        bscore = 10
    elif  akoku == 'C' and bkoku == 'D':  #協力裏切り
        ascore = 1
        bscore = 11
    elif  akoku == 'D' and bkoku == 'C':  #裏切り協力
        ascore = 11
        bscore = 1
    elif  akoku == 'D' and bkoku == 'D':  #裏切り裏切り
        ascore = 2
        bscore = 2
    else:
        print("未定義")

print("Ａ国の得点:" + str(ascore))
print("Ｂ国の得点:" + str(bscore))


#print(scores)
