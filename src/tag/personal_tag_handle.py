import json

f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)
data=list(dict.values(data))
f = open('tags.json', encoding='gbk')
res = f.read()
tags = json.loads(res)

output_dict={}
for user in data:
    output_dict[user["user_id"]]={}
    for case in user["cases"]:
        final_score=case["final_score"]
        if not tags.__contains__(case["case_id"]):
            break
        case_tag=tags[case["case_id"]]["tags"]
        for tag in case_tag:
            if not output_dict[user["user_id"]].__contains__(tag):
                output_dict[user["user_id"]][tag]={}
                output_dict[user["user_id"]][tag]["num"]=1
                output_dict[user["user_id"]][tag]["average"] = final_score
            else:
                n=output_dict[user["user_id"]][tag]["num"]
                ave=output_dict[user["user_id"]][tag]["average"]
                output_dict[user["user_id"]][tag]["average"] = (final_score+ave*n)/(n+1)
                output_dict[user["user_id"]][tag]["num"] += 1
json_out = json.dumps(output_dict, ensure_ascii=False, indent=2)
with open('personal_tag.json', 'w') as f:
    f.write(json_out)
