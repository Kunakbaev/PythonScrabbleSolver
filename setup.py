

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

meanings = []
wordsTree = {}

def loadNouns():
    # ww = "тѐлереда́кторы"
    # for i in range(len(ww)): print(i, ww[i])
    lines = []
    wordLines = []
    breakLine = "----------"
    with open("./meanings.txt", "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line)
    # correct = open("./correct.txt", "w", encoding="utf-8")
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
WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)


# help text (instruction)

helpWord = "Инструкция.\n" \
           "* Если вы не знакомы с правилами игры, то их легко можно найти онлайн.\n" \
           "* Слева расположенно игровое поле.\n" \
           "* На панель МОИ БУКВЫ можно кликнуть и ввести ваши буквы.\n" \
           "* Если вы хотите найти налучший способ поставить слово на доску, нажмите ПОДОБРАТЬ СЛОВО. \n" \
           "После некоторого времени вы увидите список слов и их стоимости. Чтобы посмотреть информацию о конкретном слове " \
           "кликните на него. Нажав на кнопку ПОСТАВИТЬ вы поставите слово на доску.\n" \
           "* Чтобы очистить ячейку очистите поле ввода слова и нажмите на ячейку.\n" \
           "* Если вы хотите узнать, существует ли какое-то слово, введите его в поле ВАШЕ СЛОВО и нажмите enter.\n" \
           "* Если вы хотите поставить слово другого игрока, то введите это слово в поле ВАШЕ СЛОВО, затем выберите необходимую " \
           "ориентацию нажав на маленькую квадратную кнопку (H - слово ставится горизантально, V - слово " \
           "ставится вертикально). Затем кликните на ячейку на поле, с которой начинается слово." \
           "\n\nTODO: \n* Добавить множественные формы существительных\n" \
           "* Попробовать ускорить приложение с помощью многопоточности или изменения алгоритма\n" \
           "* Сделать код красивым\n" \
           "* Досмотреть сериал СВЕРХЪЕСТЕСТВЕННОЕ" \
           ""

