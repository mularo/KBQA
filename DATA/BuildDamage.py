'''用来提取功能实体类型的py文件'''
import codecs
import csv
from py2neo import Graph, Node

g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
#建立毁伤等级的实体，与目标类型建立关系
'''根本不用将csv文件转存到txt文件中，直接在得到每一行的字典时进行处理即可'''
# fw = open("4.txt",'w',encoding = 'utf-8')
with codecs.open('6.1.csv', 'r', encoding='utf-8') as fp:
    fp_key = csv.reader(fp)  #所有列名，相当于得到了key
    for csv_key in fp_key:
        # print('字典的key值：%s' % csv_key)
        csv_reader = csv.DictReader(fp, fieldnames=csv_key)#按列名读取每一行的每一列（即键值）
        # print('DictReader()方法返回值：%s' % csv_reader)
        for row in csv_reader:
            csv_dict = dict(row)
            # print(type(csv_dict),csv_dict)
            targetTypeID = csv_dict['目标类型ID']
            name = csv_dict['毁伤等级名称']
            ID = csv_dict['毁伤等级ID']
            description = csv_dict['毁伤等级描述']
            node = Node("damageGrade", name=name, ID=ID, description=description)
            g.create(node)    #有一个问题是，目标类型在图谱中存储只有name
            query = "match(p:targetType),(q:damageGrade) where p.name='坦克'and q.毁伤等级名称='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                 name,"haveDamageGrade", "有毁伤等级")
            print(query)
            g.run(query)
            # json.dump(csv_dict,fw,ensure_ascii=False)
            # fw.write("\n")
# fw.close()
#再用8.2文件建立一个毁伤模式实体类别，有毁伤模式编号和毁伤模式名称，毁伤模式描述
#之后会与6.2文件建立关系   这里只建立毁伤模式的节点
with codecs.open('8.2.csv', 'r', encoding='utf-8') as f:
    fp_key = csv.reader(f)  #所有列名，相当于得到了key
    for csv_key in fp_key:
        # print('字典的key值：%s' % csv_key)
        csv_reader = csv.DictReader(f, fieldnames=csv_key)#按列名读取每一行的每一列（即键值）
        # print('DictReader()方法返回值：%s' % csv_reader)
        for row in csv_reader:
            csv_dict = dict(row)
            # print(type(csv_dict),csv_dict)
            damageID = csv_dict['毁伤模式编号']
            name = csv_dict['毁伤模式名称']
            description = csv_dict['毁伤模式描述']
            node = Node("damagePattern", number=damageID, name=name,description=description)
            print(node)
            g.create(node)    #有一个问题是，目标类型在图谱中存储只有name

            # json.dump(csv_dict,fw,ensure_ascii=False)
            # fw.write("\n")

