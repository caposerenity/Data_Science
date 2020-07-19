import json

# 对programming_style_data.json数据进行代码风格评估，结果保存在programming_style_data.json的styles中

f = open('programming_style_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

notes = []
for k1 in data.keys():
    total = 0
    short = 0
    medium = 0
    long = 0
    small = 0
    big = 0
    medium_time = 0
    has_note = 0
    no_note = 0
    not_eng = 0
    for case in data[k1]["cases"].values():
        if case["final_cheat"] or case["no_upload"] or case["final_score"] != 100: continue
        total += 1
        # 分析代码长度
        if float(case["line_rank"][0:3]) <= 30:
            short += 1
        elif float(case["line_rank"][0:3]) >= 70:
            long += 1
        else:
            medium += 1
        # 分析代码时间复杂度
        if float(case["time_rank"][0:3]) <= 30:
            small += 1
        elif float(case["time_rank"][0:3]) >= 70:
            big += 1
        else:
            medium_time += 1
        # 分析注释意识
        if case["note_count"] != 0:
            has_note += 1
        # 非英文命名
        if case["no-english"] != 0:
            not_eng += 1
    # 代码长度
    if short + long < total * 0.3:
        data[k1]["styles"].append("你的代码大都属于一般长度")
    else:
        if total == 0:
            data[k1]["styles"].append("你目前的数据没有有效的代码可以分析代码长度")
        else:
            data[k1]["styles"].append(
                "你的代码" + str(round(short * 100 / total, 2)) + "%比较精简，" + str(round(long * 100 / total, 2)) + "%比较冗长")
    # 时间复杂度
    if big + small < total * 0.3:
        data[k1]["styles"].append("代码的时间复杂度大都属于中等程度")
    else:
        if total == 0:
            data[k1]["styles"].append("你目前的数据没有有效的代码可以分析时间复杂度")
        else:
            data[k1]["styles"].append(
                "代码的时间复杂度" + str(round(small * 100 / total, 2)) + "%较小，" + str(round(big * 100 / total, 2)) + "%较大")
    if big + small > total * 0.3 and total != 0 and small > big:
        data[k1]["styles"].append("看来你python的掌握程度不错 :D")
    else:
        data[k1]["styles"].append("还需要加强对python的掌握程度")
    # 注释意识
    if total == 0:
        notes.append(0)
    else:
        notes.append(round(has_note / total, 2))
    # 非英文命名
    if total == 0:
        data[k1]["styles"].append("你目前的数据没有有效的代码可以分析命名习惯")
    else:
        tmp = round(100 * not_eng / total, 2)
        if tmp > 50:
            data[k1]["styles"].append("你" + str(tmp) + "%的题目中都有非英文命名，要养成良好的命名方式啊")
        elif not_eng == 0:
            data[k1]["styles"].append("你的命名意识非常好，继续保持 :D")
        else:
            data[k1]["styles"].append("你" + str(tmp) + "%的题目中有非英文命名，要加强使用良好的命名方式的意识啊")

# 分析注释意识
notes.sort()
for k1 in data.keys():
    has_note = 0
    total = 0
    for case in data[k1]["cases"].values():
        if case["final_cheat"] or case["no_upload"] or case["final_score"] != 100: continue
        total += 1
        if case["note_count"] != 0:
            has_note += 1
    if total == 0:
        data[k1]["styles"].append("你注释的意识超过0%的同学")
        data[k1]["styles"].append("赶紧培养起注释的习惯吧")
    else:
        tmp = round(notes.index(round(has_note / total, 2)) * 100 / len(notes), 2)
        if tmp < 30:
            data[k1]["styles"].append("你注释的意识超过" + str(tmp) + "%的同学")
            data[k1]["styles"].append("赶紧培养起注释的习惯吧")
        elif tmp > 70:
            data[k1]["styles"].append("你注释的意识超过" + str(tmp) + "%的同学")
            data[k1]["styles"].append("这是一个好习惯，继续保持 :D")
        else:
            data[k1]["styles"].append("你注释的意识超过" + str(tmp) + "%的同学")
            data[k1]["styles"].append("要加强注释的意识哦")

for k1 in data.keys():
    print(data[k1]["styles"])

json_out = json.dumps(data, ensure_ascii=False, indent=2)
with open('programming_style_data.json', 'w') as f:
    f.write(json_out)
