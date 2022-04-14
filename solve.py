from ctypes import *
import encodeWords
from setup import WORDS_IN_SOLUTION, DLL_PATH, RESULT_WORDS_FILE_PATH, DICT_PATH

lib = CDLL(DLL_PATH)

class CNoun(Structure):
    _fields_ = [
        ('word', c_char_p),
        ('meaning', c_char_p),
        ('score', c_int),
        ('x', c_char_p),
        ('y', c_char_p),
        ('h', c_char_p)
    ]

class Word():
    def __init__(self, word, i, j, h, score, wordInd):
        self.word = word
        self.i = i
        self.j = j
        self.h = h
        self.score = score
        self.wordInd = wordInd

def matrix2Cmatrix(m):
    matrixType = c_char_p * 15
    matrix = matrixType()
    for i in range(15):
        str = ""
        for j in range(15):
            if m[i][j] != '':
                str += encodeWords.rusToEn(m[i][j])
            else:
                str += ' '
        matrix[i] = str.encode("utf-8")
    matrixC = cast(matrix, POINTER(c_char_p))
    return matrixC

def loadNounsToDll():
    print("loading nouns to dll")
    lib.loadWords.argtypes = [c_char_p]
    lib.loadWords(DICT_PATH.encode("utf-8"))

def solve(matrix, letters):
    # calling cpp function from dll lib

    myLetters = ""
    for ch in letters:
        myLetters += encodeWords.rusToEn(ch)
    matrixC = matrix2Cmatrix(matrix)
    lib.solve.argtypes = [POINTER(c_char_p), c_char_p, c_char_p, c_int]
    lib.solve.restypes = c_int
    size = lib.solve(matrixC, myLetters.encode("utf-8"), RESULT_WORDS_FILE_PATH.encode("utf-8"), WORDS_IN_SOLUTION)
    print(size, "words have been found")
    res = []
    lines = []
    with open(RESULT_WORDS_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    i = 0
    #print(lines)
    while i < len(lines):
        word = encodeWords.enWordToRus(lines[i][:-1])
        y = int(lines[i + 1][:-1])
        x = int(lines[i + 2][:-1])
        score = int(lines[i + 3][:-1])
        h = lines[i + 4][:-1]
        ind = lines[i + 5][:-1]
        w = Word(word, y, x, h, score, ind)
        #print(lines[i][:-1], word, x, y, score, h, ind)
        res.append(w)
        i += 6
    return res
