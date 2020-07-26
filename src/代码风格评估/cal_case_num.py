import json

# 计算某一用户现在数据中的case数量

f = open('programming_style_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

print(len(data["60618"]["cases"]))


