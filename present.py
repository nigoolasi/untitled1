# 用于计算当沿路径跑动的时候，之间的落差随着高度的增加，小汽车的损坏程度加大，当高度落差>5 时，小汽车报废
# 计算公式：y=2*x^2
#
import random
import data

max = 30
pc = 0.8  # 交差概率
selpc = 0.6
Pm = 0.2  # 变异概率




def geneanswer(i, j):
    result = []
    while i < max and j < max:
        t = random.randint(0, 1)
        if t == 1 and i <= max - 2:
            i = i + 1
        elif j <= max - 2:
            j = j + 1
        else:
            if t == 1:
                j = j + 1
            else:
                i = i + 1
        result.append((i, j))
    return result

def cal(x):
    return 2 * pow(x, 2)


def calcutepower(R):
    car = 100
    map = data.map
    k1 = 0
    for r in R:
        k2 = map[r[0]][r[1]]
        e = k2 - k1
        car = car - cal(e)
        print("汽车完整度：%s" % car)
        k1 = k2
    print("染色体的适应度：%s" % car)
    return car
    pass


def choose():
    population = []
    chroms = data.route
    chooselist = (calcutepower(r) for r in chroms)
    print("适应度列表：?%s" % chooselist)
    chooseposible = ((q, w / sum(chooselist)) for q, w in enumerate(chooselist))
    chooseposible = list(chooseposible)
    sorted(chooseposible, key=lambda x: x[1])
    print("选择概率%s" % chooseposible)
    m = 0
    while m < max * selpc:
        population.append(chroms[chooseposible[m][0]])
        m = m + 1
    print("经过选择后的种群%s" % population)
    return population


# 交换基因随机选取两个个体进行交配，这样的话就可以进行新的个体产生
def crossgene(p):
    population = []
    population = population + p
    inxe = len(p) * pc
    i = 0
    while i < inxe:
        temp = []
        pos1 = random.randint(0, inxe)  # 父亲
        print("父亲染色体：%s" % pos1)
        pos2 = random.randint(0, inxe)  # 母亲
        print("母亲染色体：%s" % pos2)
        # 此处不再判断是不是相等，如果相等就按自我交配处处理
        w1 = random.randint(0, len(p[pos1]))
        print("父亲基因交换位置：%s" % w1)
        w2 = random.randint(0, len(p[pos2]))
        print("母亲基因交换位置：%s" % w2)
        ent1 = p[pos1]
        ent2 = p[pos2]
        if ent1[w1][0] <= ent2[w2][0]:
            temp = temp + list((for q, w in enumerate(ent1) if q < w1))
            j = 0
            while j < ent2[w2][0] - ent1[w1][0]:
                temp.append(ent1[w1][0] + j, ent1[w1][1])
                j = j + 1
            j = 0
            while j < ent2[w2][1] - ent1[w1][1]:
                temp.append(ent1[w1][0], ent1[w1][1] + j)
                j = j + 1
            temp = temp + list((for q, w in enumerate(ent2) if q > w2))
        else:
            temp = temp + list((for q, w in enumerate(ent2) if q < w2))
            j = 0
            while j < ent1[w1][0] - ent2[w2][0]:
                temp.append(ent2[w2][0] + j, ent1[w1][1])
                j = j + 1
            j = 0
            while j < ent1[w1][1] - ent2[w2][1]:
                temp.append(ent1[w1][0], ent1[w1][1] + j)
                j = j + 1
            temp = temp + list((for q, w in enumerate(ent1) if q > w1))
        population.append(temp)
        i = i + 1
    print("交配后的种群%s" % population)
    return population


# 开始变异。变异只能是行变到列变，这们的话，只后边的重新说计算
def changenosignal(p):
    population = []
    pr = random.randint(1, 4)
    pm = pr * Pm
    lk = 0
    for q in p:
        lk = lk + len(q)
    pos = lk * pm
    whichc = pos / max
    genpos = divmod(pos, max)
    print("变异的点%s"%whichc)
    if p[whichc][genpos][0] == p[whichc][genpos - 1][0]:
        p[whichc][genpos][0] = (p[whichc][genpos][0] + 1, p[whichc][genpos][1] - 1)
    else:
        p[whichc][genpos][0] = (p[whichc][genpos][0] - 1, p[whichc][genpos][1] + 1)
    population=population+p
    population=population+geneanswer(population[whichc][genpos][0],population[whichc][genpos][1])
    print("变异后的种群%s" % population)
    pass


def begin():

    pass


if __name__ == "main":
    for item in data.route:
        pass
