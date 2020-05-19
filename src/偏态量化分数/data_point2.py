import json
import math
from statistics import mean

f = open('handled_data_again.json', encoding='utf8')
res = f.read()
data = json.loads(res)
data = list(dict.values(data))
print(data)

output_dict = {}
user0 = data[2]
sum=0
caseid=[]
print(sum)
for user in data:
    cases = user["cases"]
    print(cases)
    for case in cases:
        if case["case_id"] not in caseid:
            newcase = {}
            newcase["case_point"] = [case["final_score"]]
            newcase["case_type"] = case["case_type"]
            output_dict[case["case_id"]] = newcase
            caseid.append(case["case_id"])
        else:
            (output_dict[case["case_id"]])["case_point"].append(case["final_score"])
for id in output_dict:
    case=(output_dict[id])
    score20=0
    score100=0
    sum=0
    midscore=0
    num=len(case["case_point"])
    temp=sorted(case["case_point"])
    if(num%2==0):
        midscore=(temp[num//2]+temp[num//2-1])/2
    else:
        midscore=temp[num//2]
    for score in temp:
        if score<20:
            score20+=1
        if score==100:
            score100+=1
        sum+=score
    average=sum/num
    dx=0
    for score in temp:
        dx+=(score-average)*(score-average)
    case["case_id"]=id
    case["average"]=average
    case["below20"]=score20
    dx=dx/num
    case["var"]=100
    if case["var"]<0:
        case["var"]=-case["var"]
    case["fullpoint"]=score100
    case["num"]=num
    case["finallevel"]=((100-average)/100*0.6+score20/num*0.2+(num-score100)/num*0.2)*100
    case["upload_intervals"]=[]
    case["upload_numbers"]=[]
    case["u"]=case["var"]/(1-0.25*math.pi)
    case["r"]=100
    if case["r"]<0:
        case["r"]=-case["r"]
    case["case_point"].sort()
    case["case_point"].reverse()
print(output_dict)
json_out=json.dumps(output_dict,ensure_ascii=False,indent=2)
with open('data_point4.json', 'w') as f:
    f.write(json_out)
