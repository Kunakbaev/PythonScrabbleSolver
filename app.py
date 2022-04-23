from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import copy

from setup import *
import solve

Window.size = (WINDOW_W, WINDOW_H)

class MainApp(App):
    def build(self):
        self.ind = -1
        self.showedButton = None
        self.title = 'Scrabble solver'
        self.size = (WINDOW_W, WINDOW_H)
        self.window_padding = WINDOW_PADDING
        self.tiles = []
        self.matrix = []
        self.w = 15
        self.h = 15
        self.isInput = False
        layout = FloatLayout()
        buttonW = (self.size[1] - self.window_padding * 2) / self.w
        buttonH = (self.size[1] - self.window_padding * 2) / self.h
        self.buttonW = buttonW
        self.buttonH = buttonH
        for i in range(self.h):
            self.tiles.append([])
            self.matrix.append([])
            for j in range(self.w):
                self.matrix[i].append('')
                offset = 2
                col = NORM
                if i == self.h // 2 and j == self.w // 2:
                    col = CENTER
                elif (i == 0 and (j == 0 or j == self.w // 2 or j == self.w - 1)
                ) or (i == self.h // 2 and (j == 0 or j == self.w - 1)
                ) or (i == self.h - 1 and (j == 0 or j == self.w // 2 or j == self.w - 1)):
                    col = TRIPLE_WORD
                elif (i == j or (i == self.w - j - 1)) and abs(i - self.h // 2) >= 3:
                    col = DOUBLE_WORD
                elif i % 4 == 1 and j % 4 == 1:
                    col = TRIPLE_LETTER
                elif (abs(i - self.h // 2) == 7 and (j % 8 == 3)) or (
                    abs(i - self.h // 2) == 4 and (j % 7 == 0)) or (
                    abs(i - self.h // 2) == 0 and (j % 8 == 3)) or (
                    abs(i - self.h // 2) == 1 and abs(j - self.w // 2) == 1) or (
                    abs(i - self.h // 2) == 5 and abs(j - self.w // 2) == 1) or (
                    abs(i - self.h // 2) == 1 and abs(j - self.w // 2) == 5):
                    col = DOUBLE_LETTER
                btn = Button(text='',
                 background_normal='',
                 background_down='',
                 background_color=col,
                 font_size=30, bold=True,
                 pos=(self.window_padding + j * buttonW + offset,
                      self.size[1] - self.window_padding - (i + 1) * buttonH + offset),
                 size_hint=((buttonW - 2 * offset) / self.size[0], (buttonH - 2 * offset) / self.size[1])
                )
                btn.ids['i'] = i
                btn.ids['j'] = j
                btn.bind(on_press=self.tile_on_press)
                self.tiles[i].append(btn)
                layout.add_widget(btn)
        #layout.add_widget(label)
        self.layout = layout
        self.addOtherButtons()
        return layout

    def addOtherButtons(self):
        h = (self.size[1] - self.window_padding * 6) / 12
        w = (self.size[0] - self.window_padding * 4 - self.buttonW * self.w) / 2
        self.putButton = Button(text='Поставить',
          background_normal='',
          background_down='',
          background_color=WHITE,
          color=BLACK,
          font_size=20, bold=True,
          pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3, self.size[1] - 2 * h - 2 * self.window_padding),
          size_hint=((4 * w / 3 - h - self.window_padding) / self.size[0], h / self.size[1])
        )
        self.changeOrientation = Button(text='H',
        background_normal='',
        background_down='',
        background_color=WHITE,
        color=BLACK,
        font_size=20, bold=True,
        pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3 + 4 * w / 3 - h,
             self.size[1] - 2 * h - 2 * self.window_padding),
        size_hint=(h / self.size[0], h / self.size[1])
        )
        self.helpLabel = TextInput(text=helpWord,
        background_disabled_normal="", multiline=True,
        background_color=WHITE, foreground_color=BLACK,
        font_size=17, pos=(0, 0), disabled=True,
        size_hint=(1, None), height=800
        )
        self.helpLabelView = ScrollView(do_scroll_x=False, do_scroll_y=True,
        pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3, self.window_padding),
        size_hint=((4 * w / 3) / self.size[0], 4 * h / self.size[1])
        )
        self.helpLabelView.add_widget(self.helpLabel)
        self.myLetters = "тыкласс"
        self.myLettersLabel = Button(text='Мои буквы : ' + self.myLetters,
           background_normal='',
           background_down='',
           background_color=WHITE,
           color=BLACK,
           font_size=20, bold=True,
           pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3, self.size[1] - h - self.window_padding),
           size_hint=((4 * w / 3) / self.size[0], h / self.size[1])
        )
        self.meaningInput = TextInput(multiline=False, size_hint=((4 * w / 3) / self.size[0], h / self.size[1]),
                  pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3,
                       self.size[1] - 3 * h - 3 * self.window_padding),
                    background_color=WHITE, foreground_color=BLACK, hint_text="Ваше слово : ",
                  font_size=30)
        self.meaningPanel = TextInput(multiline=True, size_hint=((4 * w / 3) / self.size[0], None),
                height=800, font_size=18,
                pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3,
                       self.size[1] - 8 * h - 4 * self.window_padding),
                disabled=True, background_disabled_normal="", hint_text="Его значение",
                background_color=WHITE, foreground_color=BLACK
                )
        self.meaningPanelView = ScrollView(size_hint=(1, 5 * h / self.size[1]),
              pos=(self.window_padding * 3 + self.buttonW * self.w + w * 2 / 3,
                   self.size[1] - 8 * h - 4 * self.window_padding),
              do_scroll_x=False, do_scroll_y=True
              )
        self.meaningPanelView.add_widget(self.meaningPanel)
        self.lettersInput = None
        self.myLettersLabel.bind(on_press=self.changeMyLetters)
        self.putButton.bind(on_press=self.putSolution)
        self.changeOrientation.bind(on_press=self.changeOrientationFunc)
        self.meaningInput.bind(on_text_validate=self.showMeaning)
        self.layout.add_widget(self.myLettersLabel)
        self.layout.add_widget(self.putButton)
        self.layout.add_widget(self.changeOrientation)
        self.layout.add_widget(self.helpLabelView)
        self.layout.add_widget(self.meaningInput)
        self.layout.add_widget(self.meaningPanelView)
        self.addWordsPanel()

    def addWordsPanel(self):
        w = (self.size[0] - self.window_padding * 4 - self.w * self.buttonW) / 3
        h = ((self.size[1] - self.window_padding * 5) * 2)
        print(h, h / 10000)
        self.solveButton = Button(text='Подобрать\nслово',
          background_normal='',
          background_down='',
          background_color=WHITE,
          color=BLACK,
          font_size=20, bold=True,
          size_hint=(1, None), height=50
          )
        self.solveButton.bind(on_press=self.solve)
        self.noWordsPanel = Button(text='Решений нет',
         background_normal='',
         background_down='',
         background_color=WHITE,
         color=BLACK,
         font_size=23, bold=True,
         pos=(0, 0),
         size_hint=(1, None), height=100
        )
        self.wordsPanel = BoxLayout(orientation='vertical', size_hint=(1, None), height=50, spacing=5)
        view = ScrollView(size_hint=(w / self.size[0], h / self.size[1]),
                          pos=(self.window_padding * 2 + self.buttonW * self.w, self.size[1] - h - self.window_padding),
                          do_scroll_x=False, do_scroll_y=True)
        self.wordsPanel.add_widget(self.solveButton)
        view.add_widget(self.wordsPanel)
        self.viewWordsPanel = view
        self.layout.add_widget(view)

    def getMultiplicator(self, i, j):
        if (i == 0 and (j == 0 or j == self.w // 2 or j == self.w - 1)
                      ) or (i == self.h // 2 and (j == 0 or j == self.w - 1)
                            ) or (i == self.h - 1 and (j == 0 or j == self.w // 2 or j == self.w - 1)):
                return TRIPLE_WORD
        elif (i == j or (i == self.w - j - 1)) and abs(i - self.h // 2) >= 3: return DOUBLE_WORD
        elif i % 4 == 1 and j % 4 == 1: return TRIPLE_LETTER
        elif (abs(i - self.h // 2) == 7 and (j % 8 == 3)) or (
        abs(i - self.h // 2) == 4 and (j % 7 == 0)) or (
         abs(i - self.h // 2) == 0 and (j % 8 == 3)) or (
         abs(i - self.h // 2) == 1 and abs(j - self.w // 2) == 1) or (
         abs(i - self.h // 2) == 5 and abs(j - self.w // 2) == 1) or (
         abs(i - self.h // 2) == 1 and abs(j - self.w // 2) == 5): return DOUBLE_LETTER
        return NORM

    def putWord(self, obj):
        solve.used.append(obj.wordInd)
        if obj.h == 'h':
            for j in range(obj.j, obj.j + len(obj.word)):
                self.tiles[obj.i][j].text = obj.word[j - obj.j]
                self.matrix[obj.i][j] = obj.word[j - obj.j]
                self.tiles[obj.i][j].color = WHITE
        else:
            for i in range(obj.i, obj.i + len(obj.word)):
                self.tiles[i][obj.j].text = obj.word[i - obj.i]
                self.matrix[i][obj.j] = obj.word[i - obj.i]
                self.tiles[i][obj.j].color = WHITE

    def putSolution(self, instance):
        if self.ind == -1:
            return
        children = self.wordsPanel.children.copy()
        for elem in children:
            self.wordsPanel.remove_widget(elem)
        self.wordsPanel.add_widget(self.solveButton)
        self.wordsPanel.height = 50
        obj = self.solutions[self.ind]
        self.putWord(obj)

        self.ind = -1
        self.solutions = []

    def showSolution(self):
        if self.ind == -1:
            return

        obj = self.solutions[self.ind]
        obj.text = obj.word
        self.meaningInput.text = obj.word
        self.showMeaning(obj)
        if obj.h == 'h':
            for j in range(obj.j, obj.j + len(obj.word)):
                self.tiles[obj.i][j].text = obj.word[j - obj.j]
                self.tiles[obj.i][j].color = BLACK
        else:
            for i in range(obj.i, obj.i + len(obj.word)):
                self.tiles[i][obj.j].text = obj.word[i - obj.i]
                self.tiles[i][obj.j].color = BLACK

    def showSolutionFromList(self, instance):
        print("show solution from list")
        if self.ind != -1:
            self.showedButton.background_color = WHITE
            self.showedButton.color = BLACK

            obj = self.solutions[self.ind]
            if obj.h == 'h':
                for j in range(obj.j, obj.j + len(obj.word)):
                    self.tiles[obj.i][j].text = self.matrix[obj.i][j]
                    self.tiles[obj.i][j].color = WHITE
            else:
                for i in range(obj.i, obj.i + len(obj.word)):
                    self.tiles[i][obj.j].text = self.matrix[i][obj.j]
                    self.tiles[i][obj.j].color = WHITE
        instance.background_color = BLACK
        instance.color = WHITE
        self.showedButton = instance
        self.ind = instance.ids['btn ind']
        self.showSolution()

    def addWordsToPanel(self):
        h = self.size[1] - self.window_padding * 2
        w = self.viewWordsPanel.size_hint[0] * self.size[0]
        self.wordsPanel.height = (h / 10) * len(self.solutions)
        children = self.wordsPanel.children.copy()
        for elem in children: self.wordsPanel.remove_widget(elem)
        for i in range(len(self.solutions)):
            elem = self.solutions[i]
            word = elem.word
            btn = Button(text=word + ' cost : ' + str(elem.score),
             background_normal='',
             background_down='',
             background_color=WHITE if i else BLACK,
             color=BLACK if i else WHITE, font_size=18, bold=True, size_hint=(1, 1)
             )
            if not i:
                self.showedButton = btn
            btn.ids['btn ind'] = i
            btn.bind(on_press=self.showSolutionFromList)
            self.wordsPanel.add_widget(btn)

    def solve(self, instance):
        print('solving...')
        self.solutions = []
        self.solutions = solve.solve(copy.deepcopy(self.matrix), self.myLetters)
        if not len(self.solutions):
            children = self.wordsPanel.children.copy()
            for elem in children:
                self.wordsPanel.remove_widget(elem)
            self.wordsPanel.add_widget(self.solveButton)
            self.wordsPanel.add_widget(self.noWordsPanel)
            self.wordsPanel.height = 155
            return
        # self.solutions = sorted(self.solutions, key=lambda boom: -boom.score)
        # self.solutions = self.solutions[:WORDS_IN_SOLUTION]
        # for elem in self.solutions:
        #     print(elem.word)
        self.ind = 0
        self.showSolution()
        self.addWordsToPanel()

    def tile_on_press(self, instance):
        i = instance.ids['i']
        j = instance.ids['j']
        text = self.meaningInput.text
        if len(text) == 0:
            # print("cleaning")
            self.matrix[i][j] = ''
            self.tiles[i][j].text = ''
            return
        h = 'h' if self.changeOrientation.text == 'H' else 'v'
        if h == 'h':
            if self.w <= j + len(text) - 1:
                return
        else:
            if self.h <= i + len(text) - 1:
                return
        word = solve.Word(text, i, j, h, 0, 0)
        self.putWord(word)

    def changeOrientationFunc(self, instance):
        instance.text = 'V' if instance.text == 'H' else 'H'

    def showMeaning(self, value):
        self.meaningPanel.text = ""
        word = value.text
        for ch in word:
            if (ch < 'а' or 'я' < ch) and ch != 'ё':
                self.meaningPanel.text += "Слово должно состоять только из русских букв."
                return
        meaning = solve.isWord(word)
        if meaning == -1:
            self.meaningPanel.text += "Такого слова нет."
            return
        lines = len(meaning) / 20 + 10
        #print(meaning)
        self.meaningPanel.height = self.meaningPanel.line_height * lines
        self.meaningPanel.text += meaning

    def on_enterMyLetters(self, value):
        for ch in value.text:
            if (ch < 'а' or 'я' < ch) and ch != 'ё' and ch != '_':
                self.lettersInput.text = "Русские буквы и _"
                return
        self.layout.remove_widget(self.lettersInput)
        self.lettersInput = None
        self.myLetters = value.text
        self.myLettersLabel.text += value.text

    def changeMyLetters(self, instance):
        if self.lettersInput != None:
            return
        instance.text = "мои буквы : "
        self.lettersInput = TextInput(text="?", multiline=False, size_hint=instance.size_hint,
                              pos=instance.pos, background_color=(1,1,1,1), foreground_color=(0,0,0,1), font_size=30)
        self.lettersInput.bind(on_text_validate=self.on_enterMyLetters)
        self.layout.add_widget(self.lettersInput)
        
        
