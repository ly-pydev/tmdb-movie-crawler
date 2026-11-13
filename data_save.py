import csv
import os

# 定义csv字段顺序，和打印顺序保持一致
FIELD_NAMES = [
    "标题",
    "海报链接",
    "上映信息",
    "评分",
    "简介",
    "导演",
    "Screenplay",
    "Story_Novel",
    "演员"
]

# 标记表头是否已经写入，防止循环翻页重复写表头
header_written = False
CSV_FILE = "tmdb_top_movie.csv"


def init_csv():
    """初始化csv文件，写入表头，只执行一次"""
    global header_written
    if not header_written:
        # 文件不存在或者需要新建表头
        with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
            writer.writeheader()
        header_written = True
        print(f"\n✅ CSV文件初始化完成：{CSV_FILE}")


def save_movie_data(title, poster_url, detail_info):
    """
    保存单条电影数据到csv
    :param title: 电影标题
    :param poster_url: 海报链接
    :param detail_info: get_movie_detail 返回的字典
    """
    # 先初始化表头
    init_csv()

    row = {
        "标题": title,
        "海报链接": poster_url,
        "上映信息": detail_info["上映信息"],
        "评分": detail_info["评分"],
        "简介": detail_info["简介"],
        "导演": detail_info["导演"],
        "Screenplay": detail_info["Screenplay"],
        "Story_Novel": detail_info["Story_Novel"],
        "演员": detail_info["角色"]
    }

    with open(CSV_FILE, "a", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writerow(row)
    print(f"💾 已保存【{title}】到csv")
