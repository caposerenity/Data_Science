import json
from statistics import mean

f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))
print(data)

output_dict = {}
user0 = data[2]
sum = 0
caseid = []
print(sum)
for user in data:
    cases = user["cases"]
    print(cases)
    for case in cases:
        if case["case_id"] not in caseid:
            newcase = {}
            newcase["case_point"] = []
            newcase["case_type"] = case["case_type"]
            output_dict[case["case_id"]] = newcase
            caseid.append(case["case_id"])
        else:
            (output_dict[case["case_id"]])["case_point"].append(case["final_score"])
for id in output_dict:
    case = (output_dict[id])
    score20 = 0
    score100 = 0
    sum = 0
    midscore = 0
    num = len(case["case_point"])
    temp = sorted(case["case_point"])
    if (num % 2 == 0):
        midscore = (temp[num // 2] + temp[num // 2 - 1]) / 2
    else:
        midscore = temp[num // 2]
    for score in temp:
        if score < 20:
            score20 += 1
        if score == 100:
            score100 += 1
        sum += score
    average = sum / num
    case["average"] = average
    case["below20"] = score20
    case["fullpoint"] = score100
    case["num"] = num
    case["final_score"] = ((100 - average) / 100 * 0.6 + score20 / num * 0.2 + (num - score100) / num * 0.2) * 100
    case["upload_intervals(min)"] = []
    case["upload_numbers"] = []
    case["average_interval(min)"] = 0
    case["average_numbers"] = 0
print(output_dict)
json_out = json.dumps(output_dict, ensure_ascii=False, indent=2)
with open('case_data.json', 'w') as f:
    f.write(json_out)
