import json
import sys

f = open('problem_data.json', encoding='gbk')
l = f.read()
data=json.loads(l)
output_dict = {}
data=list(dict.values(data))
for problem in data:
    line_count_data=problem["line_count_data"]
    note_count_data=problem["note_count_data"]
    time_count_data=problem["time_use_data"]
    for user in line_count_data:
        if output_dict.__contains__(user["user_id"]):
            temp=output_dict[user["user_id"]]["line_rank"]
            output_dict[user["user_id"]]["line_rank"]=(temp*output_dict[user["user_id"]]["line_count"]+float(user["rank"][:-1]))/(output_dict[user["user_id"]]["line_count"]+1)
            output_dict[user["user_id"]]["line_count"]+=1
        else:
            output_dict[user["user_id"]]={}
            output_dict[user["user_id"]]["line_rank"] = float(user["rank"][:-1])
            output_dict[user["user_id"]]["line_count"] = 1
            output_dict[user["user_id"]]["note_rank"] = 0
            output_dict[user["user_id"]]["note_count"] = 0
            output_dict[user["user_id"]]["time_rank"] = 0
            output_dict[user["user_id"]]["time_count"] = 0

    for user in note_count_data:
        if output_dict.__contains__(user["user_id"]):
            temp = output_dict[user["user_id"]]["note_rank"]
            output_dict[user["user_id"]]["note_rank"] = (temp * output_dict[user["user_id"]]["note_count"] + float(user["rank"][:-1])) / (output_dict[user["user_id"]]["note_count"] + 1)
            output_dict[user["user_id"]]["note_count"] += 1
        else:
            output_dict[user["user_id"]]={}
            output_dict[user["user_id"]]["note_rank"] = float(user["rank"][:-1])
            output_dict[user["user_id"]]["note_count"] = 1
            output_dict[user["user_id"]]["line_rank"] = 0
            output_dict[user["user_id"]]["line_count"] = 0
            output_dict[user["user_id"]]["time_rank"] = 0
            output_dict[user["user_id"]]["time_count"] = 0

    for user in time_count_data:
        if output_dict.__contains__(user["user_id"]):
            temp = output_dict[user["user_id"]]["time_rank"]
            output_dict[user["user_id"]]["time_rank"] = (temp * output_dict[user["user_id"]]["time_count"] + float(user["rank"][:-1])) / (output_dict[user["user_id"]]["time_count"] + 1)
            output_dict[user["user_id"]]["time_count"] += 1
        else:
            output_dict[user["user_id"]]={}
            output_dict[user["user_id"]]["time_rank"] = float(user["rank"][:-1])
            output_dict[user["user_id"]]["time_count"] = 1
            output_dict[user["user_id"]]["note_rank"] = 0
            output_dict[user["user_id"]]["note_count"] = 0
            output_dict[user["user_id"]]["line_rank"] = 0
            output_dict[user["user_id"]]["line_count"] = 0

data=list(dict.values(output_dict))
for user in data:
    user["time_rank"]=str(user["time_rank"])
    if len(user["time_rank"])>5:
        user["time_rank"]=user["time_rank"][:5]+"%"
    else:
        user["time_rank"]+="%"
    user["line_rank"] = str(user["line_rank"])
    if len(user["line_rank"]) > 5:
        user["line_rank"] = user["line_rank"][:5] + "%"
    else:
        user["line_rank"] += "%"
    user["note_rank"]=str(user["note_rank"])
    if len(user["note_rank"])>5:
        user["note_rank"]=user["note_rank"][:5]+"%"
    else:
        user["note_rank"]+="%"
json_out=json.dumps(output_dict,ensure_ascii=False,indent=2)
with open('personal_rank.json', 'w') as f:
    f.write(json_out)