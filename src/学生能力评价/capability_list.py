import json

f = open('capability.json', encoding='gb18030')
res = f.read()
data = json.loads(res)
data=list(dict.values(data))
print(data)
output={}
type=["字符串","线性表","数组","查找算法",'排序算法','数字操作',"树结构","图结构"]
for user in data:
    temp={}
    temp["user_id"]=user["user_id"]
    temp["capability"]=[]
    temp["score"]=[]
    for t in type:
        temp["capability"].append(user[t]["capability"])
        temp["score"].append(user[t]["quantified_score"])
    output[user["user_id"]]=temp
    print(user)
json_out = json.dumps(output, ensure_ascii=False, indent=2)
with open('capability_list.json', 'w') as f:
    f.write(json_out)