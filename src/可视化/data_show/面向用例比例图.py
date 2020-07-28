from pyecharts import options as opts
from pyecharts.charts import Bar
import json

# 生成面向用例比例图

f = open('handled_data.json', encoding='gbk')
res = f.read()
data = json.loads(res)

xaxis = []
case_oriented = []
no_case_oriented = []
for k in data.keys():
    xaxis.append(k)
    yes = 0
    no = 0
    for case in data[k]["cases"]:
        if case["final_cheat"]:
            yes += 1
        else:
            no += 1
    case_oriented.append(yes)
    no_case_oriented.append(no)

c = (
    Bar()
        .add_xaxis(xaxis)
        .add_yaxis("面向用例题数", case_oriented, stack="stack1")
        .add_yaxis("正常完成题数", no_case_oriented, stack="stack1")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        title_opts=opts.TitleOpts(title="面向用例比例图"),
        yaxis_opts=opts.AxisOpts(name="题目数量"),
        xaxis_opts=opts.AxisOpts(name="用户ID"),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],

    )
        .render("面向用例比例图.html")
)
