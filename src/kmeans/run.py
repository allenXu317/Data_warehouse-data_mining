import csv
import os
import random
from time import sleep

# 实现 最原始版本的 kmeans 算法，可用于多维数据集计算
# 测试数据集为4维数据集
# 但是还没进行验证

#增加一行

def mkdir(path):

    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
        return True

    else:
        print("---  There is this folder!  ---")
        return False

# 对文本数据csv化
def getCsv(pathSrc,pathDst):

    # mkdir(pathDst)

    file = open(pathSrc,"r",encoding='utf-8')

    new_file = open(pathDst,"w",newline="",buffering=10,encoding='utf-8')

    writer = csv.writer(new_file)

    # first_row = ['']

    types = {}
    t_type = 0

    line = 0
    for f in file:
        row= []
        f = f.replace('\n','')
        text = f.split('\t')
        # text = f.split(',')
        print(text)
        i = 0
        while i<len(text):
            row.append(text[i])
            if i == len(text)-1 and line != 0:
                if text[i] not in types :
                    types[text[i]] = t_type
                    t_type += 1
            i += 1
        line += 1

        # print(types)
        writer.writerow(row)
    
    return types


#得到所有向量
def getDatas(datasPath="",types=[]):
    file = open(datasPath,"r",encoding='utf-8')
    reader = csv.reader(file)
    datas = []
    line = 0
    for r in reader:
        data = []
        if line == 0:
            line += 1
            continue
        for rr in r:
            if rr in types:
                data.append(types[rr])
                continue
            data.append(float(rr))
        datas.append(data)
    return datas

# 得到初始的k个向量
def getDefaultK(k,datas=[]):
    index = []
    while k>0:
        i = random.randint(0,len(datas)-1)
        if i in index:
            continue
        else:
            k -= 1
            index.append(i)
    res = []
    print("初始的index为：")
    print(index)
    for i in index:
        res.append(datas[i])

    # res = [datas[5],datas[12],datas[24]]

    return res


# 计算均值向量:
def getMeanVector(datas=[],k=1):
    if len(datas) == 0:
        res = []
        return res
    
    res = [0 for _ in range(len(datas[0]))]

    for i,val in enumerate(res):
        for data in datas:
            res[i] += data[i]
        res[i] /= k


    return res
        

# 计算欧氏距离:
def getEdistance(x1=[],x2=[]):
    # print(x1,x2)
    distance = 0.0
    i = 0
    calc = 0.0
    while i<len(x1):
        t = x1[i] - x2[i]
        t *= t
        calc += t
        i += 1
    distance = calc ** 0.5
    # print(distance)
    return distance

# 对样本数据进行预处理
def preProcessDatas(datas=[]):
    res = {}
    i = 1
    while i<=len(datas):
        res[i-1] = datas[i-1]
        i += 1
        # print(res)
    return res

# 得到k个簇
def getClusters(k):
    i = 1
    clusters = {}
    while i<=k:
        clusters[i] = []
        i += 1
    return clusters


def getMin(arr):
    i = 0
    t_min = arr[0]
    loc = 0
    while i < len(arr):
        if t_min > arr[i]:
            t_min = arr[i]
            loc = i
        i += 1
    return loc


def myKmeas(k=0,datas=[]):

    MAX_LOOP = 100

    #获取初始的均值向量
    starts = getDefaultK(k,datas)
    print("初始的"+str(k)+"个均值向量为:")
    print(starts)

    #对数据进行预处理
    p_datas = preProcessDatas(datas)
    # print(p_datas)

    #得到初始的k个簇
    clusters = getClusters(k)

    vectorF = []
    vectorF = starts

    loop = 0
    while loop < MAX_LOOP:
        # print(vectorF)
        clusters = getClusters(k)
        vectorK = []
        loop += 1
        # 距离计算
        for p in p_datas:
            data = p_datas[p]
            temp = []
            for s in vectorF:
                if len(s) == 0:
                    s = [0 for _ in range(len(data))]
                    # continue
                # print(s,data)
                distance = getEdistance(data,s)
                temp.append(distance)
            # print(temp)
            # sleep(5)
            c_index = getMin(temp)
            clusters[c_index+1].append(p)
        print("---------------------------------------")
        # print(clusters)
        for i in clusters:
            print(len(clusters[i]))

        # 比较新的均值向量
        for c in clusters:
            cluster = clusters[c]
            c_datas = []
            for cc in cluster:
                c_datas.append(p_datas[cc])
                # print(c_datas)
            vectorK.append(getMeanVector(c_datas,len(cluster)))

        flag = True
        # print(vectorK)
        # sleep(5)
        for i,val in enumerate(vectorF):
            if vectorF[i] != vectorK[i]:
                # print(vectorK[i],vectorF[i])
                vectorF[i] = vectorK[i]
                flag = False
        # vectorK = []
        if flag == True:
            break

    # print(loop)
    # print(clusters)
    print("迭代次数为:"+str(loop)) 
    for c in clusters:
        print(clusters[c])           


    

pathSrc = "../dwDatas.txt"
pathDst = "../datas.csv"

types = getCsv(pathSrc,pathDst)
datas = getDatas(pathDst,types)
print(datas)
k = 10
myKmeas(k,datas)


# 欧氏距离测试:
# k1 = [0.403,0.237]
# k2 = [0.697,0.460]
# d = getEdistance(k1,k2)
# print(d)

