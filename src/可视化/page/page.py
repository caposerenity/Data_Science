from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie, Radar
from pyecharts.commons.utils import JsCode
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts.components import Image
from pyecharts.options import ComponentTitleOpts
import json
import datetime
from pyecharts import options as opts
from pyecharts.charts import Calendar

fp = open('calendar_heat_map.json', encoding='utf-8')
res = fp.read()
data_ = json.loads(res)

fpp = open('user_time_data.json', encoding='utf-8')
res2 = fpp.read()
data_fea = json.loads(res2)

f3 = open('personal_rank.json', encoding='gbk')
res3 = f3.read()
data_rank = json.loads(res3)

f4 = open('programming_style_data.json', encoding='utf-8')
res4 = f4.read()
data_style = json.loads(res4)

f5 = open('capability_list.json', encoding='gbk')
res5 = f5.read()
data_radar = json.loads(res5)


def title(fea_data, style_data) -> Image:
    image = Image()
    sub_data = ""
    for i in range(len(fea_data)):
        if i == 0: sub_data += "关于面向用例：\n"
        if i == 3: sub_data += "\n关于提交次数：\n"
        if i == 4: sub_data += "\n关于时间偏好：\n"
        if i == 9: sub_data += "\n面对难题：\n"
        sub_data = sub_data + fea_data[i] + "\n"

    for i in range(len(style_data)):
        if i == 0: sub_data += "\n\n代码风格评估：\n"

        sub_data = sub_data + style_data[i]
        if i == 2: sub_data += "\n"
        if i == 3: sub_data += "\n"
        if i == 5: sub_data += "\n"

    # img_src = (
    #     "/Users/amanda/Data_Science/src/可视化/title.png"
    # )
    # image.add(
    #     src=img_src,
    #     style_opts={"width": "200px", "height": "200px", "style": "margin-top: 20px"},
    # )

    image.set_global_opts(
        title_opts=ComponentTitleOpts(title="PYTHON 用户数据分析", subtitle=sub_data)
    )

    return image


def calendar_heat_map(data, k) -> Calendar:
    calendar = (
        Calendar()
            .add("", data, calendar_opts=opts.CalendarOpts(range_="2020"))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="user_id:" + k + " Upload numbers Heat Map"),

            visualmap_opts=opts.VisualMapOpts(
                orient="horizontal",
                is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
                pieces=[{"min": 1, "max": 5}, {"min": 6, "max": 10}, {"min": 11, "max": 15}, {"min": 16, "max": 20},
                        {"min": 21, "max": 25}, {"min": 26, "max": 30}, {"min": 31, "max": 40}, {"min": 41, "max": 60},
                        {"min": 61, "max": 80}, {"min": 81}]

            ),
        )
    )
    return calendar


def rank_liquid(data) -> Liquid:
    data1 = float(data["line_rank"][:-1]) / 100
    data2 = float(data["note_rank"][:-1]) / 100
    data3 = float(data["time_rank"][:-1]) / 100
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
            .set_global_opts(title_opts=opts.TitleOpts(title="user_id:" + k + "的代码行数、注释行数、时间复杂度排名显示", pos_top=60))
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
    return grid


def user_ability_radar(v1, v2) -> Radar:
    radar = (
        Radar(init_opts=opts.InitOpts())
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="字符串", max_=100),
                opts.RadarIndicatorItem(name="线性表", max_=100),
                opts.RadarIndicatorItem(name="数组", max_=100),
                opts.RadarIndicatorItem(name="查找算法", max_=100),
                opts.RadarIndicatorItem(name="排序算法", max_=100),
                opts.RadarIndicatorItem(name="数字操作", max_=100),
                opts.RadarIndicatorItem(name="树结构", max_=100),
                opts.RadarIndicatorItem(name="图结构", max_=100),
            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        )
            .add(
            series_name="学生能力评估",
            data=v1,
            linestyle_opts=opts.LineStyleOpts(color="#CD0000", width=3, opacity=0.7),
        )
            .add(
            series_name="学生平均得分",
            data=v2,
            linestyle_opts=opts.LineStyleOpts(color="#5CACEE", width=3, opacity=0.7),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(), legend_opts=opts.LegendOpts()
        )
    )
    return radar


def page_simple_layout(heat_data, user_id, fea_data, rank_data, style_data, v1, v2):
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        calendar_heat_map(heat_data, user_id),
        # bar_datazoom_slider(),
        # line_markpoint(),

        # grid_mutil_yaxis(),
        # liquid_data_precision(),
        # table_base(),
    )
    if rank_data != "no_rank_data":
        page.add(rank_liquid(rank_data))
    page.add(user_ability_radar(v1,v2))
    page.add(title(fea_data, style_data), )

    page.render("user_page" + user_id + ".html")


if __name__ == "__main__":
    begin = datetime.date(2020, 2, 1)
    end = datetime.date(2020, 3, 31)

    # 用于存放所有有水球图的user_id
    user_liquid = []
    for k in data_rank.keys():
        user_liquid.append(k)

    for k in data_.keys():
        times = []
        data = []

        for v in data_[k].values():
            times.append(v)

        for i in range((end - begin).days + 1):
            data.append([str(begin + datetime.timedelta(days=i)), times[i]])

        # 雷达图
        v1 = [data_radar[k]["capability"]]
        v2 = [data_radar[k]["score"]]
        for i in range(8):
            for j in range(8):
                v1[0][j] = round(v1[0][j], 2)
        for i in range(8):
            for j in range(8):
                v2[0][j] = round(v2[0][j], 2)

        if k in user_liquid:
            page_simple_layout(data, k, data_fea[k]["feature_description"], data_rank[k], data_style[k]["styles"], v1,
                               v2)
        else:
            page_simple_layout(data, k, data_fea[k]["feature_description"], "no_rank_data", data_style[k]["styles"], v1,
                               v2)
