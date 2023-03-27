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
