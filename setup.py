
from win32api import GetSystemMetrics

# here all consts are prepared

# prepare words and meanings

WORDS_IN_SOLUTION = 50

letterCost = {
    'а': 1,
    'б': 3,
    'в': 1,
    'г': 3,
    'д': 2,
    'е': 1,
    'ё': 3,
    'ж': 5,
    'з': 5,
    'и': 1,
    'й': 4,
    'к': 2,
    'л': 2,
    'м': 2,
    'н': 1,
    'о': 1,
    'п': 2,
    'р': 1,
    'с': 1,
    'т': 1,
    'у': 2,
    'ф': 10,
    'х': 5,
    'ц': 5,
    'ч': 5,
    'ш': 8,
    'щ': 10,
    'ъ': 10,
    'ы': 4,
    'ь': 3,
    'э': 8,
    'ю': 8,
    'я': 3,
    '_': 2
}

letterCount = {
    'а': 8,
    'б': 2,
    'в': 4,
    'г': 2,
    'д': 4,
    'е': 8,
    'ё': 1,
    'ж': 1,
    'з': 2,
    'и': 5,
    'й': 1,
    'к': 4,
    'л': 4,
    'м': 3,
    'н': 5,
    'о': 10,
    'п': 4,
    'р': 5,
    'с': 5,
    'т': 5,
    'у': 4,
    'ф': 1,
    'х': 1,
    'ц': 1,
    'ч': 1,
    'ш': 1,
    'щ': 1,
    'ъ': 1,
    'ы': 2,
    'ь': 2,
    'э': 1,
    'ю': 1,
    'я': 2,
    '_': 2
}

meanings = []
wordsTree = {}

def loadNouns():
    lines = []
    wordLines = []
    breakLine = "----------"
    with open("./meanings.txt", "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    with open("./correct.txt", "r", encoding="utf-8") as f:
        for line in f:
            wordLines.append(line)
    i = 0
    meaning = ""
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
    while i < len(wordLines):
        if wordLines[i][:-1] == breakLine:
            if i:
                ind += 1
        else:
            word = wordLines[i][:-1]
            okey = True
            for ch in word:
                if (ch < 'а' or 'я' < ch) and ch != 'ё':
                    okey = False
                    break
            if okey:
                words.append(word)
                v = wordsTree
                for ch in word:
                    if ch not in v:
                        v[ch] = {}
                    v = v[ch]
                v['ind'] = ind
        i += 1
    print("Words have been loaded : ", len(words))


# window parametres

WINDOW_W = GetSystemMetrics(0)
WINDOW_H = GetSystemMetrics(1)
# WINDOW_W = 1200
# WINDOW_H = 700
WINDOW_PADDING = 10


# different colors

NORM = (.1922, .7686, .5529, 1)
DOUBLE_LETTER = (.68, .85, .9, 1)
TRIPLE_LETTER = (.1922, .3882, .6118, 1)
DOUBLE_WORD = (1, .6667, 0, 1)
TRIPLE_WORD = (.9059, .0941, .2157, 1)
CENTER = (1, .7529, .7961, 1)
WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)

# game parametres

# it is should be const, because in rules board's size is always 15
GAME_W = 15

LETTERS_PER_MOVE = 7

# help text (instruction)

helpWord = "Инструкция.\n" \
           "* Краткий экскурс в правила. Необходимо составлять слова из букв вашего набора и ставить их на доску. За каждое слово вы получаете" \
           " очки. Также есть различные бонусы. Голубой = буква х2, синий = буква х3, жёлтый = слово х2, красный = слово х3. " \
           "Слова надо ставить как в кроссвордах (верт. или гориз.), т.к. чтобы слово ещё не было поставленно ни одним из игроков и оно соприк" \
           "асалось с каким-то раннее поставленным словом (за искл. 1ого хода). Побеждает игрок с наибольшим числом очков.\n" \
           "* Слева расположенно игровое поле.\n" \
           "* Если вы хотите узнать, существует ли какое-то слово, введите его в поле ВАШЕ СЛОВО и нажмите enter.\n" \
           "* Если вы хотите поставить слово, то введите это слово в поле ВАШЕ СЛОВО, затем выберите необходимую " \
           "ориентацию нажав на маленькую квадратную кнопку (H - слово ставится горизантально, V - слово " \
           "ставится вертикально). Затем кликните на ячейку на поле, с которой начинается слово и оно поставится." \
           "\n\nTODO: \n* Добавить слова со странными падежами (местный и разделительный)\n" \
           "* Попробовать ускорить приложение с помощью многопоточности или изменения алгоритма (хотя и так быстро работает)\n" \
           "* Сделать код красивым\n" \
           "* Досмотреть тетрадь смерти" \
           ""

