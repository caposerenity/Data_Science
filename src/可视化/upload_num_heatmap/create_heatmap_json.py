import json

# 生成calendar_heat_map。json 里面包括cheat的提交记录，因为只作为学生的行为分析，不作为能力考察中
fp = open('user_coffee.json', encoding='utf-8')
res = fp.read()
data_ = json.loads(res)

f = open('calendar_heat_map.json', encoding='utf-8')
new_res = f.read()
new_data = json.loads(new_res)

for k in new_data.keys():
    for t in new_data[k].keys():
        new_data[k][t] = 0

for k in data_.keys():
    for case_id in data_[k].keys():
        if (case_id == "user_id"):
            pass
        else:
            for time in data_[k][case_id]:
                new_data[k][time] += 1

json_out = json.dumps(new_data, ensure_ascii=False, indent=2)
with open('calendar_heat_map.json', 'w') as f:
    f.write(json_out)
