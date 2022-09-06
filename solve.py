
from setup import WORDS_IN_SOLUTION, GAME_W, wordsTree, letterCost, meanings


class Word():
    def __init__(self, word, i, j, h, score, wordInd):
        self.word = word
        self.i = i
        self.j = j
        self.h = h
        self.score = score
        self.wordInd = wordInd

res = []
count = {}
used = []

def isWord(word): # we want to check if word is in our dictionary and if it is we return it's meaning
    v = wordsTree
    for ch in word:
        if ch not in v:
            return -1
        v = v[ch]
    if 'ind' not in v:
        return -1
    return meanings[v['ind']]

def getMultiplicator(i, j): # we want to know which bonus this current cell gives to us
    # one digit = letter bonus, two digit = word bonus
    if (i == 0 and (j == 0 or j == GAME_W // 2 or j == GAME_W - 1)
    ) or (i == GAME_W // 2 and (j == 0 or j == GAME_W - 1)
    ) or (i == GAME_W - 1 and (j == 0 or j == GAME_W // 2 or j == GAME_W - 1)):
        return 33
    elif (i == j or (i == GAME_W - j - 1)) and abs(i - GAME_W // 2) >= 3:
        return 22
    elif i % 4 == 1 and j % 4 == 1:
        return 3
    elif (abs(i - GAME_W // 2) == 7 and (j % 8 == 3)) or (
            abs(i - GAME_W // 2) == 4 and (j % 7 == 0)) or (
            abs(i - GAME_W // 2) == 0 and (j % 8 == 3)) or (
            abs(i - GAME_W // 2) == 1 and abs(j - GAME_W // 2) == 1) or (
            abs(i - GAME_W // 2) == 5 and abs(j - GAME_W // 2) == 1) or (
            abs(i - GAME_W // 2) == 1 and abs(j - GAME_W // 2) == 5):
        return 2
    return 1


def dfs(matrix, i, j, v, word, score, isHor, isDouble=False, isTriple=False, hadContact=False, didPut=False): # main solving function
    global res, count
    if GAME_W <= j or GAME_W <= i:
        return
    for ch in v:
        if ch == 'ind':
            continue
        if ch not in letterCost:
            continue
        didModification = False
        hasBlank = False
        if matrix[i][j] == '':
            if ch not in count or not count[ch]:
                if '_' not in count or not count['_']:
                    continue
                else:
                    count['_'] -= 1
                    hasBlank = True
            if not hasBlank:
                count[ch] -= 1
                didModification = True
        elif matrix[i][j] != ch:
            continue

        hadContact = hadContact or matrix[i][j] == ch

        if (((i and matrix[i - 1][j] != '') or (i + 1 < GAME_W and matrix[i + 1][j] != '')) and matrix[i]
            [j] == '' and isHor) or \
                (((j and matrix[i][j - 1] != '') or (j + 1 < GAME_W and matrix[i][j + 1] != '')) and matrix[i]
                    [j] == '' and not isHor):
            isOk = False
            if isHor:
                w = ch
                for ii in range(i + 1, GAME_W, 1):
                    if matrix[ii][j] == '':
                        break
                    w += matrix[ii][j]
                for ii in range(i - 1, -1, -1):
                    if matrix[ii][j] == '':
                        break
                    w = matrix[ii][j] + w
                if isWord(w) != -1:
                    isOk = True
            else:
                w = ch
                for jj in range(j + 1, GAME_W, 1):
                    if matrix[i][jj] == '':
                        break
                    w += matrix[i][jj]
                for jj in range(j - 1, -1, -1):
                    if matrix[i][jj] == '':
                        break
                    w = matrix[i][jj] + w
                if isWord(w) != -1:
                    isOk = True
            if not isOk:
                if didModification:
                    count[ch] += 1
                continue
            else:
                hadContact = True

        cost = letterCost[ch]
        if hasBlank:
            cost = 2
        multiplicator = getMultiplicator(i, j)
        isDouble = isDouble or (multiplicator == 22 and matrix[i][j] == '')
        isTriple = isTriple or (multiplicator == 33 and matrix[i][j] == '')
        if multiplicator == 2 and matrix[i][j] == '':
            cost *= 2
        if multiplicator == 3 and matrix[i][j] == '':
            cost *= 3
        if 'ind' in v[ch] and (hadContact or (isHor and j - len(word) + 1 <= 7 <= j and i == 7) or
                               (not isHor and i - len(word) + 1 <= 7 <= i and j == 7)) and \
                didPut and not v[ch]['ind'] in used:
            flag = True
            val = j - len(word + ch) if isHor else i - len(word + ch)
            if val + 1 and matrix[i][val] != '' and isHor:
                flag = False
            if val + 1 and matrix[val][j] != '' and not isHor:
                flag = False
            if j + 1 < GAME_W and matrix[i][j + 1] != '' and isHor:
                flag = False
            if i + 1 < GAME_W and matrix[i + 1][j] != '' and not isHor:
                flag = False
            if flag:
                co = score + cost
                if isDouble:
                    co *= 2
                if isTriple:
                    co *= 3
                if isHor:
                    res.append(Word(word + ch, i, val + 1, 'h', co, v[ch]['ind']))
                else:
                    res.append(Word(word + ch, val + 1, j, 'v', co, v[ch]['ind']))
        if isHor:
            dfs(matrix, i, j + 1, v[ch], word + ch, score + cost, True, isDouble, isTriple,
                hadContact, didPut or matrix[i][j] == '')
        else:
            dfs(matrix, i + 1, j, v[ch], word + ch, score + cost, False, isDouble, isTriple,
                hadContact, didPut or matrix[i][j] == '')
        if didModification:
            count[ch] += 1
        if hasBlank:
            count['_'] += 1

# we try to put all possible words from each cell in every possible orientation
def solve(matrix, letters):
    global res, count
    res = []
    count = {}
    root = wordsTree
    for ch in letters:
        if ch not in count:
            count[ch] = 1
        else:
            count[ch] += 1
    for i in range(GAME_W):
        for j in range(GAME_W):
            # we try to put words horizontally
            dfs(matrix, i, j, root, "", 0, True)
            # we try to put words vertically
            dfs(matrix, i, j, root, "", 0, False)
    # we want words with biggest score
    res = sorted(res, key=lambda x: -x.score)
    size = min(len(res), WORDS_IN_SOLUTION)
    res = res[:size]
    return res
