import json

f = open('user_type_data.json', encoding='gb18030')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))
print(data)

scoreRate = 0.6
timeRate = 0.4
acRate = 0.383
oneARate = 0.3
averageRate = 0.317
debugRate = 0.4
timeComRate=0.3
logicComRate=0.3

output_dict = {}


def cal_difficulty(ac, oneAC, average, debug, time,logic):
    score_temp = scoreRate * ((ac) * acRate + (oneAC) * oneARate + (average / 100) * averageRate)
    debug=1-handle_debug(debug)
    if time==-1:
        time=10
    time=1-time/10
    logic=1-logic/10
    time_temp = timeRate * (debug*debugRate + time * timeComRate+logic*logicComRate)
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
type=["字符串","线性表","数组","查找算法",'排序算法','数字操作',"树结构","图结构"]
output={}
for user in data:
    for t in type:
        user[t]["capability"]=cal_difficulty(user[t]["AC"],user[t]["1A"],user[t]["quantified_score"],user[t]["upload_interval"],user[t]["time_complication"],user[t]["logic_complication"])
    output[user["user_id"]]=user
json_out = json.dumps(output, ensure_ascii=False, indent=2)
with open('capability.json', 'w') as f:
    f.write(json_out)