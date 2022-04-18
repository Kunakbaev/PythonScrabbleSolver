
import encodeWords
import os

# prepare words and meanings

WORDS_IN_SOLUTION = 50

currentDirectory = os.path.dirname(os.path.realpath(__file__))
# DLL_PATH = "C:\\Users\\tyrep\\Documents\\C++LibForPython\\Dll1\\x64\\Release\\Dll1.dll"
DLL_PATH = currentDirectory + "\\Dll1.dll"
RESULT_WORDS_FILE_PATH = currentDirectory + "\\resultWords.txt"
DICT_PATH = currentDirectory + "\\dict.txt"
print(currentDirectory)

meanings = []
wordsTree = {}

def loadEncodedNouns(words):
    with open(DICT_PATH, "w",
              encoding="utf-8") as f:
        for word in words:
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

def loadNouns():
    lines = []
    wordLines = []
    with open(currentDirectory + "\\meanings.txt", "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    with open(currentDirectory + "\\words.txt", "r", encoding="utf-8") as f:
        for line in f:
            wordLines.append(line)
    i = 0
    meaning = ""
    breakLine = "----------"
    words = []
    while i < len(lines):
        if lines[i][:-1] == breakLine:
            if i:
                meanings.append(meaning)
            meaning = ""
        else:
            meaning += lines[i][:-1]
        i += 1
    ind = 0
    i = 0
    temp = []
    badly = 0
    while i < len(wordLines):
        if wordLines[i][:-1] == breakLine:
            if i:
                ind += 1
                if len(temp) >= 2 and len(temp[1]) >= len(temp[0]) + 3:
                    print(temp[0], temp[1])
                    badly += 1
                temp = []
        else:
            word = wordLines[i][:-1]
            words.append(word)
            temp.append(word)
            v = wordsTree
            for ch in word:
                if ch not in v:
                    v[ch] = {}
                v = v[ch]
            v['ind'] = ind
        i += 1
    loadEncodedNouns(words)
    print(badly)


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


# help text (instruction)

helpWord = "Инструкция.\n" \
           "* Если вы не знакомы с правилами игры, то их легко можно найти онлайн.\n" \
           "* Слева расположенно игровое поле.\n" \
           "* На панель МОИ БУКВЫ можно кликнуть и ввести ваши буквы.\n" \
           "* Если вы хотите найти налучший способ поставить слово на доску, нажмите ПОДОБРАТЬ СЛОВО. \n" \
           "После некоторого времени вы увидите список слов и их стоимости. Чтобы посмотреть информацию о конкретном слове " \
           "кликните на него. Нажав на кнопку ПОСТАВИТЬ вы поставите слово на доску.\n" \
           "* Если вы хотите узнать, существует ли какое-то слово, введите его в поле ВАШЕ СЛОВО и нажмите enter.\n" \
           "* Если вы хотите поставить слово другого игрока, то введите это слово в поле ВАШЕ СЛОВО, затем выберите необходимую " \
           "ориентацию нажав на маленькую квадратную кнопку (H - слово ставится горизантально, V - слово " \
           "ставится вертикально). Затем кликните на ячейку на поле, с которой начинается слово." \
           "\n\nTODO: \n* Добавить множественные формы существительных\n" \
           "* Попробовать ускорить приложение с помощью многопоточности или изменения алгоритма\n" \
           "* Сделать код красивым\n" \
           "* Досмотреть сериал СВЕРХЪЕСТЕСТВЕННОЕ" \
           ""

