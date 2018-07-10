tem = [(0, 0), (1, 1), (3, 1), (4, 2), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12),
       (14, 12), (15, 13), (15, 15), (15, 17), (16, 18), (16, 20), (17, 21), (19, 21), (21, 21), (21, 23), (22, 24),
       (23, 25), (24, 26), (25, 27), (26, 28), (28, 28), (29, 29)]
k = 6

import random

leb = 29


def initanswer(result, item, ditem=(leb, leb)):
    if item[0] >= ditem[0]:
        if item[1] >= ditem[1]:
            result.append(ditem)
            return result
    pos = random.randint(0, 1)
    if pos == 0 and item[0] < ditem[0]:
        result.append(item)
        temp = (item[0] + 1, item[1])
        return initanswer(result, temp, ditem)
    elif pos == 1 and item[1] < ditem[1]:
        result.append(item)
        temp = (item[0], item[1] + 1)
        return initanswer(result, temp, ditem)
    return initanswer(result, item, ditem)


result = []
d = (9, 8)
result = initanswer(result, (2, 3), ditem=d)
print(result)
print(len(result))
