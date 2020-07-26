import json


# 对 user_time_data.json 数据进行处理, 将得到的用户特征分析存入"feature_description", 相应的数据存入"feature_data"


# 如果d1的时间比d2早，return true
# 03-24 03-11
def data_compare(d1, d2):
    data_1 = d1.split("-")
    data_2 = d2.split("-")
    if int(data_1[0]) < int(data_2[0]):
        return True
    elif int(data_1[0]) > int(data_2[0]):
        return False
    else:
        if int(data_1[1]) <= int(data_2[1]): return True
    return False


# 用于排序，以小时排序
def take_time(elem):
    ret = int(elem[6:8])
    if 0 <= ret <= 5:
        ret += 24
    return ret


# 获得提交的最晚时间
def get_last_time(times):
    if not times: return 0
    times.sort(key=take_time)
    return times[len(times) - 1]


# 得到两个时间的间隔，单位小时
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
        base = (29 - fir_time[1]) * 24
        fir_time[1] = 0
    interval = base + (sec_time[1] - fir_time[1]) * 24 + (sec_time[2] - fir_time[2]) + (
            sec_time[3] - fir_time[3]) // 60
    return interval


# 用于排序，以日期为key
def take_time_2(elem):
    return int(elem[3:5])


# 判断是否在24小时内完成题目
def is_in_24(times):
    if not times: return False
    times.sort(key=take_time_2)
    if get_time_interval(times[0], times[len(times) - 1]) <= 12: return True
    return False


f = open('user_time_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

fp = open('user_coffee.json', encoding='utf-8')
new_res = fp.read()
new_data = json.loads(new_res)

fpp = open('case_data.json', encoding='utf-8')
case_res = fpp.read()
case_data = json.loads(case_res)

user_cheat_rate = []
for k in data.keys():
    total = 0  # 题目总数
    cheat = 0  # 作弊的题目数
    all_last_upload = []
    no_record = True
    rate_array = {'字符串': 0, '线性表': 0, '数组': 0, '查找算法': 0, '排序算法': 0, '数字操作': 0, '图结构': 0, '树结构': 0}
    for type_ in data[k].keys():
        if type_ == "user_id" or type_ == "feature_data" or type_ == "feature_description":
            continue
        # 统计cheat和total数量
        total += data[k][type_]["total_num"]
        cheat += data[k][type_]["cheat_num"]
        rate_array[type_] = round(100 * data[k][type_]["cheat_num"] / data[k][type_]["total_num"], 2)
        if data[k][type_]["aver_numbers"] == 0.0:
            pass
        else:
            no_record = False

    if no_record:
        # 只有一题，且分数为0，且没有提交记录
        data[k]["feature_data"].append(-1)
        data[k]["feature_description"].append("您在现在的数据中没有任何记录呢")
    else:
        data[k]["feature_data"].append(round(100 * cheat / total, 2))
        data[k]["feature_description"].append("您有" + str(round(cheat * 100 / total, 2)) + "%的题目使用面向用例方法")
        data[k]["feature_data"].append(max(rate_array.values()))
        user_cheat_rate.append(round(100 * cheat / total, 2))
        # 判断哪一题型user面向用例最多
        if data[k]["feature_data"][0] == 0.0:
            data[k]["feature_description"].append("您对所有题目都认真谨慎")
            data[k]["feature_description"].append("希望您能继续保持呢:)")
            data[k]["feature_data"].append(0.0)
            # data[k]["feature_data"].append(0.0)
        else:
            keys = []
            for key, value in rate_array.items():
                if (value == max(rate_array.values())):
                    keys.append(key)
            # 如果有并列第一的情况
            for i in range(len(keys)):
                if i == 0:
                    res = "您在" + keys[i]
                else:
                    res += "、" + keys[i]
            res += "题型中最喜欢面向用例,其中" + str(max(rate_array.values())) + "%使用了面向用例"
            data[k]["feature_description"].append(res)

user_cheat_rate = sorted(user_cheat_rate)
# 判断使用面向用例的能力超过d%的同学
for k in data.keys():
    if data[k]["feature_data"][0] == 0.0 or data[k]["feature_data"][0] == -1:
        pass
    else:
        for i in range(len(user_cheat_rate)):
            if data[k]["feature_data"][0] > user_cheat_rate[i]:
                pass
            else:
                if len(user_cheat_rate) - 1 == i:
                    data[k]["feature_data"].append(100)
                    data[k]["feature_description"].append("使用面向用例的能力位列第一:)")
                else:
                    data[k]["feature_data"].append(round(100 * i / len(user_cheat_rate), 2))
                    data[k]["feature_description"].append(
                        "使用面向用例的能力超过" + str(round(100 * i / len(user_cheat_rate), 2)) + "%的同学:)")
                    break
    # print(data[k]["feature_description"])

# 你在***题型中平均提交次数最多,提交了%次
for k in data.keys():
    all_upload_num = {'字符串': 0, '线性表': 0, '数组': 0, '查找算法': 0, '排序算法': 0, '数字操作': 0, '图结构': 0, '树结构': 0}
    for type_ in data[k].keys():
        if type_ == "user_id" or type_ == "feature_data" or type_ == "feature_description": continue
        all_upload_num[type_] = data[k][type_]["aver_numbers"]
    max_value = max(all_upload_num.values())
    for key in all_upload_num.keys():
        if max_value == all_upload_num[key]:
            data[k]["feature_description"].append("你在" + key + "题型中平均提交次数最多, " + "平均提交了" + str(int(max_value)) + "次")
            data[k]["feature_data"].append(key)
            data[k]["feature_data"].append(max_value)

all_last_day = []
for k in data.keys():
    all_last_upload = {}
    last_day = "02-01"
    for type_ in data[k].keys():
        if type_ == "user_id" or type_ == "feature_data" or type_ == "feature_description":
            continue
        # 统计所有最后一次提交时间
        for t in data[k][type_]["last_upload_times"]:
            if t == "": continue
            all_last_upload[t[0:5]] = 0
        for t in data[k][type_]["last_upload_times"]:
            if t == "": continue
            if data_compare(last_day, t[0:5]): last_day = t[0:5]
            all_last_upload[t[0:5]] += 1
    # print(all_last_upload)
    # 判断早早将代码写完/平均分配每天的代码量/ 在ddl前爆肝作业
    if data[k]["feature_data"][0] == -1: continue
    if data_compare(last_day, "03-24"):
        data[k]["feature_data"].append(1)
        data[k]["feature_description"].append("您喜欢早早将代码写完")
    else:
        more_than_20 = False
        if last_day == "03-31" or last_day == "03-30":
            for key in all_last_upload.keys():
                if (
                        key == "03-24" or key == "03-25" or key == "03-26" or key == "03-27" or key == "03-28" or key == "03-29" or key == "03-30" or key == "03-31"):
                    if all_last_upload[key] >= 20:
                        more_than_20 = True
                        break
        if more_than_20:
            data[k]["feature_data"].append(3)
            data[k]["feature_description"].append("您喜欢在ddl前爆肝作业")
        else:
            data[k]["feature_data"].append(2)
            data[k]["feature_description"].append("您喜欢平均分配每天的代码量")
    # %月%日你完成了所有作业
    data[k]["feature_data"].append(last_day)
    data[k]["feature_description"].append(last_day + "你完成了所有作业")
    all_last_day.append(last_day)

json_out = json.dumps(data, ensure_ascii=False, indent=2)
with open('user_time_data.json', 'w') as f:
    f.write(json_out)

f = open('user_time_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

all_last_day = sorted(all_last_day)
# 您是第几个完成作业的
for k in data.keys():
    if data[k]["feature_data"][0] != -1:
        for i in range(len(all_last_day)):
            if data[k]["feature_data"][4] == all_last_day[i]:
                data[k]["feature_data"].append(i + 1)
                data[k]["feature_description"].append("您是第" + str(i + 1) + "位完成作业的学生")
                break

# 你最喜欢在 上午[1]（5-12）/下午[2]（12-18）/晚上[3]（18-23）/凌晨（23-5）[4]写题目
# %月%日的%点你还在肝代码，小心头发/（没有超过晚上10点的）你从不在晚上写代码，你的头发一定很茂盛（羡慕[0,0,0]）
for k in new_data.keys():
    early_morning = []
    morning = 0
    early = 0
    afternoon = 0
    night = 0
    time_datail = []  # 存储所有时间段
    for case_id in new_data[k].keys():
        if case_id == "user_id": continue
        for time in new_data[k][case_id]:
            time_datail.append(time)
    # 对时间段进行统计
    for time in time_datail:
        if 5 < int(time[6:8]) <= 12:
            morning += 1
        elif 12 < int(time[6:8]) <= 18:
            afternoon += 1
        elif 18 < int(time[6:8]) <= 23:
            night += 1
            early_morning.append(time)
        else:
            early += 1
            early_morning.append(time)
    compare = [early, morning, afternoon, night]
    if max(compare) == early:
        data[k]["feature_description"].append("你最喜欢在凌晨写题目")
        data[k]["feature_data"].append(4)
    elif max(compare) == morning:
        data[k]["feature_description"].append("你最喜欢在上午写题目")
        data[k]["feature_data"].append(1)
    elif max(compare) == afternoon:
        data[k]["feature_description"].append("你最喜欢在下午写题目")
        data[k]["feature_data"].append(2)
    else:
        data[k]["feature_description"].append("你最喜欢在晚上写题目")
        data[k]["feature_data"].append(3)
    last_time = get_last_time(early_morning)
    if last_time == 0:
        data[k]["feature_description"].append("你从不在晚上写代码，你的头发一定很茂盛")
        data[k]["feature_data"].append(0)
    else:
        data[k]["feature_description"].append(
            str(last_time[1:2]) + "月" + str(int(last_time[3:5])) + "日的" + str(int(last_time[6:8])) + "点你还在肝代码，小心头发")
        data[k]["feature_data"].append(last_time)

# 你有d%的题目花费时间不超过1天
for k in new_data.keys():
    total = 0  # 题目总数
    valid = 0  # 一天内完成的题目数
    for case_id in new_data[k].keys():
        if case_id == "user_id": continue
        total += 1
        is_valid = is_in_24(new_data[k][case_id])
        if is_valid: valid += 1
    data[k]["feature_description"].append("你有" + str(round(100 * valid / total, 2)) + "%的题目在一天内完成")
    data[k]["feature_data"].append(round(100 * valid / total, 2))

# 获得难题case_id
high_diff = []
for k in case_data.keys():
    if case_data[k]["final_score"] >= 60:
        high_diff.append(k)
# 你遇到了%题难题，（对于难度系数>40的题目）;有% 的题目你一天把它解决掉;% 的题目是慢慢击破，%的题目没有做出来
# 没遇到难题 None
for k in new_data.keys():
    num_diff = 0  # 遇到的难题数量
    valid_num = 0  # 一天内解决的难题数量
    slow_num = 0  # 慢慢解决难题数量
    unfinished_num = 0  # 没解决的难题数量
    for case_id in new_data[k].keys():
        if case_id == "user_id": continue
        if case_id not in high_diff: continue
        num_diff += 1
        if not new_data[k][case_id]:
            unfinished_num += 1
        else:
            if is_in_24(new_data[k][case_id]):
                valid_num += 1
            else:
                slow_num += 1
    if num_diff == 0:
        data[k]["feature_description"].append("你目前的记录中没有难题")
        data[k]["feature_data"].append(None)
    else:
        data[k]["feature_description"].append(
            "你遇到了" + str(num_diff) + "题较难的题, " + "有" + str(round(100 * valid_num / num_diff, 2)) + "%的题目你一天把它解决掉, " +
            str(round(100 * slow_num / num_diff, 2)) + "%的题目是慢慢击破")
        data[k]["feature_data"].append(num_diff)
        data[k]["feature_data"].append(round(100 * valid_num / num_diff, 2))
        data[k]["feature_data"].append(round(100 * slow_num / num_diff, 2))
    print(data[k]["feature_description"])

json_out = json.dumps(data, ensure_ascii=False, indent=2)
with open('user_time_data.json', 'w') as f:
    f.write(json_out)
