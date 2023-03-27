#运行一次，建立目标类型的六个实体节点
from py2neo import Graph, Node
g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
#建立毁伤等级的实体，与目标类型建立关系
with open('./目标类型.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        l = line.split(" ")
        # print(line)
        print(l)
        name = l[0]
        ID = l[1]
        description = l[2]
        node = Node("targetType", name=name,ID=ID,description=description)
        g.create(node)
