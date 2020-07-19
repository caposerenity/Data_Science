import json
import sys

f = open('tags.CSV', encoding='gbk')
l = f.readline()
output_dict = {}
type_dict = {}
for i in range(6):
    l = f.readline()
while l != '':
    print(l)
    s = l.split(',')
    if not (s[4] == '' and s[5] == '' and s[6] == ''):
        output_dict[s[0]] = {}
        output_dict[s[0]]['name'] = s[2]
        output_dict[s[0]]['tags'] = []
        if (s[4] != ''):
            output_dict[s[0]]['tags'].append(s[4])
        if (s[5] != ''):
            output_dict[s[0]]['tags'].append(s[5])
        if (s[6] != ''):
            output_dict[s[0]]['tags'].append(s[6])
    if not (s[3] == ''):
        if not type_dict.__contains__(s[3]):
            type_dict[s[3]] = {}
            type_dict[s[3]]['total'] = 0
        for i in range(4, 7):
            if s[i] != '' and type_dict[s[3]].__contains__(s[i]):
                type_dict[s[3]]['total'] += 1
                type_dict[s[3]][s[i]]['num'] += 1
            #                type_dict[s[3]][s[i]]['percent']=type_dict[s[3]][s[i]]['num']/type_dict[s[3]]['total']
            elif s[i] != '':
                type_dict[s[3]][s[i]]={}
                type_dict[s[3]][s[i]]['num'] = 1
                type_dict[s[3]]['total'] += 1
    l = f.readline()
for item in dict.values(type_dict):
    total = item['total']
    for tag in dict.values(item):
        if type(tag)==dict:
            tag['percent']=round(tag['num']/total,3)
json_out = json.dumps(output_dict, ensure_ascii=False, indent=2)
with open('tags.json', 'w') as f:
    f.write(json_out)
json_out = json.dumps(type_dict, ensure_ascii=False, indent=2)
with open('type_tags_count.json', 'w') as f:
    f.write(json_out)
