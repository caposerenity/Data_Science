import json
import time

f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

fp = open('case_data.json', encoding='utf-8')
new_res = fp.read()
new_data = json.loads(new_res)


# return {str} '"%m-%d-%H-%M"'
def timestamp_to_str(timestamp):
    timestamp = int(timestamp * (10 ** (10 - len(str(timestamp)))))
    time_local = time.localtime(timestamp)
    dt = time.strftime("%m-%d-%H-%M", time_local)
    return dt


# param {str} '02-05-20-22'
# return {int} min
def get_time_interval(fir, sec):
    if fir == sec:
        return 0
    fir_time = fir.split("-")
    sec_time = sec.split("-")
    fir_time = list(map(int, fir_time))
    sec_time = list(map(int, sec_time))
    if (fir_time[0] > sec_time[0] or
            (fir_time[0] == sec_time[0] and fir_time[1] > sec_time[1]) or
            (fir_time[0] == sec_time[0] and fir_time[1] == sec_time[1] and fir_time[2] > sec_time[2]) or
            (fir_time[0] == sec_time[0] and fir_time[1] == sec_time[1] and fir_time[2] == sec_time[2] and fir_time[3] >
             sec_time[3])):
        tmp = fir_time
        fir_time = sec_time
        sec_time = tmp
    base = 0
    if sec_time[0] != fir_time[0]:
        base = (29 - fir_time[1]) * 24 * 60
        fir_time[1] = 0
    interval = base + (sec_time[1] - fir_time[1]) * 24 * 60 + (sec_time[2] - fir_time[2]) * 60 + (
            sec_time[3] - fir_time[3])
    return interval


# def get_std_time(min):
#     if (min == 0): return ""
#     res = ["0", "day-", "0", "hour-", "0", "min"]
#     res[0] = str(min // 1440)
#     min %= 1440
#     res[2] = str(min // 60)
#     res[4] = str(min % 60)
#     return "".join(res)


# param : interval(min)
# return {int} score_timeInterval
def getScore_base_interval(interval, id_):
    weighted_score = new_data[id_]["final_score"]
    if interval == 0:
        sco = weighted_score * 0.8
    elif interval <= 10:
        sco = weighted_score * 0.4
    elif 10 < interval <= 30:
        sco = weighted_score * 0.6
    elif 30 < interval <= 90:
        sco = weighted_score * 0.7
    elif 90 < interval <= 300:
        sco = weighted_score * 0.75
    elif 300 < interval <= 600:
        sco = weighted_score * 0.85
    elif 600 < interval <= 1440:
        sco = weighted_score * 0.9
    else:
        sco = weighted_score
    return sco


# param : upload_numbers
# return {int} score_uploadTimes
def getScore_base_numbers(num, id_):
    weighted_score = new_data[id_]["final_score"]
    if num == 0:
        sco = weighted_score * 0.8
    elif num <= 5:
        sco = weighted_score * 0.5
    elif 5 < num <= 10:
        sco = weighted_score * 0.6
    elif 10 < num <= 15:
        sco = weighted_score * 0.7
    elif 15 < num <= 20:
        sco = weighted_score * 0.8
    elif 20 < num <= 40:
        sco = weighted_score * 0.9
    else:
        sco = weighted_score
    return sco


output_dict_user = {}
score = {}
# firstly filtering out cheating cases
for user in data:
    user_id = user["user_id"]
    cases = user["cases"]
    for case in cases:
        case_intervals = []
        case_numbers = []
        case_id = case["case_id"]
        final_score = case["final_score"]
        upload_num = 0
        if case["final_cheat"]:
            score[case_id] = new_data[case_id]["final_score"] * 0.7
        else:
            if not case["upload_records"]:
                # not upload
                first_time = ""
                last_time = first_time
            else:
                # have upload record
                for record in case["upload_records"]:
                    upload_localtime = timestamp_to_str(record["upload_time"])
                    if upload_num == 0:
                        first_time = upload_localtime
                    last_time = upload_localtime
                    upload_num += 1
            score[case_id] = getScore_base_numbers(upload_num, case_id)
            score[case_id] = (
                    score[case_id] + getScore_base_interval(get_time_interval(first_time, last_time), case_id))
            # add item : upload_last_time
            case["upload_first_time"] = first_time
            case["upload_last_time"] = last_time
            case["upload_interval"] = get_time_interval(first_time, last_time)
            case["upload_numbers"] = upload_num
            new_data[case_id]["upload_intervals(min)"].append(case["upload_interval"])
            new_data[case_id]["upload_numbers"].append(case["upload_numbers"])
            new_data[case_id]["average_interval(min)"] += get_time_interval(first_time, last_time)
            new_data[case_id]["average_numbers"] += upload_num
    # print([case_id, last_time, final_score, case["final_cheat"]])
    output_dict_user[user["user_id"]] = user
json_out_ = json.dumps(output_dict_user, ensure_ascii=False, indent=2)
with open('handled_data.json', 'w') as fp:
    fp.write(json_out_)


for id in new_data:
    new_data[id]["upload_intervals(min)"].sort()
    new_data[id]["upload_numbers"].sort()

for k, v in score.items():
    new_data[k]["final_score"] = round((new_data[k]["final_score"] + v / len(new_data[k]["upload_numbers"])), 2)
    new_data[k]["average_numbers"] = round((new_data[k]["average_numbers"] / len(new_data[k]["upload_numbers"])), 2)
    new_data[k]["average_interval(min)"] = round(
        (new_data[k]["average_interval(min)"] / len(new_data[k]["upload_numbers"])), 2)

# get result
json_out = json.dumps(new_data, ensure_ascii=False, indent=2)
with open('case_data.json', 'w') as f:
    f.write(json_out)

# vis
