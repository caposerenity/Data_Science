from pyecharts import options as opts
from pyecharts.charts import Scatter  # 导入散点图绘制模块
import json

# 生成debug时间和题目难度的点图, 通过点图能看出debug时间得进行修正，修正后才能进行拟合

f = open('case_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

xy_data = []
tmp = []
x_data = []
y_data = []
# x轴为难度，y轴为debug时间
for k in data.keys():
    if data[k]["case_type"] == "字符串":
        tmp = [data[k]["final_score"],data[k]["average_interval(min)"]]
        xy_data.append(tmp)
xy_data = sorted(xy_data)
for tmp in xy_data:
    x_data.append(tmp[0])
    y_data.append(tmp[1])
    # y_data.append(round(tmp[1]/10,2))
scatter3 = (
    Scatter()
        .add_xaxis(x_data)
        .add_yaxis("debug-time(min)", y_data)
        .set_global_opts(
        title_opts=opts.TitleOpts(title='scatter debug-diff'),
        visualmap_opts=opts.VisualMapOpts(max_=600)
    )
)
scatter3.render('liner-debug-scatter.html')



