#这个要分三次创建关系，节点只能创建一次
'''用来提取功能实体类型的py文件'''
import codecs
import csv
import json
import os
from py2neo import Graph, Node
# '''读取并提取csv数据，程序运行前利用csv文件得到txt文件'''
# fw = open("4.txt",'w',encoding = 'utf-8')
# with codecs.open('./4.12.csv', 'r', encoding='utf-8') as fp:
#     fp_key = csv.reader(fp)  #所有列名，相当于得到了key
#     for csv_key in fp_key:
#         # print('字典的key值：%s' % csv_key)
#         csv_reader = csv.DictReader(fp, fieldnames=csv_key)#按列名读取每一行的每一列（即键值）
#         # print('DictReader()方法返回值：%s' % csv_reader)
#         for row in csv_reader:
#             csv_dict = dict(row)
#             # print(type(csv_dict),csv_dict)
#             json.dump(csv_dict,fw,ensure_ascii=False)
#             fw.write("\n")
# fw.close()
#
# file = open("4.txt","r",encoding = 'utf-8')
# lines = file.readlines()
# for line in lines:
#     line = json.load(line)
#     print(type(line),line)
# file.close()


class functionGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, '4.txt')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
        
    '''读取文件'''
#目前只读取了一个文件可用来构建部件实体
    def read_nodes(self):
        # 共5类节点 
        components = []  # 部件
        functions = []  # 功能

        function_infos = []  # 部件信息

        # 构建节点实体关系
        #1.功能与目标之间的关系
        #2.功能与部件之间的关系
        #3.功能之间的父子关系
        rels_haveFunction = []  # 目标－功能   拥有关系
        rels_relevant = []      # 功能 — 部件    关联关系
        rels_Father = []        # 功能 - 功能    父子关系

    #要考虑与目标建立的联系吗
        count = 0
        for data in open(self.data_path,encoding='utf-8'):
            function_dict = {}
            count += 1
            # print(count)
            data_json = json.loads(data)
            function = data_json['功能名称']   #得到功能名称，作为实体上的name
            functions.append(function)
            targetID  = data_json['目标ID']   #得到该功能属于的目标ID，用于之后建立关系1
            # match(p:function),(q:functionType) where p.name='T72'and q.name="坦克" create (p)-[r:目标类型.txt]->(q)    直接用这行语句就可以构建关系，对于这些关系，也许可以采取人工手动构建

            # print(functionType,type(functionType))
            # print("function",function)
            function_dict['功能名称'] = data_json['功能名称']
            function_dict['功能ID'] = data_json['功能ID']
            function_dict['功能描述'] = data_json['功能描述']
            function_dict['父功能ID'] = data_json['父功能ID']
            function_dict['部件ID'] = data_json['部件ID']
#1.添加到目标与功能关系
            rels_haveFunction.append([targetID,function])   #使用的是目标的ID和功能的名称
#2.添加到功能与部件的关联关系
            rels_relevant.append([function,function_dict['部件ID']])  #使用的是功能的名称和部件ID，也许可以与上一个文件相关联得到部件的名称，好像直接用部件ID在neo4j中查询就可以
#3.添加到父子关系
            if function_dict['父功能ID'] != "":
                rels_Father.append([function_dict['父功能ID'],function_dict['功能ID']])

#这里每个数据都有，原理是是不需要用if/else的，但是仅是针对这个目标的，所以还是用以下判断

            function_infos.append(function_dict)
            # print(function_dict)

        return set(functions), rels_haveFunction,rels_relevant,rels_Father,function_infos
#
#     '''建立节点'''

    def create_node(self, label, nodes):
        count = 0
        print("label:",label,"nodes:",nodes)
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            # print(count, len(nodes))
        return

    '''创建知识图谱中心部件的节点'''
#充实每个节点
    def create_functions_nodes(self, function_infos):
        count = 0
        for function_dict in function_infos:
            node = Node("function", name = function_dict['功能名称'], ID=function_dict['功能ID'],
                        description = function_dict['功能描述'], 父功能ID = function_dict['父功能ID'], 部件ID = function_dict['部件ID'])
            self.g.create(node)
            count += 1
            print(count)
        return
#
    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self):
        functions, rels_haveFunction,rels_relevant,rels_Father,function_infos = self.read_nodes()
        self.create_functions_nodes(function_infos)

        return
    #创建该目标的实体
#
#     '''创建实体关系边'''
#
    def create_graphrels(self): #这里调用函数，好像要跟函数create_relationship里的query一一对应
        functions, rels_haveFunction, rels_relevant, rels_Father, function_infos = self.read_nodes()
        # print("部件有：",components)
        # self.create_relationship('target', 'function', rels_haveFunction, 'haveFunction', '拥有功能') #暂时不建立这个关系了
        # self.create_relationship('function', 'component', rels_relevant, 'binding', '关联部件')
        self.create_relationship('function','function',rels_Father,'father','父部件关系')    #头实体是父功能ID
        #match(p:function),(q:functionType) where p.name='T72'and q.name="坦克" create (p)-[r:目标类型.txt]->(q)    直接用这行语句就可以构建关系，对于这些关系，也许可以采取人工手动构建

    '''创建实体关联边'''

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]   #下面这句查询语句中就包括了建立，如果没有建立成功，极大可能是查询匹配的属性没写对导致找不到
            # 关系一：目标与功能间的拥有关系
            # query = "match(p:%s),(q:%s) where p.ID='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            #     start_node, end_node, p, q, rel_type, rel_name)
            # # 关系二：功能与部件间的关联关系
            # query = "match(p:%s),(q:%s) where p.name='%s'and q.ID='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
            #     start_node, end_node, p, q, rel_type, rel_name)
            # #关系三：功能与功能间的父子关系
            query = "match(p:%s),(q:%s) where p.ID='%s'and q.ID='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                # print("Q",query)
                count += 1
                # print(rel_type, count, all)
            except Exception as e:
                print(e)
        return
#
#
if __name__ == '__main__':
    handler = functionGraph()
    handler.read_nodes()
    # print("step1:导入图谱节点中")
    # handler.create_graphnodes()   #在创建其他的边时，这句不运行，否则会创建重复的实体
    print("step2:导入图谱边中")
    handler.create_graphrels()
#
