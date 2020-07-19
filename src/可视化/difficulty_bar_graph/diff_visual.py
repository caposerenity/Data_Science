import matplotlib.pyplot as plt
import pandas as pd
import json
import pylab as pl

fp = open('case_data.json', encoding='utf-8')
res = fp.read()
data = json.loads(res)

# 题目难度条形图的实现, 虚线是平均值, 还在优化中
index_string = []
values_string = []
aver = 0
for k in data.keys():
    if (data[k]["case_type"] == "线性表"):
        index_string.append("")
        values_string.append(data[k]["final_score"])
        aver += data[k]["final_score"]
aver = round(aver / len(values_string), 2)
fig = plt.figure()
data = pd.Series(values_string, index=index_string)  # 调整index得到横坐标
plt.title('Difficulty bar graph for liner table topics')
plt.ylabel('degree of difficulty')
plt.axhline(y=aver, color='y', linestyle='--', label='average')
data.plot.bar(color='b', alpha=0.7)
fig.savefig('线性表难度条形图.png')

fp = open('type_data.json', encoding='utf-8')
res = fp.read()
data = json.loads(res)

index_string = ['string', 'liner table', 'arrays', 'search', 'sort', 'number', 'graph', 'tree']
values_string = []
for k in data.keys():
    values_string.append(data[k]["case_aver_diff"])

fig = plt.figure()
data = pd.Series(values_string, index=index_string)  # 调整index得到横坐标
plt.title('Difficulty bar graph for all topics')
plt.ylabel('degree of difficulty')
data.plot.bar(color='b', alpha=0.7)
fig.subplots_adjust(bottom=0.2)
fig.savefig('所有类型难度条形图.png')
