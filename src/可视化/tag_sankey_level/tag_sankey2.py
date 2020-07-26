import json
import pyecharts.options as opts
from pyecharts.charts import Sankey

# 生成tag分类的桑葚图（第二种

with open("tag_sankey_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
(
    Sankey(init_opts=opts.InitOpts(width="1000px",height="1200px"))
    .add(
        series_name="",
        nodes=data["nodes"],
        links=data["links"],
        itemstyle_opts=opts.ItemStyleOpts(border_width=1, border_color="#aaa"),
        linestyle_opt=opts.LineStyleOpts(color="source", curve=0.5, opacity=0.5),
        tooltip_opts=opts.TooltipOpts(trigger_on="mousemove"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Sankey Diagram"))
    .render("sankey_diagram2.html")
)
