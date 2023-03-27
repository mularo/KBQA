#运行前要先运行BuildTargetType.py先创建目标类型
#1.这里创建的目标T72这个节点，并且建立了与目标类型之间的关系
#这份代码可以用来创建所有目标的节点和与目标类型的关系——因为封装成了函数
from py2neo import Graph, Node
import csv
g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
filename = '2.2目标基本信息数据.csv'
def createNode(filename):
    data = {}   #把数据存储到字典中 一次装一个目标的基本信息
    with open(filename,"r",encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)        # 读取第一行每一列的标题
        print(header)
        for row in csv_reader:        #出标题的每一行中的所有列
            print(row)
            for i in range(len(row)):
                data.update({header[i]: row[i]})
            for item in data:  #查看一个目标的基本信息
                print(item)
    #在这里创建节点
            node = Node("target",name=data["目标名称"],ID=data["目标ID"],部署位置=data["部署位置"],description=data["描述"],目标位置=data["目标位置"],
                         目标速度=data["目标速度（m/s）"],国家=data["国家"],所属军种=data["所属军种"],服役时间=data["服役时间"],主要功能=data["主要功能"],
                         备注=data["备注"])
            g.create(node)
    return data["目标ID"]    #返回目标ID用于得到目标类型，创建关系

# targetID = createNode(filename)   #目标ID在什么范围内就可以判定是属于什么类型   ，target是目标ID，而不是目标名称
def getType(targetID):
    rang = int(targetID[2:])    #得到整数   来得到目标是属于什么目标类型
    if rang>=5000 and rang<6000:
        targetType = "工业设施类"
    elif rang>=4000 and rang<5000:
        targetType = "坦克"
    elif rang>=3000 and rang<4000:
        targetType = '阵地技术兵器'
    elif rang>=2000 and rang<3000:
        targetType = "建筑工事"
    elif rang>=1000 and rang<2000:
        targetType = '巡航导弹'
    else:
        targetType = "飞机"
    return targetType  #返回的是目标类型的名称name
#1.创建目标节点，并且返回目标的ID
targetID = createNode(filename)
#2.利用目标ID所属区间来得到目标类型，从而创建目标与目标类型间的关系
targetTypeName = getType(targetID)
print(targetID,targetTypeName)
#用的是m目标的ID和目标类型的名称
query = "match(p:target),(q:targetType) where p.ID='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            targetID, targetTypeName, "belongsTo", "目标类型")
g.run(query)  # 要run了才会执行query语句
print(query)
