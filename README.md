# TMDB Movie Spider
> 基于 Playwright 实现的 TMDB 高分电影榜单爬虫，适合 Python 爬虫学习练习

## 📖 项目介绍
本项目使用 Playwright 模拟浏览器访问 TMDB 高分电影页面，自动翻页抓取电影信息，解析电影详情页的海报、评分、简介、主创人员等数据，并导出为 CSV 文件，方便后续用 Excel 查看、数据分析。
爬虫对主创人员做了简单去重：同一个人在同一部电影里只保留一次，同时区分导演、剧本编剧（Screenplay）、故事/原著（Story/Novel）、演员四类角色。

## ✨ 功能清单
1. 自定义抓取页数，自动翻页
2. 抓取字段：海报链接、上映信息、评分、简介、导演、Screenplay、Story/Novel、演员
3. 单部电影内主创自动去重
4. 导出 CSV 文件，**每次运行会覆盖旧的 tmdb_top_movie.csv**

## 📦 环境依赖
Python 3.8+
```bash
pip install -r requirements.txt
playwright install chromium

## 🚀 使用方法

1. 打开 `main.py`，修改 `page_total` 的数值，设置想要抓取多少页

```
page_total = 2
```

2. 运行主程序

```
python main.py
```

3. 抓取完成后，在项目根目录生成 `tmdb_top_movie.csv`

## 📁 文件说明

- `main.py`：程序入口，翻页调度、列表页抓取
- `TMDB_detail.py`：详情页解析模块，提取电影各项信息
- `data_save.py`：CSV 存储模块，负责写入数据
- `requirements.txt`：依赖清单
- `.gitignore`：忽略缓存、csv、系统文件

## ⚠️ 注意事项

1. 本项目仅用于学习爬虫技术，请勿高频大量请求，遵守 TMDB 网站规则
2. 网站前端页面结构改版后，XPath 会失效，需要重新调整解析表达式
3. CSV 文件每次运行会直接覆盖，重要数据请提前备份