import json
from pyecharts import options as opts
from pyecharts.charts import Grid, Liquid
from pyecharts.commons.utils import JsCode

f = open('personal_rank.json', encoding='gbk')
res = f.read()
data = json.loads(res)

for k in data.keys():
    data1 = float(data[k]["line_rank"][:-1]) / 100
    data2 = float(data[k]["note_rank"][:-1]) / 100
    data3 = float(data[k]["time_rank"][:-1]) / 100

    l1 = (
        Liquid(init_opts=opts.InitOpts(chart_id="代码行数"))
            .add("line_rank",
                 [data1],
                 center=["15%", "50%"],
                 label_opts=opts.LabelOpts(
                     font_size=50,
                     formatter=JsCode(
                         """function (param) {
                                 return (Math.floor(param.value * 10000) / 100) + '%';
                             }"""
                     ),
                     position="inside",
                 ),
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title=k + "的代码行数、注释行数、时间复杂度排名显示",pos_top=60))
    )

    l2 = Liquid().add(
        "note_rank",
        [data2],
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
            ),
            position="inside",
        ),
    )
    l3 = Liquid().add(
        "time_rank",
        [data3],
        center=["85%", "50%"],
        label_opts=opts.LabelOpts(
            font_size=50,
            formatter=JsCode(
                """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
            ),
            position="inside",
        ),

    )

    grid = Grid().add(l1, grid_opts=opts.GridOpts()).add(l2, grid_opts=opts.GridOpts()).add(l3,
                                                                                            grid_opts=opts.GridOpts())
    grid.render("multiple_liquid.html")
    break
