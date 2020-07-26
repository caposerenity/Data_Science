import json

# 获取分析代码风格要用的数据
# 数据保存在programming_style_data.json中

f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)

fp = open('count_data.json', encoding='gbk')
c_res = fp.read()
c_data = json.loads(c_res)

fpp = open('programming_style_data.json', encoding='utf-8')
p_res = fpp.read()
out_data = json.loads(p_res)

# 初始化
# for k in data.keys():
#     output[k] = {"user_id": k, "cases": {},"styles":[]}


for k1 in data.keys():
    user_id = k1
    out_data[k1]["styles"]=[]
    for case in data[k1]["cases"]:
        case_id = case["case_id"]
        lenl = len(case["upload_records"])
        if lenl == 0:
            out_data[user_id]["cases"][case_id] = {"case_id": case_id, "final_cheat": case["final_cheat"],
                                                   "no_upload": True,
                                                   "final_score":case["final_score"],
                                                   "line_count": 0,
                                                   "line_rank": 0, "note_count": 0, "note_rank": 0, "time_use": -1,
                                                   "time_rank": -1,
                                                   "no-english": -1,
                                                   "func-count": -1}
        else:
            out_data[user_id]["cases"][case_id] = {"case_id": case_id, "final_cheat": case["final_cheat"],
                                                   "no_upload": False,
                                                   "final_score": case["final_score"],
                                                   "line_count": 0,
                                                   "line_rank": 0, "note_count": 0, "note_rank": 0, "time_use": -1,
                                                   "time_rank": -1,
                                                   "no-english": case["upload_records"][lenl - 1][
                                                       "not_eng"],
                                                   "func-count": case["upload_records"][lenl - 1][
                                                       "count_func"]}
        # one_out = out_data[user_id]["cases"][case_id]

for c_id in c_data.keys():
    for line in c_data[c_id]["line_count_data"]:
        out_data[str(line["user_id"])]["cases"][c_id]["line_count"]=line["line_count"]
        out_data[str(line["user_id"])]["cases"][c_id]["line_rank"]=line["rank"]
    for note in c_data[c_id]["note_count_data"]:
        out_data[str(note["user_id"])]["cases"][c_id]["note_count"] = note["note_count"]
        out_data[str(note["user_id"])]["cases"][c_id]["note_rank"] = note["rank"]
    for time in c_data[c_id]["time_use_data"]:
        out_data[str(time["user_id"])]["cases"][c_id]["time_use"] = time["time_use"]
        out_data[str(time["user_id"])]["cases"][c_id]["time_rank"] = time["rank"]

for user in out_data.values():
    print(user)

json_out = json.dumps(out_data, ensure_ascii=False, indent=2)
with open('programming_style_data.json', 'w') as f:
    f.write(json_out)
