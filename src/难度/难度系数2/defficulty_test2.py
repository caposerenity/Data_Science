import json

f = open('../difficulty_origin_data.json', encoding='gb18030')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))
print(data)

scoreRate = 0.65
timeRate = 0.35
acRate = 0.383
oneARate = 0.317
averageRate = 0.3
debugRate = 0.55
submitRate = 0.45

output_dict = {}


def cal_difficulty(ac, oneAC, average, debug, submit):
    score_temp = scoreRate * ((1 - ac) * acRate + (1 - oneAC) * oneARate + (1 - average / 100) * averageRate)
    debug=handle_debug(debug)
    submit=handle_submit(submit)
    time_temp = timeRate * (debug*debugRate + submitRate * submit)
    return (score_temp + time_temp) * 100


def handle_debug(debug):
    if debug == 0:
        return 0.8
    elif debug <= 10:
        return 0.4
    elif debug <= 30:
        return 0.6
    elif debug <= 90:
        return 0.7
    elif debug <= 300:
        return 0.75
    elif debug <= 600:
        return 0.85
    elif debug <= 1400:
        return 0.9
    else:
        return 1


def handle_submit(submit):
    if submit == 0:
        return 0.8
    elif submit <= 5:
        return 0.5
    elif submit <= 10:
        return 0.6
    elif submit <= 15:
        return 0.7
    elif submit <= 20:
        return 0.8
    elif submit <= 40:
        return 0.9
    else:
        return 1


for case in data:
    case["final_level"] = cal_difficulty(float(case["AC_rate"]), float(case["1A_rate"]), float(case["average"]),
                                         float(case["average_interval(min)"]), float(case["average_numbers"]))
    case.pop('final_score')
    case.pop('below20')
    case.pop('case_point')
    case.pop('1A_case')
    case.pop('upload_intervals(min)')
    case.pop('upload_numbers')
    case.pop('fullpoint')
    output_dict[case["case_id"]] = case

json_out = json.dumps(output_dict, ensure_ascii=False, indent=2)
with open('difficulty_test2.json', 'w') as f:
    f.write(json_out)
