import json
import time


# 注意：先跑user_time_analysis.py 再跑user_feature.py
# 生成 user_time_data.json : 储存用户有关时间的所有数据, 以user_id为key, 并对题目类型进行分类
# 生成 user_coffee.json : 储存用户所有题目上传时间记录
# 生成 type_data.json : 以题目类型进行分类的所有数据

# return {str} '"%m-%d-%H-%M"'
def timestamp_to_str(timestamp):
    timestamp = int(timestamp * (10 ** (10 - len(str(timestamp)))))
    time_local = time.localtime(timestamp)
    dt = time.strftime("%m-%d-%H-%M", time_local)
    return dt


f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

# 生成user_time_data.json
out_dict = {}
out_coffee = {}
for user in data:
    user_id = user["user_id"]
    cases = user["cases"]
    out_dict[user_id] = {'user_id': user_id, "feature_data": [], "feature_description": []}
    out_coffee[user_id] = {"user_id": user_id}
    for case in cases:
        out_dict[user_id][case["case_type"]] = {"type": case["case_type"], "total_num": 0, "cheat_num": 0,
                                                "valid_num": 0,
                                                "case_id": [],
                                                "first_upload_times": [], "last_upload_times": [], 'intervals(min)': [],
                                                "upload_nums": [], "aver_intervals(min)": 0, "aver_numbers": 0,
                                                "count_lines": []}
        out_coffee[user_id][case["case_id"]] = []
for user in data:
    user_id = user["user_id"]
    cases = user["cases"]
    for case in cases:
        # user_coffee
        for record in case["upload_records"]:
            out_coffee[user_id][case["case_id"]].append(timestamp_to_str(record["upload_time"]))
        # user_time_data
        type = out_dict[user_id][case["case_type"]]
        if (case["final_cheat"]):
            type["cheat_num"] += 1
            type["total_num"] += 1
        else:
            type["valid_num"] += 1
            type["total_num"] += 1
            type["case_id"].append(case["case_id"])
            type["first_upload_times"].append(case["upload_first_time"])
            type["last_upload_times"].append(case["upload_last_time"])
            type["intervals(min)"].append(case["upload_interval"])
            type["upload_nums"].append(case["upload_numbers"])
            type["aver_numbers"] += case["upload_numbers"]
            type["aver_intervals(min)"] += case["upload_interval"]
    for case_ty in out_dict[user["user_id"]].keys():
        if case_ty == "user_id" or case_ty == "feature_data" or case_ty == "feature_description": continue
        if len(out_dict[user["user_id"]][case_ty]["upload_nums"]) == 0: continue
        out_dict[user["user_id"]][case_ty]["aver_numbers"] /= len(out_dict[user["user_id"]][case_ty]["upload_nums"])
        out_dict[user["user_id"]][case_ty]["aver_intervals(min)"]/=len(out_dict[user["user_id"]][case_ty]["upload_nums"])

for k, v in out_dict.items():
    print(v)
json_out = json.dumps(out_dict, ensure_ascii=False, indent=2)
with open('user_time_data.json', 'w') as f:
    f.write(json_out)

json_out = json.dumps(out_coffee, ensure_ascii=False, indent=2)
with open('user_coffee.json', 'w') as f:
    f.write(json_out)

f = open('case_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

# 生成type_case.json
types = ['字符串', '线性表', '数组', '查找算法', '排序算法', '数字操作', '图结构', '树结构']
out_dict = {'字符串': {}, '线性表': {}, '数组': {}, '查找算法': {}, '排序算法': {}, '数字操作': {}, '图结构': {}, '树结构': {}}
for k, v in out_dict.items():
    v = {"case_type": k, "case_num": 0, "case_aver_diff": 0, "cases": {}}
    out_dict[k] = v
for k in data.keys():
    out_dict[data[k]["case_type"]]["case_num"] += 1
    out_dict[data[k]["case_type"]]["cases"][k] = data[k]
    out_dict[data[k]["case_type"]]["case_aver_diff"] += data[k]["final_score"]
for type in types:
    out_dict[type]["case_aver_diff"] = round(out_dict[type]["case_aver_diff"] / out_dict[type]["case_num"], 2)

json_out = json.dumps(out_dict, ensure_ascii=False, indent=2)
with open('type_data.json', 'w') as f:
    f.write(json_out)
