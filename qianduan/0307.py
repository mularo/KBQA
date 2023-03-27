# # from flask import Flask, request, jsonify
# # from neo4j import GraphDatabase
# #
# # app = Flask(__name__)
# # driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=('neo4j', '123456'))
# #
# # # Flask.request_context()
# #
# # @app.route('/get_graph')
# # # @app.before_request
# # def get_graph():
# #     # with app.app_context():  #加了这个还是报错
# #     # with app.test_request_context('/test'):  #加了这个就不报错了
# #     with app.test_request_context('http://localhost:63342/MyKB/qianduan/0307.html?_ijt=6euieug2sipoaem68obc5v5vdv&_ij_reload=RELOAD_ON_SAVE'):  #加了这个就不报错了
# #
# #         node_type = request.args.get('type')
# #         print("node_type",node_type)
# #         with driver.session() as session:
# #             result = session.run(f"MATCH (n:{node_type})-[r]->(m) RETURN n, r, m")
# #             graph_data = []
# #             for record in result:
# #                 graph_data.append({
# #                         'source': record['r'].start_node.id,
# #                         'target': record['r'].end_node.id,
# #                         'label': record['r'].type,
# #                         'source_label': list(record['r'].start_node.labels)[0],
# #                         'target_label': list(record['r'].end_node.labels)[0],
# #                         'source_name': record['r'].start_node.get('name', ''),
# #                         'target_name': record['r'].end_node.get('name', '')
# #                     })
# #         return jsonify(graph_data)
# #
# # if __name__ == '__main__':
# #     graph_data=get_graph()
# #     print(graph_data)
# # # import json
# # #
# # # # 将节点和边数据封装成JSON格式
# # # nodes = [{'id': 1, 'label': 'Node 1'}, {'id': 2, 'label': 'Node 2'}]
# # # edges = [{'id': 1, 'source': 1, 'target': 2, 'label': 'Edge 1'}]
# # # graph_data = {'nodes': nodes, 'edges': edges}
# # #
# # # # 将JSON数据返回给前端页面
# # # json.dumps(graph_data)
# # #
# #
# from flask import Flask, render_template, request
# from neo4j import GraphDatabase
#
# app = Flask(__name__)
# # app = Flask(__name__, template_folder='templates', static_folder='static', debug=True)
# # Set up Neo4j driver
# driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', '123456'))
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/function', methods=['GET','POST'])
# def get_function_graph():
#     with driver.session() as session:
#         # Query Neo4j for function graph
#         result = session.run("MATCH (f:function)-[r]-(o) RETURN f, r, o")
#         # Process result into graph format
#         # ...
#         # Return graph as HTML to display on page
#         return "Function graph"
#
# @app.route('/incident', methods=['GET','POST'])  #这里既要写GET,又要写POST
# def get_incident_graph():
#     with driver.session() as session:
#         # Query Neo4j for incident graph
#         # result = session.run("MATCH (i:incident)-[r]-(o) RETURN i, r, o")
#         # Process result into graph format
#         #处理一下查询代码，测试前端有无反应
#         result = session.run("MATCH (i:incident)-[r]-(o) RETURN i, r, o")
#         print("result",result)
#         # ...
#         # Return graph as HTML to display on page
#         return "Incident graph"    #只能返回字符串才能显示吗？如果想要
#         # return result
# @app.route('/damage_tree', methods=['GET','POST'])
# def get_damage_tree_graph():
#     with driver.session() as session:
#         # Query Neo4j for damage tree graph
#         result = session.run("MATCH (dt:DamageTree)-[r]-(o) RETURN dt, r, o")
#         # Process result into graph format
#         # ...
#         # Return graph as HTML to display on page
#         return "Damage Tree graph"
#
# if __name__ == '__main__':
#     app.run()   #将服务器部署在默认端口，并开始监听请求

from flask import Flask, request, jsonify,render_template
from neo4j import GraphDatabase
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
driver = GraphDatabase.driver('bolt://127.0.0.1:7687', auth=('neo4j', '123456'))
    # #
@app.route('/query',methods=['GET','POST'])
def query_question(question):
    with driver.session() as session:
    # Query Neo4j for incident graph
        print(question)

        result = session.run("MATCH (i:incident)-[r]-(o) WHERE i.name='动力系统' RETURN i, r, o")
        print("result",result)
            # ...
            # Return graph as HTML to display on page
        return f'You asked "{question}"'    #只能返回字符串才能显示吗？如果想要
            # return result
app.run()
# query_question(question)