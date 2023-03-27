import jieba
from py2neo import Graph, Node

#连接数据库
# g = Graph(
#             host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
#             http_port=7474,  # neo4j 服务器监听的端口号
#             user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
#             password="123456")
s = "T72坦克的部件BJ0002的毁伤模式有哪几种？它的目标类型是什么？"
print("\n")
print(s)
print("\n")
s1 = jieba.lcut(s)
print(s1)
jieba.load_userdict("D:\Desktop\MyKB\DATA\dictMy")    #自定义词典
s2 = jieba.lcut(s)
print("\n")
print("\n")
print(s2)
# s = "T72坦克的部件BJ0002的毁伤模式有哪几种？这些毁伤模式的名称是什么？"
# s1 = jieba.lcut(s,cut_all=False)   #直接用这个返回分词得到的词语列表，用cut得到的列表是单个字的
# print("s1", s1)
# s2 = list(" ".join(s1))
# print(s2)
# ID = " "
# for i in range(0, len(s1)):
#     # print("开始解析")
#     word = s1[i]
#     # print("word",word)
#     if word == "部件":
#         ID = s1[i+1]
#         print("ID",ID,type(ID))
#     if word == "毁伤模式":
#         sql = "MATCH (m:component)-[r:existDamage]->(n:damagePattern) where m.部件ID = '%s' return n.毁伤模式编号, n.毁伤模式名称" % (ID)#.format(ID)
#         result = g.run(sql)
#         print(result)
#         break


# if "目标类型.txt" in s1:
#
#     sql = "MATCH (m:target)-[r:belongsTo]->(n:targetType) where m.name = 'T72' return n.name"
#     result = g.run(sql)
#     print(result)
# print(s)
# print(" ".join(s1))