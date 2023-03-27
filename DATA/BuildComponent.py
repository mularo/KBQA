#这个一键运行即可，运行之前要先运行BuildDamage.py,建立毁伤模式的节点
#要先建立毁伤模式的实体节点,再建立与子部件与毁伤模式的关系，加入其中
# coding: utf-8
'''
#实体类别
1.目标类型.txt  ：有六个实体：飞机、巡航导弹、建筑工事、阵地技术兵器、坦克、工业设施
             属性值有：ID，名称，描述（名称跟描述一样）
2.目标     ：各种具体的目标：F-22，T72   （以目标的名称来建立实体）
（目前就三个F-22,T72,CHE,暂且只建立T72)            属性有ID
3.部件     ：以名称来建立实体
            属性有：ID,名称，描述，材料ID，等效厚度，是否实心，X轴正向等效厚度(mm)，X轴负向等效厚度(mm)
            Y轴正向等效厚度(mm),Y轴负向等效厚度(mm)，Z轴正向等效厚度(mm),Z轴负向等效厚度(mm)
            父部件ID，几何中心x(mm)，几何中心y(mm)，几何中心z(mm),长度(mm),高度(mm),宽度(mm)
            三维模型数据文件，
            毁伤模式编号，毁伤模式名称  ————这个可以不考虑，再关系处再考虑，也可以就在这，便于查询
这里可以考虑单独提取出父部件这个实体类别，然后建立父子关系，或者就作为属性也可以
3.功能    ：以功能名称建立实体，例如：动力系统，传动系统，油箱
            有属性值:ID,名称，描述，父功能ID
4.毁伤    ：共有六种毁伤模式： 1.破孔，2.穿透，3.变形，4.冲击振动，5.引燃，6.引爆
            有属性值：编号，名称，描述
    毁伤等级：K1级毁伤，K2级毁伤，F1级毁伤，F2级毁伤，M1级毁伤，M2级毁伤   ————这之类怎么归结
5.事件     ：是毁伤树中的各个事件
            有名称，ID，
#关系类别：
1.属于关系     目标-目标类型.txt
2.毁伤模式关系   部件-毁伤
3.拥有功能关系   部件-功能
4.事件绑定部件的关系  事件-部件

'''


'''
1.目标类型的实体建立直接建立
2.对3.13.txt文件进行提取，提取出其中的部件，毁伤    ————这个数据主要是针对部件的建立的
'''


import os
import json
from py2neo import Graph, Node,Relationship


class TargetGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, './3.13.txt')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")

#有六种类型对应六种编号 MBLX001、MBLX002、MBLX003、MBLX004、MBLX005、MBLX006  在表中一般都是以编号来识别的
#MB0001- MB0999；巡航导弹类 MB1001-MB1999；建筑工事类 MB2001- MB2999；阵地技术兵器类 MB3001- MB3999；坦克类 MB4001- MB4999；工业设施类 MB5001- MB5999
    '''读取文件'''
#目前只读取了一个文件可用来构建部件实体
    def read_nodes(self):
        # 共5类节点
        # targetTypes = ['飞机','巡航导弹','建筑工事','阵地技术兵器','坦克','工业设施']   #目标类型放在这里构建
        # targets = ['T72','che','F22']  # 目标
        components = []  # 子部件  得到它要根据父部件来剔除
        father_components = []
        component_infos = []  # 部件信息
        # 构建节点实体关系
        rels_belongTo = []  # 子部件-目标   属于关系  这个在后面建立
        rels_father = [] #父部件-子部件
        rels_existDamage = []    #子部件与毁伤模式的关系
        

        count = 0
        for data in open(self.data_path,encoding='utf-8'):
            component_dict = {}
            count += 1
            # print(count)
            data_json = json.loads(data)  #先得到所有信息
            # match(p:target),(q:targetType) where p.name='T72'and q.name="坦克" create (p)-[r:目标类型.txt]->(q)    直接用这行语句就可以构建关系，对于这些关系，也许可以采取人工手动构建
            self.targetID = data_json["目标ID"]
            # print(targetType,type(targetType))
            # print("target",target)
            componentName = data_json['部件名称']    #name    得到部件的名称
            components.append(data_json["部件ID"])    #部件名称填到components里面
            # rels_belongTo.append([component,targetID])   #部件与目标建立属于关系   #这里先不急着加到关系里面去
            component_dict['部件名称'] = componentName    #其实是针对部件的
            # targets.append(component)     #部件的名称保存到列表中
            component_dict['部件ID'] = data_json["部件ID"]
            component_dict['部件描述'] = data_json["部件描述"]
            component_dict['材料ID'] = data_json["材料ID"]
            component_dict['等效厚度'] = data_json["等效厚度(mm)"]
            component_dict['是否实心'] = data_json["是否实心"]
            # component_dict['X轴正向等效厚度(mm)'] = ''
            # component_dict['X轴负向等效厚度(mm)'] = ''
            # component_dict['Y轴正向等效厚度(mm)'] = ''
            # component_dict['Y轴负向等效厚度(mm)'] = ''
            # component_dict['Z轴正向等效厚度(mm)'] = ''
            # component_dict['Z轴负向等效厚度(mm)'] = ''
            component_dict['父部件ID'] = data_json["父部件ID"]
            component_dict['几何中心x(mm)'] = data_json["几何中心x(mm)"]
            component_dict['几何中心y(mm)'] = data_json["几何中心y(mm)"]
            component_dict['几何中心z(mm)'] = data_json["几何中心y(mm)"]
            component_dict['长度(mm)'] = data_json["长度(mm)"]
            component_dict['宽度(mm)'] = data_json["宽度(mm)"]
            component_dict['高度(mm)'] = data_json["高度(mm)"]
            component_dict['三维模型数据文件'] = data_json["三维模型数据文件"]
            component_dict['毁伤模式编号'] = data_json["毁伤模式编号"]
            component_dict['毁伤模式名称'] = data_json["毁伤模式名称"]

#这里每个数据都有，原理是是不需要用if/else的，但是仅是针对这个目标的，所以还是用以下判断

#先建立部件的属性

            if component_dict['是否实心'] == "1":  #1表示实心，0表示空心
                component_dict['是否实心'] = "是"
            else:
                component_dict["是否实心"] = "否"

            # if 'X轴正向等效厚度(mm)' in data_json:
            #     component_dict['X轴正向等效厚度(mm)'] = data_json['X轴正向等效厚度(mm)']
            #
            # if 'X轴负向等效厚度(mm)' in data_json:
            #     component_dict['X轴负向等效厚度(mm)'] = data_json['X轴负向等效厚度(mm)']
            #
            # if 'Y轴正向等效厚度(mm)' in data_json:
            #     component_dict['Y轴正向等效厚度(mm)'] = data_json['Y轴正向等效厚度(mm)']
            #
            # if 'Y轴负向等效厚度(mm)' in data_json:
            #     component_dict['Y轴负向等效厚度(mm)'] = data_json['Y轴负向等效厚度(mm)']
            #
            # if 'Z轴正向等效厚度(mm)' in data_json:
            #     component_dict['Z轴正向等效厚度(mm)'] = data_json['Z轴正向等效厚度(mm)']
            #
            # if 'Z轴负向等效厚度(mm)' in data_json:
            #     component_dict['Z轴负向等效厚度(mm)'] = data_json['Z轴负向等效厚度(mm)']

            if component_dict['父部件ID'] != "" : #如果该部件存在父部件，就把它与父部件之间的关系添加
                rels_father.append([component_dict["父部件ID"],component_dict["部件ID"]]) #都用ID

                if  component_dict["父部件ID"] not in father_components: #如果父部件ID还没有添加到father_components中去，那么就进行添加
                    father_components.append(component_dict["父部件ID"])  # 得到父部件的部件，

                # component_dict['父部件ID'] = data_json['父部件ID']

            if '几何中心x(mm)' in data_json:
                component_dict['几何中心x(mm)'] = data_json['几何中心x(mm)']

            if '几何中心y(mm)' in data_json:
                component_dict['几何中心y(mm)'] = data_json['几何中心y(mm)']

            if '几何中心z(mm)' in data_json:
                component_dict['几何中心z(mm)'] = data_json['几何中心z(mm)']

            if '长度(mm)' in data_json:
                component_dict['长度(mm)'] = data_json['长度(mm)']

            if '宽度(mm)' in data_json:
                component_dict['宽度(mm)'] = data_json['宽度(mm)']

            if '高度(mm)' in data_json:
                component_dict['高度(mm)'] = data_json['高度(mm)']

            if '三维模型数据文件' in data_json:
                component_dict['三维模型数据文件'] = data_json['三维模型数据文件']

            if component_dict['毁伤模式编号'] != [] :   #对于存在毁伤模式的就要建立关系
                print("毁伤模式编号",component_dict['毁伤模式编号'])
                rels_existDamage.append([component_dict["部件ID"],component_dict["毁伤模式编号"]])
                # component_dict['毁伤模式编号'] = data_json['毁伤模式编号']
                #判定使用毁伤模式编号
                component_dict['毁伤模式名称'] = data_json['毁伤模式名称']

            component_infos.append(component_dict)
        # query = "match(p:target),(q:targetType) where p.目标ID='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
        #     target, targetType, "belongsTo", "目标类型.txt")
        # self.g.run(query)  # 要run了才会执行query语句
        # print(query)
        return set(components), father_components,component_infos, rels_father,rels_existDamage

    #set是无重复元素的集合

    '''建立节点'''

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
    def create_targets_nodes(self, father_components,target_infos):
        count = 0
        for component_dict in target_infos:  #所有部件的节点都要建立，只是父部件与子部件的label不一样
            if component_dict["部件ID"] in father_components:
                label = "father_component"
            else:
                label = "component"
            node = Node(label, name=component_dict['部件名称'], ID=component_dict['部件ID'],
                            description=component_dict['部件描述'], 材料ID=component_dict['材料ID'],
                            等效厚度=component_dict['等效厚度'], 是否实心=component_dict['是否实心'],
                            # X轴正向等效厚度=component_dict['X轴正向等效厚度(mm)'], X轴负向等效厚度=component_dict['X轴负向等效厚度(mm)'],
                            # Y轴正向等效厚度=component_dict['Y轴正向等效厚度(mm)'], Y轴负向等效厚度=component_dict['Y轴负向等效厚度(mm)'],
                            # Z轴正向等效厚度=component_dict['Z轴正向等效厚度(mm)'], Z轴负向等效厚度=component_dict['Z轴负向等效厚度(mm)'],
                            父部件ID = component_dict['父部件ID'], 几何中心x = component_dict['几何中心x(mm)'], 几何中心y = component_dict['几何中心y(mm)'],
                            几何中心z=component_dict['几何中心z(mm)'], 长度 = component_dict['长度(mm)'], 宽度 = component_dict['宽度(mm)'], 高度 = component_dict['高度(mm)'],
                            三维模型数据文件 = component_dict['三维模型数据文件'])
            self.g.create(node)
            count += 1
        # print(count)
        return

    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self):
        components, father_components, component_infos,  rels_belongTo, _ = self.read_nodes()
        self.create_targets_nodes(father_components,component_infos)   #这个和 # self.create_node('component', components)是重复的，使用下面这个创建的节点只有name一个属性

        # self.create_node('targetType', self.targetTypes)   #不在这里建立节点，在最开始建立

        return
    #创建该目标的实体

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
            #都是用ID，所有可以共用一条查询语句
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
    #重写一个建立毁伤模式关系的函数，因为传入的数据和查询的语言都不一样
    def create_DamageRelationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理，这里没有用到
        set_edges = []
        for edge in edges:
            p = edge[0]
            q = edge[1]   #下面这句查询语句中就包括了建立，如果没有建立成功，极大可能是查询匹配的属性没写对导致找不到
            #都是用ID，所有可以共用一条查询语句
            for pattern in q:
                query = "match(p:%s),(q:%s) where p.ID='%s'and q.number='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, pattern, rel_type, rel_name)
                try:
                    self.g.run(query)
                    print("Q",query)
                    count += 1
                    # print(rel_type, count, all)
                except Exception as e:
                 print(e)
        return
    def create_graphrels(self):
        components, father_components, components_infos, rels_father, rels_existDamage = self.read_nodes()
        #不属于父部件的部件都与目标建立属于关系
        rels_belongsTo= []
        for com in components:
            if com not in father_components:
                rels_belongsTo.append([com,self.targetID])
                # self.create_relationship("component", "damagePattern", rels_existDamage, "existDamage","存在毁伤")  # 建立存在毁伤关系——只有子部件有吗？
        self.create_DamageRelationship("component", "damagePattern", rels_existDamage, "existDamage","存在毁伤")  # 用的是component.ID和damagePattern.number
        #毁伤模式是一个列表，可能有很多
        self.create_relationship('component', 'target', rels_belongsTo, 'belongsTo', '组成部件')  #建立属于关系
        # print("部件有：",components)            #都用ID
        self.create_relationship('father_component', 'component', rels_father, 'father', '父部件')#建立父子关系
        # self.create_relationship('target', 'targetType', rels_belongTo, 'belongsTo', '目标类型.txt')
        #match(p:target),(q:targetType) where p.name='T72'and q.name="坦克" create (p)-[r:目标类型.txt]->(q)    直接用这行语句就可以构建关系，对于这些关系，也许可以采取人工手动构建



if __name__ == '__main__':
    handler = TargetGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")
    handler.create_graphrels()

