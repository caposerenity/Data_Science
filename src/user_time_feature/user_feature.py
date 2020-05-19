import json

# 还没写完 明天一定 呜呜
# 对 user_time_data.json 数据进行处理, 将得到的用户特征分析存入"feature_description", 相应的数据存入"feature_data"

f = open('user_time_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

user_cheat_rate = []
for k in data.keys():
    total = 0
    cheat = 0
    rate_array = {'字符串': 0, '线性表': 0, '数组': 0, '查找算法': 0, '排序算法': 0, '数字操作': 0, '图结构': 0, '树结构': 0}
    for type_ in data[k].keys():
        if type_ == "user_id" or type_ == "feature_data" or type_ == "feature_description":
            continue
        total += data[k][type_]["total_num"]
        cheat += data[k][type_]["cheat_num"]
        rate_array[type_] = round(100 * data[k][type_]["cheat_num"] / data[k][type_]["total_num"], 2)
    data[k]["feature_data"].append(round(100 * cheat / total, 2))
    data[k]["feature_description"].append("您有" + str(round(cheat * 100 / total, 2)) + "%的题目使用面向用例方法")
    data[k]["feature_data"].append(max(rate_array.values()))
    user_cheat_rate.append(round(100 * cheat / total, 2))
    # 判断哪一题型user面向用例最多
    if data[k]["feature_data"][0]==0.0:
        data[k]["feature_description"].append("您对所有题目都认真谨慎")
        data[k]["feature_description"].append("希望您能继续保持呢:)")
        data[k]["feature_data"].append(0.0)
        data[k]["feature_data"].append(0.0)
    else:
        keys = []
        for key, value in rate_array.items():
            if (value == max(rate_array.values())):
                keys.append(key)
        # 如果有并列第一的情况
        for i in range(len(keys)):
            if i == 0: res = "您在" + keys[i]
            else: res += "、" + keys[i]
        res += "题型中最喜欢面向用例,其中" + str(max(rate_array.values())) + "%使用了面向用例"
        data[k]["feature_description"].append(res)
user_cheat_rate = sorted(user_cheat_rate)
# 判断使用面向用例的能力超过d%的同学
for k in data.keys():
    if data[k]["feature_data"][0]==0.0:
        pass
    else:
        for i in range(len(user_cheat_rate)):
            if data[k]["feature_data"][0] >= user_cheat_rate[i]:
                pass
            else:
                if len(user_cheat_rate)-1 == i:
                    data[k]["feature_data"].append(100)
                    data[k]["feature_description"].append("使用面向用例的能力位列第一:)")
                else:
                    data[k]["feature_data"].append(round(100 * i / len(user_cheat_rate), 2))
                    data[k]["feature_description"].append(
                        "使用面向用例的能力超过" + str(round(100 * i / len(user_cheat_rate), 2)) + "%的同学:)")
                    break
    print(data[k]["feature_description"])

json_out = json.dumps(data, ensure_ascii=False, indent=2)
with open('user_time_data.json', 'w') as f:
    f.write(json_out)
