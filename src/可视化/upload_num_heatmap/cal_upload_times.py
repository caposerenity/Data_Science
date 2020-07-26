import json
# 计算某一用户提交的总次数
f = open('calendar_heat_map.json', encoding='utf-8')
new_res = f.read()
new_data = json.loads(new_res)

res=0
for val in new_data["60618"].values():
    res+=val

print(res)
