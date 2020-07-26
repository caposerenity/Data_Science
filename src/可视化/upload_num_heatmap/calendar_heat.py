import json
import datetime
from pyecharts import options as opts
from pyecharts.charts import Calendar

#  生成学生提交记录的热点图 user_id.html

fp = open('calendar_heat_map.json', encoding='utf-8')
res = fp.read()
data_ = json.loads(res)

begin = datetime.date(2020, 2, 1)
end = datetime.date(2020, 3, 31)

for k in data_.keys():
    times = []
    data = []
    for v in data_[k].values():
        times.append(v)

    for i in range((end - begin).days + 1):
        data.append([str(begin + datetime.timedelta(days=i)), times[i]])

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
    name = "uploads_"+k + '.html'
    calendar.render(name)
