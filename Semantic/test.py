import jieba
from py2neo import Graph, Node


#1.连接KB
g = Graph(
    host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
    http_port=7474,  # neo4j 服务器监听的端口号
    user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
    password="123456")

#2.获取用户输入的问题
user_input = input("请输入你的字符串：")   #T72中的哪些功能是父功能
#3.将components.txt里的词都提取出来，保存到一个列表中，供之后查询意图使用
components = []
f = open("dict/components","r",encoding="utf-8")
data = f.readlines()
for d in data:
    components.append(d)
    # print(d)
jieba.load_userdict("D:\Desktop\MyKB\DATA\dictMy")    #自定义词典
words = jieba.lcut(user_input)

print("words:",words)
for word in words:
    if word in components:

        print("用户查询的是跟目标功能有关的问题")
        query = f"MATCH (n:function) WHERE n.父功能ID=n.部件ID RETURN n.name"   #父功能ID为空这里不好判断，用和部件ID一样都为空来判断
        results = g.run(query)
        print("T72的{}有：".format(word))
        for result in results:
            print(result)
        break


