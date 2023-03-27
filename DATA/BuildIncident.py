'''一键运行即可'''
import json
# f = open("./4.txt","r",encoding='utf-8')
# lines = f.readlines()
# function = []
# for line in lines:
#     line = json.loads(line)
#     fun = line["功能名称"]
#     # print(fun)
#     function.append(fun)
# print("function有：",len(function),"个")
# f2 = open("./6.2.txt","r",encoding="utf-8")
# lines2 = f2.readlines()
# incidents = []
# for line2 in lines2:
#     line2 = json.loads(line2)
#     inci = line2["事件名称"]
#     # print(inci)
#     incidents.append(inci)
# print("事件有：",len(incidents),"个")
# all = function+incidents
# # print(all)
# # for a in all:
# #     if a in function:
# #         pass
# #     if a in incidents:
# #         pass
# #     else:
# #         print(a)
# #需要查看事件是否只与子部件关联——确实是
# #父功能和父部件之间的关系呢
# #   父部件有没有功能呢？  作为父功能的功能是不对应部件的，也存在不是父功能的功能不对应部件，例如”油箱“
# fathercom = ["油箱","烟幕发射器","辅助武器","主动轮","履带","托带轮","诱导轮","负重轮","悬挂装置","车体","炮塔"]
# for a in incidents:
#     if a in fathercom:
#         print(a)
#
#这个要分四次创建关系
'''用来提取功能实体类型的py文件'''
import codecs
import csv
import json
import os
from py2neo import Graph, Node

#建立毁伤等级的实体，与目标类型建立关系
'''读取并提取csv数据，程序运行前利用csv文件得到txt文件'''
# fw = open("6.2.txt",'w',encoding = 'utf-8')
# with codecs.open('6.2.csv', 'r', encoding='utf-8') as fp:
#     fp_key = csv.reader(fp)  #所有列名，相当于得到了key
#     for csv_key in fp_key:
#         # print('字典的key值：%s' % csv_key)
#         csv_reader = csv.DictReader(fp, fieldnames=csv_key)#按列名读取每一行的每一列（即键值）
#         # print('DictReader()方法返回值：%s' % csv_reader)
#         for row in csv_reader:
#             csv_dict = dict(row)
#             print(type(csv_dict),csv_dict)
#             json.dump(csv_dict,fw,ensure_ascii=False)
#             fw.write("\n")
# fw.close()

class incidentGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, '6.2.txt')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")

    '''读取文件'''

    # 从该文件中可以提取出一类实体：事件     四类关系（和前面的有重合）
    def read_nodes(self):
        rels_and = []  # 与关系
        rels_or = []  # 或关系

        count = 0
        number = 0
        trees = []
        incidentOfTree = []
        for data in open(self.data_path, encoding='utf-8'):
            count += 1
            # print(count)
            data_json = json.loads(data)
            if data_json["上级事件ID"] == "" :
                # trees.append(incidentOfTree)  #在最开始清空毁伤树的列表
                incidentOfTree = []  #遇到一个顶层事件就将保存这棵树的事件列表清空
                number = number + 1
            incident_dict = {}
            # incident = data_json['事件名称']  # 得到事件名称，作为实体上的name
            # incidents.append(incident)       #事件加入到incidents里面
            targetID = data_json['目标ID']  # 得到该功能属于的目标ID，用于之后建立关系1
            # match(p:incident),(q:incidentType) where p.name='T72'and q.name="坦克" create (p)-[r:目标类型.txt]->(q)    直接用这行语句就可以构建关系，对于这些关系，也许可以采取人工手动构建

            # print(incidentType,type(incidentType))
            # print("incident",incident)
            incident_dict['事件名称'] = data_json['事件名称']
            incident_dict['事件ID'] = data_json['事件ID']
            incident_dict['事件类型'] = data_json['事件类型']  #事件类型作为属性
            incident_dict['事件描述'] = data_json['事件描述']
            incident_dict['上级事件ID'] = data_json['上级事件ID']
            incident_dict['部件ID'] = data_json['部件ID']
            incident_dict['毁伤等级ID'] = data_json['毁伤等级ID']
            incident_dict['毁伤模式编号'] = data_json['毁伤模式编号']
            incident_dict['备注'] = data_json['备注']
            incident_dict['位置X'] = data_json['位置X']
            incident_dict['位置Y'] = data_json['位置Y']
            incident_dict['k'] = data_json['k']
            incident_dict['n'] = data_json['n']

            incidentOfTree.append(incident_dict)  #一棵树里的事件
            if data_json["上级事件ID"] == "" :
                trees.append(incidentOfTree)  #在最后把一棵毁伤树的所有事件加进去
                # incidentOfTree = []  #
                # number = number+1


#都统一用事件ID

            # incident_infos.append(incident_dict)
            # print(incident_dict)

        return  trees,number

    def getAtree(self):
        # superIncident
        incident_infos = self.read_nodes()
        for incident in incident_infos:
            if incident["上级事件ID"] == "" : #d顶层事件
                superIncident = incident
                relation = incident["事件类型"]  #顶层事件与中间事件的关系
            # if incident["上级事件ID"] = "SJ000":   #中间事件可能有多个
            #     mediaIncident =

                # print(incident["事件名称"])


    #
    #     '''建立节点'''
    #
    # def create_node(self, label, nodes):
    #     count = 0
    #     print("label:", label, "nodes:", nodes)
    #     for node_name in nodes:
    #         node = Node(label, name=node_name)
    #         self.g.create(node)
    #         count += 1
    #         # print(count, len(nodes))
    #     return
    #
    # '''创建知识图谱中心部件的节点'''
    #
    # # 充实每个节点
    def create_incidents_nodes(self, incident_dict):
        count = 0
        node = Node("incident",TREE = incident_dict['TREE'], name=incident_dict['事件名称'], ID=incident_dict['事件ID'], 事件类型=incident_dict['事件类型'],
                        description =incident_dict['事件描述'], 部件ID=incident_dict['部件ID'],number=incident_dict['毁伤模式编号'], 备注=incident_dict['备注'],
                        位置X=incident_dict['位置X'], 位置Y=incident_dict['位置Y'], k=incident_dict['k'], n=incident_dict['n'])
        self.g.create(node)
        count += 1
        # print(count)
        return
    #
    # #
    # '''创建知识图谱实体节点类型schema'''
    #
    # def create_graphnodes(self):
    #     incidents, rels_super, rels_relevant, rels_exitDamage, rels_haveDamage, incident_infos = self.read_nodes()
    #     self.create_incidents_nodes(incident_infos)
    #
    #     return
    #
    # # 创建该目标的实体
    # #     '''创建实体关系边'''
    # def create_graphrels(self):
    #     incidents, rels_super, rels_relevant, rels_exitDamage, rels_haveDamageGrade, incident_infos = self.read_nodes()
    #     # print("部件有：",components)
    #     self.create_relationship('incident', 'incident', rels_super, 'superIncident', '上级事件')
    #     self.create_relationship('incident', 'component', rels_relevant, 'relevant', '事件与部件的关联关系')
    #     self.create_relationship('component', 'damagePattern', rels_exitDamage, 'existDamage', '部件存在毁伤模式')  #
    #     self.create_relationship('incident', 'damageGrade', rels_haveDamageGrade, 'haveDamageGrade', '事件有毁伤等级')  # ID
    #
    #     # match(p:incident),(q:incidentType) where p.name='T72'and q.name="坦克" create (p)-[r:目标类型.txt]->(q)    直接用这行语句就可以构建关系，对于这些关系，也许可以采取人工手动构建
    #
    # '''创建实体关联边'''
    #
    # def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
    #     count = 0
    #     # 去重处理
    #     set_edges = []
    #     for edge in edges:
    #         set_edges.append('###'.join(edge))
    #     all = len(set(set_edges))
    #     for edge in set(set_edges):
    #         edge = edge.split('###')
    #         p = edge[0]
    #         q = edge[1]  # 下面这句查询语句中就包括了建立，如果没有建立成功，极大可能是查询匹配的属性没写对导致找不到
    #         # # 1.事件之间的上下级关系
    #         # query = "match(p:%s),(q:%s) where p.事件ID='%s'and q.事件ID='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
    #         #     start_node, end_node, p, q, rel_type, rel_name)
    #         # 2.事件与部件的关联关系
    #         # query = "match(p:%s),(q:%s) where p.事件ID='%s'and q.部件ID='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
    #         #     start_node, end_node, p, q, rel_type, rel_name)
    #         # 3.部件与毁伤模式关系 --存在
    #         # query = "match(p:%s),(q:%s) where p.部件ID='%s'and q.毁伤模式编号='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
    #         #     start_node, end_node, p, q, rel_type, rel_name)
    #         # # 4.事件与毁伤等级的属于关系  rels_haveDamageGrade
    #         query = "match(p:%s),(q:%s) where p.事件ID='%s'and q.毁伤等级ID='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
    #             start_node, end_node, p, q, rel_type, rel_name)
    #         try:
    #             self.g.run(query)
    #             # print("Q",query)
    #             count += 1
    #             # print(rel_type, count, all)
    #         except Exception as e:
    #             print(e)
    #     return
    def createTree(self,trees):
        flag=0
        count=0
        for tree in trees:  # 每一个tree是一个毁伤树里的所有事件
            flag += 1
            # SETIncidents = []  #用来保存所有的事件的名称，在创建节点前用于判断，如果已经存在那就不再创建相同名称的节点
            # print(len(tree), tree)
            # 其实不用这么麻烦的判断，因为整理数据时就把顶层事件放在第一个    ——顶事件在这里处理
            SUPERincident = tree[0]       #顶层事件，字典类型
            SUPERincident['TREE'] = flag
            SUPERincidentName = SUPERincident["事件名称"]
            SUPERrelation = SUPERincident['事件类型']
            SUPERincidentID = SUPERincident['事件ID']
            # 创建该树的顶层节点
            incident_dict = {}
            incident_dict[SUPERincidentID]=SUPERincidentName   #保存ID和name就行，键为ID，值为name
            handler.create_incidents_nodes(SUPERincident)    ######尝试的时候不重复构建节点
            rel = []  # 添加关系对[事件，上级事件，事件类型]

            for i in range(1, len(tree)):
                incident = tree[i]
                # 创建事件节点
                incident["TREE"] = flag
                incidentID = incident['事件ID']
                incident_dict[incidentID] = incident["事件名称"]
                # ID_NAME.append(incident_dict)
                # if incident["事件名称"] in SETIncidents:
                #     pass
                # else:
                # SETIncidents.append(incident["事件名称"])
                handler.create_incidents_nodes(incident)   #不重复构建节点
                if incident["事件类型"] != "":  # 说明是中间事件  要完成两件事：1.与顶层事件建立关系，2.设定它与下一层事件间的关系relation
                    relation = incident["事件类型"]  #这个关系是中间事件的底事件与其的关系
                    rel.append([incident['事件名称'], SUPERincidentName, SUPERrelation])
                else:  # 底事件只需要与上级事件建立联系,
                    ID = incident["上级事件ID"]
                    superNAME = incident_dict[ID]

                    rel.append([incident['事件名称'], superNAME, relation])
                #建立事件与部件的关联关系binding
                # print(incident['部件ID'])
                query = "match(p:incident),(q:component) where p.部件ID=q.ID merge (p)-[rel:binding {name:'事件关联部件'}]->(q)" #%(incident['部件ID'], incident['部件ID'])
                try:
                    self.g.run(query)
                    count = count+1
                    print(count)
                    print("Q", query)
                except Exception as e:
                    print(e)

            # 一棵树搞完了，建立该树中的关键节点,用
            print("--------------------")
            for r in rel:
                # count +=1
                if r[2] == '与':    #
                    query = "match(p:incident),(q:incident) where p.name='%s'and q.name='%s' and p.TREE=q.TREE merge (p)-[rel:and {name:'and'}]->(q)" % (
                        r[0], r[1])
                elif r[2] == '或':
                    query = "match(p:incident),(q:incident) where p.name='%s'and q.name='%s' and p.TREE=q.TREE merge (p)-[rel:or {name:'or'}]->(q)" % (
                        r[0], r[1])
                try:
                    self.g.run(query)
                    print("Q",query)
                    count += 1
                    # print(rel_type, count, all)
                except Exception as e:
                    print(e)
            #     print(count,r[2],r)


if __name__ == '__main__':
    handler = incidentGraph()
    trees, number = handler.read_nodes()
    handler.createTree(trees)


    # print(trees)
    print(number)
    # print("step1:导入图谱节点中")
    # handler.create_graphnodes()   #在创建其他的边时，这句不运行，否则会创建重复的实体
    # print("step2:导入图谱边中")
    # handler.create_graphrels()
#
