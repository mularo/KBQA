'''
该文件用于提取csv文件中的数据并进行整理
'''
import json
import pandas as pd
file = open("DATA/3.13.txt", encoding='utf-8')
datas = file.readlines()
for data in datas:
    data = json.loads(data)
    print(data)
    print(type(data))