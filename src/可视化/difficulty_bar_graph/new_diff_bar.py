import json
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts.commons.utils import JsCode

f = open('difficulty_test3.json', encoding='gbk')
res = f.read()
data = json.loads(res)

simple = [0 for i in range(8)]
medium = [0 for i in range(8)]
hard = [0 for i in range(8)]
total = [0 for i in range(8)]
nums = [0 for i in range(8)]

level_distributed = {"0-10": 0, "11-20": 0, "21-30": 0, "31-40": 0, "41-50": 0, "51-60": 0, "61-70": 0, "71-80": 0,
                     "81-90": 0, "91-100": 0}
# 观察难度情况
for val in data.values():
    if val["final_level"] <= 10:
        level_distributed["0-10"] += 1
    elif 10 < val["final_level"] <= 20:
        level_distributed["11-20"] += 1
    elif 20 < val["final_level"] <= 30:
        level_distributed["21-30"] += 1
    elif 30 < val["final_level"] <= 40:
        level_distributed["31-40"] += 1
    elif 40 < val["final_level"] <= 50:
        level_distributed["41-50"] += 1
    elif 50 < val["final_level"] <= 60:
        level_distributed["51-60"] += 1
    elif 60 < val["final_level"] <= 70:
        level_distributed["61-70"] += 1
    elif 70 < val["final_level"] <= 80:
        level_distributed["71-80"] += 1
    elif 80 < val["final_level"] <= 90:
        level_distributed["81-90"] += 1
    else:
        level_distributed["91-100"] += 1
print(level_distributed)

# 对数据进行分类
for val in data.values():
    if val["case_type"] == "字符串":
        nums[0] += 1
        total[0] += val["final_level"]
        if val["final_level"] <= 30:
            simple[0] += 1
        elif val["final_level"] > 60:
            hard[0] += 1
        else:
            medium[0] += 1
    elif val["case_type"] == "线性表":
        nums[1] += 1
        total[1] += val["final_level"]
        if val["final_level"] <= 30:
            simple[1] += 1
        elif val["final_level"] > 60:
            hard[1] += 1
        else:
            medium[1] += 1
    elif val["case_type"] == "数组":
        nums[2] += 1
        total[2] += val["final_level"]
        if val["final_level"] <= 30:
            simple[2] += 1
        elif val["final_level"] > 60:
            hard[2] += 1
        else:
            medium[2] += 1
    elif val["case_type"] == "查找算法":
        nums[3] += 1
        total[3] += val["final_level"]
        if val["final_level"] <= 30:
            simple[3] += 1
        elif val["final_level"] > 60:
            hard[3] += 1
        else:
            medium[3] += 1
    elif val["case_type"] == "排序算法":
        nums[4] += 1
        total[4] += val["final_level"]
        if val["final_level"] <= 30:
            simple[4] += 1
        elif val["final_level"] > 60:
            hard[4] += 1
        else:
            medium[4] += 1
    elif val["case_type"] == "数字操作":
        nums[5] += 1
        total[5] += val["final_level"]
        if val["final_level"] <= 30:
            simple[5] += 1
        elif val["final_level"] > 60:
            hard[5] += 1
        else:
            medium[5] += 1
    elif val["case_type"] == "图结构":
        nums[6] += 1
        total[6] += val["final_level"]
        if val["final_level"] <= 30:
            simple[6] += 1
        elif val["final_level"] > 60:
            hard[6] += 1
        else:
            medium[6] += 1
    else:
        nums[7] += 1
        total[7] += val["final_level"]
        if val["final_level"] <= 30:
            simple[7] += 1
        elif val["final_level"] > 60:
            hard[7] += 1
        else:
            medium[7] += 1

list1 = [{"value": hard[i], "percent": hard[i] / nums[i]} for i in range(8)]
list2 = [{"value": medium[i], "percent": medium[i] / nums[i]} for i in range(8)]
list3 = [{"value": simple[i], "percent": simple[i] / nums[i]} for i in range(8)]
average = [round(total[i] / nums[i], 2) for i in range(8)]

xaxis = ["字符串", "线性表", "数组", "查找算法", "排序算法", "数字操作", "图结构", "树结构"]
bar = (
    Bar()
        .add_xaxis(xaxis)
        .add_yaxis("困难", list1, stack="stack1", category_gap="50%")
        .add_yaxis("中等", list2, stack="stack1", category_gap="50%")
        .add_yaxis("简单", list3, stack="stack1", category_gap="50%")
        .extend_axis(
        yaxis=opts.AxisOpts(
            name="难度评分",
            type_="value",
            min_=0,
            max_=100,
            interval=10,
            axislabel_opts=opts.LabelOpts(formatter="{value} 分"),
        )
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="不同类别题目难度展示图"),
        toolbox_opts=opts.ToolboxOpts(),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        legend_opts=opts.LegendOpts(is_show=True),

        # xaxis_opts=opts.AxisOpts(
        #     type_="category",
        #     axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        # ),
        yaxis_opts=opts.AxisOpts(
            name="题目个数",
            type_="value",
            min_=0,
            max_=250,
            interval=50,
            axislabel_opts=opts.LabelOpts(formatter="{value} 个"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
        .set_series_opts(
        label_opts=opts.LabelOpts(
            position="right",
            formatter=JsCode(
                "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
            ),
        )
    )
    # .render("diff_type_diff_bar.html")
)
line = (
    Line()
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(
        series_name="平均难度分",
        yaxis_index=1,
        y_axis=average,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts=opts.LineStyleOpts(color="#f05b72", width=2, opacity=0.8)
    )
)
bar.overlap(line).render("diff_type_diff_bar.html")
