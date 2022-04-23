

wordLines = []
breakLine = "----------"
correct = open("./correct.txt", "w", encoding="utf-8")
with open("./words_1.0.txt", "r", encoding="utf-8") as f:
    for line in f:
        wordLines.append(line)
i = 0
temp = []
badly = 0
plus = 0
while i < len(wordLines):
    if wordLines[i][:-1] == breakLine:
        if i:
            for j in range(1, len(temp)):
                if temp[j][:2] != temp[0][:2]:
                    if len(temp[1]) >= 2:
                        ch = temp[0][1]
                        ch2 = temp[1][1]
                        isVovel = ch == 'а' or ch == 'о' or ch == 'е' or ch == 'и' or ch == 'э' \
                                  or ch == 'ю' or ch == 'я' or ch == 'у' or ch == 'ё' or ch == 'ы'
                        isVovel2 = ch2 == 'а' or ch2 == 'о' or ch2 == 'е' or ch2 == 'и' or ch2 == 'э' \
                                   or ch2 == 'ю' or ch2 == 'я' or ch2 == 'у' or ch2 == 'ё' or ch2 == 'ы'
                        if isVovel != isVovel2:
                            temp[1] = temp[0][:2] + temp[1][1:]
                            print(*temp)
                            break
            correct.write(breakLine + "\n")
            correct.write(temp[0] + "\n")
            if len(temp) >= 2 and len(temp[1]) >= len(temp[0]) + 3:
                # print(temp[0], temp[1])
                osn = temp[0][:2]
                ind = temp[1].find(osn, 3)
                # print(ind, temp[1][:ind], temp[1][ind:])
                # print(temp[1][:ind], temp[1][ind:])
                correct.write(temp[1][:ind] + "\n")
                correct.write(temp[1][ind:] + "\n")
                badly += 1
            elif len(temp) >= 2:
                correct.write(temp[1] + "\n")
            temp = []
    else:
        word = wordLines[i][:-1]
        temp.append(word)
    i += 1
print("Words have been reparsed")
