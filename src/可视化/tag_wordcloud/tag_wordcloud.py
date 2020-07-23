from pyecharts import options as opts
from pyecharts.charts import WordCloud
import json

f = open('tag_wordcloud_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)

words = []
for k in data.keys():
    words.append((k, data[k]))

c = (
    WordCloud()
        .add(
        "",
        words,
        word_size_range=[20, 100],
        textstyle_opts=opts.TextStyleOpts(),
    )
        .set_global_opts(title_opts=opts.TitleOpts(title="tag-WordCloud"))
        .render("tag_wordcloud_diamond.html")
)
