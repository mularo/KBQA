import tkinter as tk
from neo4j import GraphDatabase
from PIL import Image, ImageTk
from py2neo import Graph, Node
import jieba
class QASystemUI:
    def __init__(self, driver):
#安装的py2neo为新版本，用新的写法
        self.g = Graph('http://localhost:7474/', auth=("neo4j", "123456"))
        self.driver = driver

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Question-Answering System")

        # Set the window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1200
        window_height = 800
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Set the background to an image of a tank
        image_path = "D:/jupyter-code/T72.jpg"
        image = Image.open(image_path)
        print(image)
        image = image.resize((window_width, window_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.root, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        # Set the system name label
        system_name = tk.Label(self.root, text="目标易损性问答系统", font=("Arial", 24), bg="#FFFFFF")
        system_name.place(relx=0.5, rely=0.1, anchor="center")

        # Create the question label and entry
        tk.Label(self.root, text="请输入您的问题:", font=("Arial", 16), bg="#FFFFFF").place(relx=0.5, rely=0.3, anchor="center")
        self.question_entry = tk.Entry(self.root, width=50, font=("Arial", 14))
        self.question_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Create the answer label
        self.answer_label = tk.Label(self.root, text="", font=("Arial", 16), bg="#FFFFFF")
        self.answer_label.place(relx=0.5, rely=0.6, anchor="center")

        # Create the submit button
        tk.Button(self.root, text="提交", command=self.submit_question, font=("Arial", 16)).place(relx=0.5, rely=0.8, anchor="center")

    def submit_question(self):
#         pass
        question_text = self.question_entry.get()
#分词并输出分词后的结果
        words = jieba.lcut(question_text)
        print(words)
        jiebawords = tk.Label(self.root, text="问句分词后的结果是："+ str(words), font=("Arial", 16), bg="#FFFFFF")
#         self.question_entry = tk.Entry(self.root, width=50, font=("Arial", 14))
        jiebawords.place(relx=0.5, rely=0.5, anchor="center")
#query
        query = "MATCH (a:target) WHERE a.name='T72'  RETURN a.目标速度"
        result = self.g.run(query).data()  #.data()将查询到的结果转化为了列表的形式，列表元素是字典，字典的key是属性名称，value是属性值
#         print("resultsType: ",type(re))
        print("results:",result)
#         print(result[0].keys())
#         # Query the database using the Neo4j driver
#         with self.driver.session() as session:
#             result = session.run("MATCH (a:target) WHERE a.name='T72'  RETURN a.目标速度")
#             print("result:",result)
#         # Display the answer in the UI
        answer = [record["a.目标速度"] for record in result]
        print("answer",answer)
#         self.answer_label.config(text=answer[0])
        if answer:
            self.answer_label.config(text="T72的速度参考是："+ answer[0])
        else:
            self.answer_label.config(text="对不起，您的问题超过了我的知识范围.")

# # Connect to the Neo4j database using the driver
driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "123456"))

# # Create the UI object and start the application
ui = QASystemUI(driver)
ui.root.mainloop()
