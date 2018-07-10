# 用于计算当沿路径跑动的时候，之间的落差随着高度的增加，小汽车的损坏程度加大，当高度落差>5 时，小汽车报废
# 计算公式：y=2*x^2
#
import random
import data
import os

max = 30
pc = 0.8  # 交差概率
selpc = 0.6  # 自然选择的概率
Pm = 0.2  # 变异概率
import os
import logging
import logging.config
filepath = os.path.join(os.path.dirname(__file__), 'log.conf')
print(filepath)
logging.config.fileConfig(filepath)
log = logging.getLogger()
l=logging.getLogger("resu")

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
        k2 = map[r[0]][r[1]]
        e = k2 - k1
        car = car - cal(e)
        k1 = k2
    return car


def choose(p):
    population = []
    chroms = p
    chooselist = list(calcutepower(r) for r in p)
    log.info("适应度列表：%s" % chooselist)
    chooseposible = ((q, w / sum(chooselist)) for q, w in enumerate(chooselist))
    chooseposible = list(chooseposible)
    chooseposible = sorted(chooseposible, key=lambda x: x[1], reverse=True)
    chooselist = sorted(chooselist, reverse=True)
    log.info("选择概率%s" % chooseposible)
    log.info("选择%s" % chooselist)
    l.info("适应度列表：%s" % chooselist)
    m = 0
    while m < len(chooseposible) * selpc:
        log.info(chooseposible[m][0])
        population.append(chroms[chooseposible[m][0]])
        m = m + 1
    log.info("自然选择出的个体数量：%s" % len(population))
    log.info("选择出的个体的：%s" % population)
    return population


# 交换基因随机选取两个个体进行交配，这样的话就可以进行新的个体产生
def crossgene(p):
    log.info("交配前的种群中个体数量%s" % len(p))
    population = []
    population = population + p
    inxe = len(p) * pc
    inxe = int(inxe)
    log.info("随机选择出个体进行%s次交配" % inxe)
    i = 0
    childp = []
    while i < inxe:
        temp = []
        pos1 = random.randint(0, inxe) - 1  # 父亲
        log.info("父亲染色体：%s" % pos1)
        pos2 = random.randint(0, inxe) - 1  # 母亲
        log.info("母亲染色体：%s" % pos2)
        # 此处不再判断是不是相等，如果相等就按自我交配处处理
        w1 = random.randint(0, len(p[pos1]) - 1)
        log.info("父亲基因交换位置：%s" % w1)
        w2 = random.randint(0, len(p[pos2]) - 1)
        log.info("母亲基因交换位置：%s" % w2)
        ent1 = p[pos1]
        ent2 = p[pos2]
        log.info("父亲：%s" % ent1)
        log.info("母亲：%s" % ent2)
        if ent1[w1][0] <= ent2[w2][0] and ent1[w1][1] <= ent2[w2][1]:  # 取父亲的前面的基因
            father = temp + list((w for q, w in enumerate(ent1) if q < w1))
            mather = list((w for q, w in enumerate(ent2) if q > w2))
            child = initanswer(temp, ent1[w1], ent2[w2])
            log.info("来自父亲基因：%s" % father)
            log.info("来自母亲基因：%s" % mather)
            log.info("孩子自己的基因：%s" % child)
            child = father + child + mather
            log.info("孩子：%s" % child)
            childp.append(child)
        elif ent1[w1][0] >= ent2[w2][0] and ent1[w1][1] >= ent2[w2][1]:  ##取母亲的前面的基因
            father = temp + list((w for q, w in enumerate(ent1) if q > w1))
            mather = list((w for q, w in enumerate(ent2) if q < w2))
            child = initanswer(temp, ent2[w2], ent1[w1])
            log.info("来自父亲基因：%s" % father)
            log.info("来自母亲基因：%s" % mather)
            log.info("孩子自己的基因：%s" % child)
            child = mather + child + father
            log.info("孩子：%s" % child)
            childp.append(child)
        else:
            log.error("两个染色体虽然相爱，但是无法生孩子")
        i = i + 1
    log.info("新产生的下一代个体数量%s" % len(childp))
    log.info(childp)
    population = population + childp
    log.info("交配后的种群中个体数量%s" % len(population))
    return population


# 开始变异。变异只能是行变到列变，这们的话，只后边的重新说计算
def changenosignal(p):
    log.info("变异前的种群中个体数量%s" % len(p))
    population = []
    pr = random.randint(1, 4)
    pm = pr * Pm
    lk = 0
    for q in p:
        lk = lk + len(q)
    pos = lk * pm
    log.info("计算在群体中要变异的位置：%s" % pos)
    genpos = divmod(pos, 2 * max - 2)[1]
    genpos = int(genpos)
    whichc = divmod(pos, 2 * max - 2)[0]
    whichc = int(whichc)
    log.info("变异的染色体号：%s" % whichc)
    log.info(p[whichc])
    log.info("变异的基因位置：%s" % genpos)
    tem = p[whichc]
    log.info("变异前的基因：%s" % str(tem[genpos]))
    log.info(tem)
    k = genpos
    del tem[k + 1:]
    if tem[genpos][0] == tem[genpos - 1][0]:
        op = tem[genpos]
        del tem[genpos]
        pl = ((op[0] + 1, op[1] - 1))
    else:
        op = tem[genpos]
        del tem[genpos]
        pl = ((op[0] - 1, op[1] + 1))
    log.info("变异后的基因：%s" % str(pl))
    u = []
    u = initanswer(u, pl)
    tem = tem + u
    del p[whichc]
    p.insert(whichc, tem)
    log.info(tem)
    population = population + p
    return population
    pass


def begin():
    y = 0
    p = data.route
    while y < 51000:
        log.info("第%s次迭代" % y)
        p = choose(p)
        p = crossgene(p)
        p = changenosignal(p)
        chooselist = list(calcutepower(r) for r in p)
        log.info("适应度列表：%s" % chooselist)
        chooseposible = ((q, w / sum(chooselist)) for q, w in enumerate(chooselist))
        chooseposible = sorted(chooseposible, key=lambda x: x[1], reverse=True)
        log.info("当前最好的路径：%s" % p[chooseposible[0][0]])
        log.info("当前次好的路径：%s" % p[chooseposible[1][0]])
        y = y + 1


begin()
