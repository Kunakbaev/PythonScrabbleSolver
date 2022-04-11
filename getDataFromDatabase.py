
import json

def getData():
    with open('shortNouns.json', 'r', encoding='utf-8') as fd:
        words = json.load(fd)
        l = []
        for key in words:
            l.append(words[key])
        return l