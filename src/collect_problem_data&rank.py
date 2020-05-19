import json
import os
import urllib.parse, urllib.request

f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))
f1 = open('problem_data.json', encoding='gbk')
res = f1.read()
problem_data = json.loads(res)

for name, data_for_rank in problem_data.items():
    problem_data[name]["line_count_data"] = []
    problem_data[name]["note_count_data"] = []
    problem_data[name]["time_use_data"] = []

for user in data:
    cases = user["cases"]
    for case in cases:
        if case["final_score"] == 100:
            print(case["case_id"], case["case_type"])
            num = 0
            line_count = 0
            note_count = 0
            time_use = 0
            problem_name = ""
            for record in case["upload_records"]:
                filename = urllib.parse.unquote(os.path.basename(record["code_url"]))
                problem_name = filename.split('_')[0]

                if record["score"] == 100:
                    line_count = (line_count * num + record["count_line"]) / (num + 1)
                    note_count = (note_count * num + record["note_line"]) / (num + 1)
                    time_use = (time_use * num + record["time_use"]) / (num + 1)
                    num += 1
            problem_data[problem_name]["line_count_data"].append({"user_id": user["user_id"], "line_count": line_count})
            problem_data[problem_name]["note_count_data"].append({"user_id": user["user_id"], "note_count": note_count})
            problem_data[problem_name]["time_use_data"].append({"user_id": user["user_id"], "time_use": time_use})

for name, data_for_rank in problem_data.items():
    data_for_rank["line_count_data"].sort(key=lambda k: k["line_count"])
    before = -1
    before_rank = ""
    for one_user_data in data_for_rank["line_count_data"]:
        one_user_data["rank"] = data_for_rank["line_count_data"].index(one_user_data) / (
            data_for_rank["line_count_data"].__len__())
        one_user_data["rank"] = round(one_user_data["rank"], 5)
        one_user_data["rank"] = str(one_user_data["rank"] * 100) + "%"
        if one_user_data["line_count"] == before:
            one_user_data["rank"] = before_rank
        before = one_user_data["line_count"]
        before_rank = one_user_data["rank"]

    data_for_rank["note_count_data"].sort(key=lambda k: k["note_count"], reverse=True)
    before = -1
    before_rank = ""
    for one_user_data in data_for_rank["note_count_data"]:
        one_user_data["rank"] = data_for_rank["note_count_data"].index(one_user_data) / (
            data_for_rank["note_count_data"].__len__())
        one_user_data["rank"] = round(one_user_data["rank"], 5)
        one_user_data["rank"] = str(one_user_data["rank"] * 100) + "%"
        if one_user_data["note_count"] == before:
            one_user_data["rank"] = before_rank
        before = one_user_data["note_count"]
        before_rank = one_user_data["rank"]

    data_for_rank["time_use_data"].sort(key=lambda k: k["time_use"])
    before = -1.5
    before_rank = ""
    for one_user_data in data_for_rank["time_use_data"]:
        one_user_data["rank"] = data_for_rank["time_use_data"].index(one_user_data) / (
            data_for_rank["time_use_data"].__len__())
        one_user_data["rank"] = round(one_user_data["rank"], 5)
        one_user_data["rank"] = str(one_user_data["rank"] * 100) + "%"
        if one_user_data["time_use"] == before:
            one_user_data["rank"] = before_rank
        before = one_user_data["time_use"]
        before_rank = one_user_data["rank"]

json_out = json.dumps(problem_data, ensure_ascii=False, indent=2)
with open('problem_data.json', 'w') as f:
    f.write(json_out)
