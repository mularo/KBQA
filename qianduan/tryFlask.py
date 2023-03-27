from flask import Flask, render_template, request
from neo4j import GraphDatabase, basic_auth

app = Flask(__name__,template_folder="tTemplatess")

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "123456"))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    # query = request.form['query']
    query = f"MATCH (n:function) WHERE n.父功能ID=n.部件ID RETURN n.name"
    with driver.session() as session:
        result = session.run(query)
        data = result.data()

    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
    # query()