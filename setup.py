
import encodeWords

# prepare words and meanings

WORDS_IN_SOLUTION = 50
DLL_PATH = "C:\\Users\\tyrep\\Documents\\C++LibForPython\\Dll1\\x64\\Release\\Dll1.dll"
RESULT_WORDS_FILE_PATH = "C:\\Users\\tyrep\\Documents\\ScrabbleSolver\\resultWords.txt"
DICT_PATH = "C:/Users/tyrep/Documents/ScrabbleSolver/dict.txt.txt"

meanings = []
wordsTree = {}
def loadMeanings(nouns):
    for i in range(len(nouns)):
        elem = nouns[i]
        word = elem['word']
        meaning = elem['meaning']
        v = wordsTree
        for ch in word:
            if ch not in v:
                v[ch] = {}
            v = v[ch]
        v['ind'] = i
        meanings.append(meaning)

def loadEncodedNouns(nouns):
    with open(DICT_PATH, "w",
              encoding="utf-8") as f:
        for i in range(len(nouns)):
            word = nouns[i]['word']
            if word.find(' ') != -1:
                continue
            w = ""
            isCorrect = True
            for ch in word:
                if (ch < 'а' or 'я' < ch) and ch != 'ё':
                    isCorrect = False
                    break
                w += encodeWords.rusToEn(ch)
            if not isCorrect:
                continue
            f.write(w)
            f.write('\n')

# window parametres

WINDOW_W = 1200
WINDOW_H = 650
WINDOW_PADDING = 8


# different colors

NORM = (.1922, .7686, .5529, 1)
DOUBLE_LETTER = (.68, .85, .9, 1)
TRIPLE_LETTER = (.1922, .3882, .6118, 1)
DOUBLE_WORD = (1, .6667, 0, 1)
TRIPLE_WORD = (.9059, .0941, .2157, 1)
CENTER = (1, .7529, .7961, 1)
WHITE = (1,1,1,1)
BLACK = (0,0,0,1)