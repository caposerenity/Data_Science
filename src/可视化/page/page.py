from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie
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

# def title()->Image:
#     image = Image()
#
#     # img_src = (
#     #     "/Users/amanda/Data_Science/src/可视化/title.png"
#     # )
#     # image.add(
#     #     src=img_src,
#     #     style_opts={"width": "200px", "height": "200px", "style": "margin-top: 20px"},
#     # )
#     image.set_global_opts(
#         title_opts=ComponentTitleOpts(title="PYTHON 用户数据分析")
#     )
#     return image

def calendar_heat_map(data,k)->Calendar:
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




def page_simple_layout(heat_data,user_id):
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        #title(),
        calendar_heat_map(heat_data,user_id),
        # bar_datazoom_slider(),
        # line_markpoint(),

        # grid_mutil_yaxis(),
        # liquid_data_precision(),
        # table_base(),
    )
    page.render("user_page"+user_id+".html")


if __name__ == "__main__":
    begin = datetime.date(2020, 2, 1)
    end = datetime.date(2020, 3, 31)

    for k in data_.keys():
        times = []
        data = []
        for v in data_[k].values():
            times.append(v)

        for i in range((end - begin).days + 1):
            data.append([str(begin + datetime.timedelta(days=i)), times[i]])

        page_simple_layout(data, k)

