import random

import setup
from app import MainApp
import solve
import copy

class Game:
    def __init__(self):
        self.app = MainApp()
        self.w = setup.GAME_W
        self.h = setup.GAME_W
        self.myScore = self.computerScore = 0
        self.sack = []
        for ch, cnt in setup.letterCount.items():
            for i in range(0, cnt):
                self.sack.append(ch)
        self.myLetters = self.takeLettersFromSack("")
        self.computerLetters = self.takeLettersFromSack("")
        self.app.myLetters = self.myLetters
        print(self.myLetters, self.computerLetters)

    def takeLettersFromSack(self, word):
        res = word
        need = setup.LETTERS_PER_MOVE - len(word)
        print("sack len : ", len(self.sack))
        if not len(self.sack):
            self.app.meaningPanel.text = "Мешок букв опустел, вероятно поле тоже заполнено, идите отдохните."
        if len(self.sack) <= need:
            for ch in self.sack:
                res += ch
            self.sack = []
            return res
        for i in range(need):
            j = random.randint(0, len(self.sack) - 1)
            res += self.sack[j]
            self.sack.remove(self.sack[j])
        return res

    def getWordScore(self, obj):
        matrix = self.app.matrix
        res = 0
        count = {}
        for ch in self.myLetters:
            if ch not in count:
                count[ch] = 0
            count[ch] += 1
        isDouble = isTriple = False
        if obj.h == 'h':
            for j in range(obj.j, obj.j + len(obj.word), 1):
                ch = obj.word[j - obj.j]
                need = self.app.matrix[obj.i][j]
                cost = setup.letterCost[ch]
                print("cost :", cost, "res :", res)
                if need != '':
                    res += cost
                    continue
                if ch not in count or not count[ch]:
                    cost = setup.letterCost['_']
                multiplicator = solve.getMultiplicator(obj.i, j)
                print("multiplicator : ", multiplicator)
                isDouble = isDouble or (multiplicator == 22 and matrix[obj.i][j] == '')
                isTriple = isTriple or (multiplicator == 33 and matrix[obj.i][j] == '')
                if multiplicator == 2:
                    cost *= 2
                if multiplicator == 3:
                    cost *= 3
                res += cost
        else:
            for i in range(obj.i, obj.i + len(obj.word), 1):
                ch = obj.word[i - obj.i]
                need = self.app.matrix[i][obj.j]
                cost = setup.letterCost[ch]
                if need != '':
                    res += cost
                    continue
                if ch not in count or not count[ch]:
                    cost = setup.letterCost['_']
                multiplicator = solve.getMultiplicator(i, obj.j)
                isDouble = isDouble or (multiplicator == 22 and matrix[i][obj.j] == '')
                isTriple = isTriple or (multiplicator == 33 and matrix[i][obj.j] == '')
                if multiplicator == 2:
                    cost *= 2
                if multiplicator == 3:
                    cost *= 3
                res += cost
        if isDouble:
            res *= 2
        if isTriple:
            res *= 3
        return res

    def isGoodPlace(self, obj):
        ind = solve.isWord(obj.word)
        if ind == -1 or ind in solve.used:
            return False
        count = {}
        for ch in self.myLetters:
            if ch not in count:
                count[ch] = 0
            count[ch] += 1
        hadContact = False
        hadEmpty = False
        matrix = self.app.matrix
        if obj.h == 'h':
            print("horizontal")
            if (obj.j and matrix[obj.i][obj.j - 1] != '') or \
                    (obj.j + len(obj.word) < setup.GAME_W and matrix[obj.i][obj.j + len(obj.word)] != ''):
                return False
            for j in range(obj.j, obj.j + len(obj.word), 1):
                ch = obj.word[j - obj.j]
                need = self.app.matrix[obj.i][j]
                hasBlank = False
                if need == '':
                    hadEmpty = True
                    if ch not in count or not count[ch]:
                        if '_' not in count or not count['_']:
                            return False
                        else:
                            count['_'] -= 1
                            hasBlank = True
                    if not hasBlank:
                        count[ch] -= 1
                elif need != ch:
                    return False
                print("I have all letters")
                hadContact = hadContact or ch == need
                if (((obj.i and matrix[obj.i - 1][j] != '') or (obj.i + 1 < setup.GAME_W and
                                                                matrix[obj.i + 1][j] != '')) and matrix[obj.i][j] == ''):
                    isOk = False
                    w = ch
                    for ii in range(obj.i + 1, setup.GAME_W, 1):
                        if matrix[ii][j] == '':
                            break
                        w += matrix[ii][j]
                    for ii in range(obj.i - 1, -1, -1):
                        if matrix[ii][j] == '':
                            break
                        w = matrix[ii][j] + w
                    if solve.isWord(w) != -1:
                        isOk = True
                    if not isOk:
                        return False
                    hadContact = True
        else:
            print("vertical")
            if (obj.i and matrix[obj.i - 1][obj.j] != '') or \
                    (obj.i + len(obj.word) < setup.GAME_W and matrix[obj.i + len(obj.word)][obj.j] != ''):
                return False
            for i in range(obj.i, obj.i + len(obj.word), 1):
                ch = obj.word[i - obj.i]
                need = self.app.matrix[i][obj.j]
                hasBlank = False
                if need == '':
                    hadEmpty = True
                    if ch not in count or not count[ch]:
                        if '_' not in count or not count['_']:
                            return False
                        else:
                            count['_'] -= 1
                            hasBlank = True
                    if not hasBlank:
                        count[ch] -= 1
                elif need != ch:
                    return False
                print("I have all letters")
                hadContact = hadContact or ch == need
                if (((obj.j and matrix[i][obj.j - 1] != '') or (obj.j + 1 < setup.GAME_W
                                                                and matrix[i][obj.j + 1] != '')) and matrix[i][obj.j] == ''):
                    isOk = False
                    w = ch
                    for jj in range(obj.j + 1, setup.GAME_W, 1):
                        if matrix[i][jj] == '':
                            break
                        w += matrix[i][jj]
                    for jj in range(obj.j - 1, -1, -1):
                        if matrix[i][jj] == '':
                            break
                        w = matrix[i][jj] + w
                    if solve.isWord(w) != -1:
                        isOk = True
                    if not isOk:
                        return False
                    hadContact = True
        print(hadContact, hadEmpty)
        flag = ((obj.h == 'h' and obj.j <= 7 <= obj.j + len(obj.word) - 1 and obj.i == 7) or
                (obj.h != 'h' and obj.i <= 7 <= obj.i + len(obj.word) - 1 and obj.j == 7))
        if (not hadContact and not flag) or not hadEmpty:
            return False
        solve.used.append(ind)

        myScore = self.getWordScore(obj)
        print("myScore : ", myScore)
        self.myScore += myScore
        self.app.myScoreLabel.text = "Мои очки : " + str(self.myScore)

        self.myLetters = ""
        for ch, cnt in count.items():
            for i in range(cnt):
                self.myLetters += ch
        print(self.myLetters)
        self.myLetters = self.takeLettersFromSack(self.myLetters)
        print("myLetters : ", self.myLetters)
        self.app.myLettersLabel.text = "Мои буквы : " + self.myLetters
        return True

    def computerMove(self):
        print('solving...')
        solutions = solve.solve(copy.deepcopy(self.app.matrix), self.computerLetters)
        if not len(solutions):
            self.app.meaningPanel.text = "Компьютер дурачок, не смог найти валидный ход, поэтому он пропустит ход."
            for ch in self.myLetters:
                self.sack.append(ch)
                self.computerLetters = ""
                self.computerLetters = self.takeLettersFromSack(self.computerLetters)
                print("computerLetters : ", self.computerLetters)
            return
        self.app.meaningPanel.text = ""
        print(solutions[0].word, "computer's score :", solutions[0].score)
        self.computerScore += solutions[0].score
        self.app.computerScoreLabel.text = "Очки оппонента : " + str(self.computerScore)
        count = {}
        for ch in self.computerLetters:
            if ch not in count:
                count[ch] = 0
            count[ch] += 1
        obj = solutions[0]
        if obj.h == 'h':
            for j in range(obj.j, obj.j + len(obj.word), 1):
                ch = obj.word[j - obj.j]
                need = self.app.matrix[obj.i][j]
                if need != '':
                    continue
                if ch not in count or not count[ch]:
                    count['_'] -= 1
                else:
                    count[ch] -= 1
        else:
            for i in range(obj.i, obj.i + len(obj.word), 1):
                ch = obj.word[i - obj.i]
                need = self.app.matrix[i][obj.j]
                if need != '':
                    continue
                if ch not in count or not count[ch]:
                    count['_'] -= 1
                else:
                    count[ch] -= 1
        self.computerLetters = ""
        for ch, cnt in count.items():
            for i in range(cnt):
                self.computerLetters += ch
        self.computerLetters = self.takeLettersFromSack(self.computerLetters)
        print("computerLetters : ", self.computerLetters)
        self.app.putWord(solutions[0])

    def skipMove(self):
        print("skip move")
        for ch in self.myLetters:
            self.sack.append(ch)
        self.myLetters = ""
        self.myLetters = self.takeLettersFromSack(self.myLetters)
        print("myLetters : ", self.myLetters)
        self.app.myLettersLabel.text = "Мои буквы : " + self.myLetters
        self.computerMove()

