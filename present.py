# 用于计算当沿路径跑动的时候，之间的落差随着高度的增加，小汽车的损坏程度加大，当高度落差>5 时，小汽车报废
# 计算公式：y=2*x^2
#
import random
import data

max = 30
pc = 0.8  # 交差概率
selpc = 0.6#自然选择的概率
Pm = 0.2  # 变异概率

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

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


def cal(x):
    return 2 * pow(x, 2)


def calcutepower(R):
    car = 1000
    map = data.map
    k1 = 0
    for r in R:
        # log.info(r[0])
        # log.info(r[1])
        k2 = map[r[0]][r[1]]
        e = k2 - k1
        # print(e)
        car = car - cal(e)
        k1 = k2
    # print("染色体的适应度：%s" % car)
    return car


def choose(p):
    population = []
    chroms = p
    chooselist = list(calcutepower(r) for r in p)
    print("适应度列表：%s" % chooselist)
    chooseposible = ((q, w / sum(chooselist)) for q, w in enumerate(chooselist))
    chooseposible = list(chooseposible)
    sorted(chooseposible, key=lambda x: x[1])
    print("选择概率%s" % chooseposible)
    m = 0
    while m < len(chooseposible) * selpc:
        population.append(chroms[chooseposible[m][0]])
        m = m + 1

    log.info("自然选择出的个体数量：%s"%len(population))
    return population


# 交换基因随机选取两个个体进行交配，这样的话就可以进行新的个体产生
def crossgene(p):
    log.info("交配前的种群中个体数量%s" % len(p))
    population = []
    population = population + p
    inxe = len(p) * pc
    inxe = int(inxe)
    print(inxe)
    i = 0
    while i < inxe:
        temp = []
        pos1 = random.randint(0, inxe) - 1  # 父亲
        print("父亲染色体：%s" % pos1)
        pos2 = random.randint(0, inxe) - 1  # 母亲
        print("母亲染色体：%s" % pos2)
        # 此处不再判断是不是相等，如果相等就按自我交配处处理
        w1 = random.randint(0, len(p[pos1]) - 1)
        print("父亲基因交换位置：%s" % w1)
        w2 = random.randint(0, len(p[pos2]) - 1)
        print("母亲基因交换位置：%s" % w2)
        ent1 = p[pos1]
        ent2 = p[pos2]
        log.info("父亲：%s" % ent1)
        log.info("母亲：%s" % ent2)
        if ent1[w1][0] <= ent2[w2][0]:  # 取父亲的前面的基因
            father = temp + list((w for q, w in enumerate(ent1) if q < w1))
            mather = list((w for q, w in enumerate(ent2) if q > w2))
            child = initanswer(temp, ent1[w1], ent2[w2])
            log.info("来自父亲基因：%s" % father)
            log.info("来自母亲基因：%s" % mather)
            log.info("孩子自己的基因：%s" % child)
            child = father + child + mather
        else:  ##取母亲的前面的基因
            father = temp + list((w for q, w in enumerate(ent1) if q > w1))
            mather = list((w for q, w in enumerate(ent2) if q < w2))
            child = initanswer(temp, ent2[w2], ent1[w1])
            log.info("来自父亲基因：%s" % father)
            log.info("来自母亲基因：%s" % mather)
            log.info("孩子自己的基因：%s" % child)
            child = mather + child + father
        log.info("孩子：%s" % child)
        population.append(child)
        i = i + 1
    log.info("交配后的种群中个体数量%s" % len(population))
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
    print(pos)
    genpos = divmod(pos, 2 * max - 2)[1]
    genpos = int(genpos)
    whichc = divmod(pos, 2 * max - 2)[0]
    whichc = int(whichc)
    print("变异的点%s" % whichc)
    print("变异的点%s" % genpos)
    tem = p[whichc]
    k = genpos
    del tem[k + 1:]
    log.info(tem)
    if tem[genpos][0] == tem[genpos - 1][0]:
        op = tem[genpos]
        del tem[genpos]
        tem.append((op[0] + 1, op[1] - 1))
    else:
        op = tem[genpos]
        del tem[genpos]
        tem.append((op[0] - 1, op[1] + 1))
    u = []
    u = initanswer(u, tem[genpos])
    tem = tem + u
    log.info(tem)
    population = population + p
    # print("变异后的种群%s" % population)
    return population
    pass


def begin():
    y = 0
    p = data.route
    while y < 3:
        print("第%s次迭代" % y)
        p = choose(p)
        p = crossgene(p)
        p = changenosignal(p)
        p = choose(p)
        print(p)
        y = y + 1


begin()
