
import requests
from bs4 import BeautifulSoup

words = open("./words.txt", "w", encoding="utf-8")
meanings = open("./meanings.txt", "w", encoding="utf-8")

smallURL = 'https://ru.wiktionary.org'
URL =  'https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5'


def loadPage(link, word, wordInd):
    wordPage = requests.get(link)
    wordSoup = BeautifulSoup(wordPage.content, "html.parser")
    mwPagesDiv = wordSoup.find("div", class_="mw-parser-output")

    morfotableDiv = mwPagesDiv.find("table", "morfotable ru")
    endl = "\n"
    words.write(str(wordInd) + endl)
    words.write(word + endl)
    if morfotableDiv != None:
        td = morfotableDiv.find_all("tr")[1].find_all("td")[2]
        multipleWordBad = td.text
        multipleWord = ""
        for ch in multipleWordBad:
            if ('а' <= ch and ch <= 'я') or ch == 'ё':
                multipleWord += ch

        if multipleWordBad[0] != '*' and multipleWord != word:
            words.write(multipleWord + endl)

    ol = mwPagesDiv.find("ol")
    meaning = ol.find("li").text
    meaning.replace(endl, "/n")
    meanings.write(meaning + endl)


pageInd = 1
wordInd = 1
while True:
    # if pageInd == 11: break
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    mwPagesDiv = soup.find(id="mw-pages")
    mwCategoryColumnsDiv = mwPagesDiv.find("div", class_="mw-category-columns")
    ulList = mwCategoryColumnsDiv.find_all("ul")
    for ul in ulList:
        linksList = ul.find_all("li")
        #print(linksList)
        cnt = 1
        for elem in linksList:
            # if cnt == 11: break
            link = elem.find("a")
            href = link["href"]
            word = link["title"]
            if len(word) < 3 or len(word) > 15 or word[0] == word[0].upper() or word.find('-') != -1:
                continue
            meaning = loadPage(smallURL + href, word, wordInd)
            #print(cnt, word, meaning, end=" ")
            print(f"{pageInd}.{cnt}")
            cnt += 1
            wordInd += 1
    nextPageA = mwPagesDiv.find_all("a")[1]
    if pageInd == 1: nextPageA = mwPagesDiv.find("a")
    URL = smallURL + nextPageA["href"]
    if nextPageA.text != "Следующая страница":
        break
    pageInd += 1
print("All job has been done!")
print(wordInd - 1, "words have been collected")




