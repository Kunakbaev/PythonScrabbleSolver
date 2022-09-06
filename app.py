from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import copy

import setup
from setup import *
import solve

# Window.size = (WINDOW_W, WINDOW_H)

# this is big ugly file, because I don't know how to work with graphics and widgets in python

class MainApp(App):
    def getColor(self, num):
        if num == 2:
            return setup.DOUBLE_LETTER
        if num == 3:
            return setup.TRIPLE_LETTER
        if num == 22:
            return setup.DOUBLE_WORD
        if num == 33:
            return setup.TRIPLE_WORD
        return setup.NORM

    def build(self):
        Window.size = (WINDOW_W, WINDOW_H)
        Window.fullscreen = "auto"
        self.showedButton = None
        self.title = 'Scrabble solver'
        self.size = (WINDOW_W, WINDOW_H)
        self.window_padding = WINDOW_PADDING
        self.tiles = []
        self.w = self.h = setup.GAME_W
        self.isInput = False
        layout = FloatLayout()
        buttonW = (self.size[1] - self.window_padding * 2) / self.w
        buttonH = (self.size[1] - self.window_padding * 2) / self.h
        self.buttonW = buttonW
        self.buttonH = buttonH
        self.matrix = []
        self.myScore = self.computerScore = 0
        for i in range(self.h):
            self.tiles.append([])
            self.matrix.append([])
            for j in range(self.w):
                self.matrix[i].append('')
                offset = 2
                col = solve.getMultiplicator(i, j)
                btn = Button(text='',
                             background_normal='',
                             background_down='',
                             background_color=self.getColor(col),
                             font_size=40, bold=True,
                             pos=(self.window_padding + j * buttonW + offset,
                                  self.size[1] - self.window_padding - (i + 1) * buttonH + offset),
                             size_hint=((buttonW - 2 * offset) / self.size[0], (buttonH - 2 * offset) / self.size[1])
                             )
                btn.ids['i'] = i
                btn.ids['j'] = j
                btn.bind(on_press=self.tile_on_press)
                self.tiles[i].append(btn)
                layout.add_widget(btn)
        self.layout = layout
        self.addOtherButtons()
        return layout

    def addOtherButtons(self):
        h = (self.size[1] - self.window_padding * 7) / 12
        w = (self.size[0] - self.window_padding * 3 - self.buttonW * self.w)
        self.myScoreLabel = Button(text="Мои очки : 0",
                                     background_normal='',
                                     background_down='',
                                     background_color=WHITE,
                                     color=BLACK,
                                     font_size=30,
                                     pos=(self.window_padding * 2 + self.buttonW * self.w,
                                          self.size[1] - h - self.window_padding),
                                     size_hint=((w - self.window_padding) * 0.5 / self.size[0], h / self.size[1])
                                     )
        self.computerScoreLabel = Button(text="Очки оппонента : 0",
                                   background_normal='',
                                   background_down='',
                                   background_color=WHITE,
                                   color=BLACK,
                                   font_size=30,
                                   pos=(self.window_padding * 3 + self.buttonW * self.w + (w - self.window_padding) * 0.5,
                                        self.size[1] - h - self.window_padding),
                                   size_hint=((w - self.window_padding) * 0.5 / self.size[0], h / self.size[1])
                                   )
        self.skipButton = Button(text='Пропустить',
                                background_normal='',
                                background_down='',
                                background_color=WHITE,
                                color=BLACK,
                                font_size=40,
                                pos=(self.window_padding * 2 + self.buttonW * self.w,
                                     self.size[1] - 3 * h - 3 * self.window_padding),
                                size_hint=((w - self.window_padding - h) / self.size[0], h / self.size[1])
                                )
        self.changeOrientation = Button(text='H',
                                        background_normal='',
                                        background_down='',
                                        background_color=WHITE,
                                        color=BLACK,
                                        font_size=40,
                                        pos=(
                                        self.window_padding * 2 + self.buttonW * self.w + w - h,
                                        self.size[1] - 3 * h - 3 * self.window_padding),
                                        size_hint=(h / self.size[0], h / self.size[1])
                                        )
        self.helpLabel = TextInput(text=helpWord,
                                   background_disabled_normal="", multiline=True,
                                   background_color=WHITE, foreground_color=BLACK,
                                   font_size=20, pos=(0, 0), disabled=True,
                                   size_hint=(1, None), height=800
                                   )
        self.helpLabelView = ScrollView(do_scroll_x=False, do_scroll_y=True,
                                        pos=(self.window_padding * 2 + self.buttonW * self.w,
                                             self.window_padding),
                                        size_hint=(w / self.size[0], 4 * h / self.size[1])
                                        )
        self.helpLabelView.add_widget(self.helpLabel)
        self.myLettersLabel = Button(text="Мои буквы : " + self.myLetters,
                                     background_normal='',
                                     background_down='',
                                     background_color=WHITE,
                                     color=BLACK,
                                     font_size=40,
                                     pos=(self.window_padding * 2 + self.buttonW * self.w,
                                          self.size[1] - 2 * h - 2 * self.window_padding),
                                     size_hint=(w / self.size[0], h / self.size[1])
                                     )
        self.meaningInput = TextInput(multiline=False, size_hint=(w / self.size[0], h / self.size[1]),
                                      pos=(self.window_padding * 2 + self.buttonW * self.w,
                                           self.size[1] - 4 * h - 4 * self.window_padding),
                                      background_color=WHITE, foreground_color=BLACK, hint_text="Ваше слово : ",
                                      font_size=40)
        self.meaningPanel = TextInput(multiline=True, size_hint=(w / self.size[0], None),
                                      height=800, font_size=30,
                                      pos=(self.window_padding * 2 + self.buttonW * self.w,
                                           self.size[1] - 8 * h - 5 * self.window_padding),
                                      disabled=True, background_disabled_normal="", hint_text="Его значение",
                                      background_color=WHITE, foreground_color=BLACK
                                      )
        self.meaningPanelView = ScrollView(size_hint=(1, 4 * h / self.size[1]),
                                           pos=(self.window_padding * 2 + self.buttonW * self.w,
                                                self.size[1] - 8 * h - 5 * self.window_padding),
                                           do_scroll_x=False, do_scroll_y=True
                                           )
        self.meaningPanelView.add_widget(self.meaningPanel)
        self.lettersInput = None
        self.changeOrientation.bind(on_press=self.changeOrientationFunc)
        self.meaningInput.bind(on_text_validate=self.showMeaning)
        self.skipButton.bind(on_press=self.skipMove)
        self.layout.add_widget(self.myLettersLabel)
        self.layout.add_widget(self.skipButton)
        self.layout.add_widget(self.changeOrientation)
        self.layout.add_widget(self.helpLabelView)
        self.layout.add_widget(self.meaningInput)
        self.layout.add_widget(self.meaningPanelView)
        self.layout.add_widget(self.myScoreLabel)
        self.layout.add_widget(self.computerScoreLabel)

    def putWord(self, obj):
        solve.used.append(obj.wordInd)
        if obj.h == 'h':
            for j in range(obj.j, obj.j + len(obj.word)):
                self.tiles[obj.i][j].text = obj.word[j - obj.j]
                self.matrix[obj.i][j] = obj.word[j - obj.j]
                self.tiles[obj.i][j].color = BLACK
        else:
            for i in range(obj.i, obj.i + len(obj.word)):
                self.tiles[i][obj.j].text = obj.word[i - obj.i]
                self.matrix[i][obj.j] = obj.word[i - obj.i]
                self.tiles[i][obj.j].color = BLACK

    def tile_on_press(self, instance):
        i = instance.ids['i']
        j = instance.ids['j']
        text = self.meaningInput.text
        if len(text) == 0:
            # self.matrix[i][j] = ''
            # self.tiles[i][j].text = ''
            return
        h = 'h' if self.changeOrientation.text == 'H' else 'v'
        if h == 'h':
            if self.w <= j + len(text) - 1:
                return
        else:
            if self.h <= i + len(text) - 1:
                return
        word = solve.Word(text, i, j, h, 0, 0)
        if not self.gameObj.isGoodPlace(word):
            self.meaningPanel.text = "Возможные варианты, почему ход не получился: такого слова не существует, " \
                                     "вы ставите его не правильно или слово уже есть на доске"
            return
        self.putWord(word)
        self.gameObj.computerMove()

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
        self.meaningPanel.height = self.meaningPanel.line_height * lines
        self.meaningPanel.text += meaning

    def setMyLetters(self, value):
        self.layout.remove_widget(self.lettersInput)
        self.lettersInput = None
        self.myLetters = value.text
        self.myLettersLabel.text += value.text

    def skipMove(self, instance):
        self.gameObj.skipMove()
