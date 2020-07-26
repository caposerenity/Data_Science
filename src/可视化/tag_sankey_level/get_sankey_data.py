import json

# 处理得到桑葚图要用的数据

f = open('type_tags_count.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

total = 0
nodes = []
out_data = {"nodes": [{"name": "Total"}], "links": []}

# 获取nodes
for k1 in data.keys():
    if k1 not in nodes:
        nodes.append(k1)
        out_data["nodes"].append({"name": k1})

for k1 in data.keys():
    total += data[k1]["total"]
    for k2 in data[k1].keys():
        if k2 not in nodes and k2 != "total":
            nodes.append(k2)
            out_data["nodes"].append({"name": k2})

# 获取links
for k1 in data.keys():
    out_data["links"].append({"source": "Total", "target": k1, "value": data[k1]["total"] / total})
for k1 in data.keys():
    for k2 in data[k1].keys():
        if k2 == "total": continue
        out_data["links"].append({"source": k1, "target": k2, "value": data[k1][k2]["percent"]})

json_out = json.dumps(out_data, ensure_ascii=False, indent=2)
with open('tag_sankey_data.json', 'w') as f:
    f.write(json_out)
