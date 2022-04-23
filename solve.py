

from setup import WORDS_IN_SOLUTION, wordsTree, letterCost, meanings


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

def isWord(word):
    v = wordsTree
    for ch in word:
        if ch not in v:
            return -1
        v = v[ch]
    if 'ind' not in v:
        return -1
    # print(word, v['ind'], meanings[v['ind']])
    return meanings[v['ind']]

def getMultiplicator(i, j):
    if (i == 0 and (j == 0 or j == 15 // 2 or j == 15 - 1)
    ) or (i == 15 // 2 and (j == 0 or j == 15 - 1)
    ) or (i == 15 - 1 and (j == 0 or j == 15 // 2 or j == 15 - 1)):
        return 33
    elif (i == j or (i == 15 - j - 1)) and abs(i - 15 // 2) >= 3:
        return 22
    elif i % 4 == 1 and j % 4 == 1:
        return 3
    elif (abs(i - 15 // 2) == 7 and (j % 8 == 3)) or (
            abs(i - 15 // 2) == 4 and (j % 7 == 0)) or (
            abs(i - 15 // 2) == 0 and (j % 8 == 3)) or (
            abs(i - 15 // 2) == 1 and abs(j - 15 // 2) == 1) or (
            abs(i - 15 // 2) == 5 and abs(j - 15 // 2) == 1) or (
            abs(i - 15 // 2) == 1 and abs(j - 15 // 2) == 5):
        return 2
    return 1


def dfs(matrix, i, j, v, word, score, isHor, isDouble=False, isTriple=False, hadContact=False, didPut=False):
    global res, count
    if 15 <= j or 15 <= i:
        return
    for ch in v:
        if ch == 'ind':
            continue
        if ch not in letterCost:
            # print(word, "|", ch)
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

        if (((i and matrix[i - 1][j] != '') or (i + 1 < 15 and matrix[i + 1][j] != '')) and matrix[i][j] == '' and isHor) or \
                (((j and matrix[i][j - 1] != '') or (j + 1 < 15 and matrix[i][j + 1] != '')) and matrix[i][j] == '' and not isHor):
            isOk = False
            if isHor:
                # ('H', word, i, j)
                w = ch
                for ii in range(i + 1, 15, 1):
                    if matrix[ii][j] == ' ':
                        break
                    w += matrix[ii][j]
                for ii in range(i - 1, -1, -1):
                    if matrix[ii][j] == ' ':
                        break
                    w = matrix[ii][j] + w
                if isWord(w) != -1:
                    # print('H', word, " ch : ", ch, "|", i, j)
                    # print(w, " | ", isWord(w))
                    isOk = True
            else:
                # print('V', word, i, j)
                w = ch
                for jj in range(j + 1, 15, 1):
                    if matrix[i][jj] == ' ':
                        break
                    w += matrix[i][jj]
                for jj in range(j - 1, -1, -1):
                    if matrix[i][jj] == ' ':
                        break
                    w = w + matrix[i][jj]
                if isWord(w) != -1:
                    # print('V', word, " ch : ", ch, "|", i, j)
                    # print(w, " | ", isWord(w))
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
        # print(word + ch, v['ind'] if 'ind' in v else None, hadContact, isHor, i, j - len(word) + 1)
        if 'ind' in v[ch] and (hadContact or (isHor and j - len(word) + 1 <= 7 <= j and i == 7) or
                               (not isHor and i - len(word) + 1 <= 7 <= i and j == 7)) and \
                didPut and not v[ch]['ind'] in used:
            flag = True
            val = j - len(word + ch) if isHor else i - len(word + ch)
            if val + 1 and matrix[i][val] != '' and isHor:
                flag = False
            if val + 1 and matrix[val][j] != '' and not isHor:
                flag = False
            if j + 1 < 15 and matrix[i][j + 1] != '' and isHor:
                flag = False
            if i + 1 < 15 and matrix[i + 1][j] != '' and not isHor:
                flag = False
            if flag:
                co = score + cost
                if isDouble:
                    co *= 2
                if isTriple:
                    co *= 3
                # print(word + ch, i, j - len(word + ch) + 1, "j : ", j, len(word), hadContact)
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

def solve(matrix, letters):
    # try to put word horizontally
    global res, count
    res = []
    count = {}
    root = wordsTree
    for ch in letters:
        if ch not in count:
            count[ch] = 1
        else:
            count[ch] += 1
    # print(letters)
    # for i in range(15):
    #     print(*matrix[i], sep=', ')
    for i in range(15):
        for j in range(15):
            dfs(matrix, i, j, root, "", 0, True)
            dfs(matrix, i, j, root, "", 0, False)
    res = sorted(res, key=lambda x: -x.score)
    # print(len(res))
    size = min(len(res), WORDS_IN_SOLUTION)
    res = res[:size]
    return res


