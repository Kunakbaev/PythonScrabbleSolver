
# decode and encode russian words

def rusInd(ch):
    if ch == 'ё': return 6
    if 'а' <= ch <= 'е':
        return ord(ch) - ord('а')
    if 'ж' <= ch <= 'я':
        return ord(ch) - ord('ж') + 7

def rusToEn(ch):
    if ch == '_': return ch
    num = rusInd(ch)
    if num < 26:
        return chr(ord('a') + num)
    return chr(ord('0') + num - 26)

def enToRus(ch):
    if ch == '_': return ch
    if ch == 'g': return 'ё'
    if 'a' <= ch <= 'f':
        return chr(ord('а') + ord(ch) - ord('a'))
    if 'h' <= ch <= 'z':
        return chr(ord('а') + ord(ch) - ord('a') - 1)
    return chr(ord('а') + 26 + ord(ch) - ord('0') - 1)

def enWordToRus(word):
    res = ""
    for ch in word:
        res += enToRus(ch)
    return res

def rusWordToEn(word):
    res = ""
    for ch in word:
        res += rusToEn(ch)
    return res