import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

words = open("./words.txt", "w", encoding="utf-8")
meanings = open("./meanings.txt", "w", encoding="utf-8")
exceptions = open("./exceptions.txt", "w", encoding="utf-8")

breakLine = "----------"
smallURL = 'https://ru.wiktionary.org'
URL =  'https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5'

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def loadPage(link, word, wordInd):
    endl = "\n"
    try:
        wordPage = requests.get(link, verify=False)
        wordSoup = BeautifulSoup(wordPage.content, "html.parser")
        mwPagesDiv = wordSoup.find("div", class_="mw-parser-output")

        grammarType = mwPagesDiv.find("a", {"title": "существительное"})
        #print(grammarType)
        if grammarType == None:
            return False

        # getting meaning of the word
        ol = grammarType.find_next("ol")
        if ol == None:
            # print("mean")
            return False
        meaning = ol.find("li").text

        # getting multiple form of word (for example: apple -> apples)
        morfotableDiv = grammarType.find_previous("table", "morfotable ru")
        #print(morfotableDiv)
        multipleWord = ""
        if morfotableDiv != None:
            tr = morfotableDiv.find_all("tr")
            if len(tr) != 7:
                if len(tr) != 8:
                    return False
                td = tr[7].find("td")
                # print(td.text)
                if td.text != "М.":
                    return False
            td = tr[1].find_all("td")[2]
            multipleWordBad = td.text
            multiple = ""
            for ch in multipleWordBad:
                if ('а' <= ch and ch <= 'я') or ch == 'ё':
                    multiple += ch

            if multipleWordBad[0] != '*' and multiple != word:
                multipleWord = multiple

        words.write(breakLine + endl)
        words.write(word + endl)
        if len(multipleWord) != 0:
            words.write(multipleWord + endl)
        meanings.write(breakLine + endl)
        meanings.write(meaning + endl)
        return True
    except Exception:
        print("Some crazy exception with ", word, " at link ", link)
        exceptions.write("Some crazy exception with " + word + " at link " + link + endl)
        return False



# print(loadPage("https://ru.wiktionary.org/wiki/%D1%85%D0%BE%D1%80", "fuck", 1))

pageInd = 1
wordInd = 1
while True:
    # if pageInd == 11: break
    page = requests.get(URL, verify=False)
    # page = requests.get("https://ru.wiktionary.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5&subcatfrom=%D0%B1%D0%B0%D1%80&filefrom=%D0%B1%D0%B0%D1%80&pageuntil=%D0%91%D0%B0%D0%BA%D1%81%D1%82%D0%B5%D1%80#mw-pages", verify=False)
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
            isOkey = loadPage(smallURL + href, word, wordInd)
            if not isOkey:
                continue
            print(f"{pageInd}.{cnt} {word} wordInd : {wordInd}")
            #print(cnt, word, meaning, end=" ")
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
