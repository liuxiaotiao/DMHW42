from numpy import *

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList



def apriori(dataSet, minSupport=0.1):
    D = list(map(set, dataSet))
    C1 = createC1(
        dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def getRules(itemsets, frequencysets, mincof):
    iSet = {}
    for i in frequencysets:
        iSet[frozenset(i)] = 0

    for i in itemsets:
        for j in frequencysets:
            if j.issubset(i):
                iSet[frozenset(j)] = iSet.get(frozenset(j), 0) + 1

    d_order = sorted(iSet.items(), key=lambda n: n[1], reverse=False)
    daset=[]
    for i in range(len(d_order)):
        for j in range(len(d_order)):
            if ((d_order[j][0] - d_order[i][0]) != frozenset()) & (d_order[i][0].issubset(d_order[j][0])):
                conf = d_order[j][1] / d_order[i][1]
                if conf >= mincof:
                    a = d_order[i][0]
                    b = d_order[j][0] - d_order[i][0]

                    ami = []
                    if b == frozenset({'yes'}):
                        ami.append(a)
                        ami.append(b)
                        ami.append(conf)
                        daset.append(ami)
                        # print(a, b, conf)
                    elif b == frozenset({'no'}):
                        ami.append(a)
                        ami.append(b)
                        ami.append(conf)
                        daset.append(ami)
                        # print(a, b, conf)
    return daset


text = ['a','m','s','f']
text = frozenset(text)
print(text)
dataSet = [['a', 'h', 't', 'f', 'no'],
        ['a', 'h', 't', 'e', 'no'],
        ['b', 'h', 't', 'f', 'yes'],
        ['c', 'm', 't', 'f', 'yes'],
        ['c', 'l', 's', 'f', 'yes'],
        ['c', 'l', 's', 'e', 'no'],
        ['b', 'l', 's', 'e', 'yes'],
        ['a', 'm', 't', 'f', 'no'],
        ['a', 'l', 's', 'f', 'yes'],
        ['c', 'm', 's', 'f', 'yes'],
        ['a', 'm', 's', 'e', 'yes'],
        ['b', 'm', 't', 'e', 'yes'],
        ['b', 'h', 's', 'f', 'yes'],
        ['c', 'm', 't', 'e', 'no']]
L, suppData = apriori(dataSet)
# print(L)
c = []
for y in dataSet:
    d = set(y)
    c.append(d)
# print("Fset:", suppData)
cl = []

for ini in suppData:
    if len(ini)>2:
        if 'yes' in ini:
            cl.append(ini)
        elif 'no' in ini:
            cl.append(ini)

dataS = getRules(c, suppData, 0.6)

judgeset = []
for itemset in dataS:
    a = frozenset(itemset[0])
    if a.issubset(text):
        judgeset.append(itemset)
print(judgeset)

frodata = []
for ittt in dataSet:
    b = frozenset(ittt)
    frodata.append(b)

num1 = 0
num2 = 0
num3 = 0
num4 = 0
for ittttt in judgeset:
    if ittttt[1]==frozenset('yes'):
        for ites in frodata:
            if (ittttt[0].issubset(ites))|frozenset('yes').issubset(ites):
                num1 += 1
            elif (ittttt[0].issubset(ites))|frozenset('no').issubset(ites):
                num2 += 1
    else:
        for itesa in frodata:
            if (ittttt[0].issubset(itesa))|frozenset('no').issubset(itesa):
                num3 += 1
            elif (ittttt[0].issubset(itesa))|frozenset('yes').issubset(itesa):
                num4 += 1
num5 = num1/(num1+num2)
num6 = num3/(num3+num4)
if num5>num6:
    print('yes')
else:
    print('no')