import json
from pyecharts import options as opts
from pyecharts.charts import Sankey

# 生成tag分类的桑葚图（第一种

with open("tag_sankey_data.json", "r", encoding="utf-8") as f:
    j = json.load(f)
sankey = (
    Sankey(init_opts=opts.InitOpts(width="1000px",height="1200px"))
        .add(
        "sankey",
        nodes=j["nodes"],
        links=j["links"],
        pos_top="10%",
        focus_node_adjacency=True,
        levels=[
            opts.SankeyLevelsOpts(
                depth=0,
                itemstyle_opts=opts.ItemStyleOpts(color="#fbb4ae"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=1,
                itemstyle_opts=opts.ItemStyleOpts(color="#b3cde3"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            ),
            opts.SankeyLevelsOpts(
                depth=2,
                itemstyle_opts=opts.ItemStyleOpts(color="#ccebc5"),
                linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
            )

        ],
        linestyle_opt=opts.LineStyleOpts(curve=0.5),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="Tag Sankey-Level"),
        tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),
    )
    # .render("./tag_sankey_with_level.html")
)
sankey.render("tag_sankey_with_level.html")
