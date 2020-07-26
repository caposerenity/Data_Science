import json

# 获取词云图要用的数据

f = open('type_tags_count.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

out_data = {}
for k1 in data.keys():
    for k2 in data[k1].keys():
        if k2 == "total": continue
        out_data[k2] = 0

for k1 in data.keys():
    for k2 in data[k1].keys():
        if k2 == "total": continue
        out_data[k2] += data[k1][k2]["num"]

json_out = json.dumps(out_data, ensure_ascii=False, indent=2)
with open('tag_wordcloud_data.json', 'w') as f:
    f.write(json_out)
