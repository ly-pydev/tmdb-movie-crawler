# from playwright.sync_api import sync_playwright
# from lxml import html
#
#
# def get_movie_detail(page, url):
#     try:
#         page.goto(url, timeout=60000)
#         page.wait_for_selector('h3:has-text("简介")', timeout=20000)
#         detail_html = page.content()
#         d_doc = html.fromstring(detail_html)
#
#         # 评分（不带百分号）
#         score = d_doc.xpath('//div[@class="user_score_chart"]/@data-percent')
#         score = score[0].strip() if score else "无"
#
#         # 简介
#         overview = d_doc.xpath('//h3[text()="简介"]/following-sibling::div[@class="overview"]/p/text()')
#         overview = overview[0].strip() if overview else "无简介"
#
#         # 上映信息
#         release_date = d_doc.xpath('//span[@class="release"]/text()')
#         release_date = release_date[0].strip() if release_date else "无"
#
#         # 导演
#         director = d_doc.xpath('//p[text()="Director"]/preceding-sibling::p/a/text()')
#         director = director[0].strip() if director else "无导演"
#
#         # 编剧
#         writer_name = d_doc.xpath('//p[text()="Writer"]/preceding-sibling::p/a/text()')
#         writer_name = writer_name[0].strip() if writer_name else "无编剧"
#
#         # 演员
#         actors = []
#         profile_list = d_doc.xpath('//li[@class="profile"]')
#         for li in profile_list:
#             name = li.xpath('.//a/text()')
#             role = li.xpath('.//p[@class="character"]/text()')
#             name = name[0].strip() if name else ""
#             role = role[0].strip() if role else ""
#             if name and role not in ("Director", "Writer"):
#                 actors.append(name)
#         actors = "、".join(actors) if actors else "无演员"
#
#         res = {
#             "上映信息": release_date,
#             "评分": score,
#             "简介": overview,
#             "导演": director,
#             "编剧": writer_name,
#             "角色": actors
#         }
#     except Exception as e:
#         res = {
#             "上映信息": "无",
#             "评分": "无",
#             "简介": "无简介",
#             "导演": "无导演",
#             "编剧": "无编剧",
#             "角色": "无角色"
#         }
#     return res
#
#
#
# # 单独调试入口
# # if __name__ == '__main__':
# #     with sync_playwright() as p:
# #         browser = p.chromium.launch(headless=False, slow_mo=300)
# #         page = browser.new_page()
# #         test_url = "https://www.themoviedb.org/movie/1560520-batman-knightfall-part-1-knightfall"
# #         info = get_movie_detail(page, test_url)
# #         print("===== 拿到的数据 =====")
# #         print(info)
# #         page.pause()
# #         browser.close()
#
#
# TMDB_detail.py
from lxml import html

def get_movie_detail(page, url):
    try:
        page.goto(url, timeout=60000)
        page.wait_for_selector('h3:has-text("简介")', timeout=20000)
        detail_html = page.content()
        d_doc = html.fromstring(detail_html)

        # 评分
        score = d_doc.xpath('//div[@class="user_score_chart"]/@data-percent')
        score = score[0].strip() if score else "无"

        # 简介
        overview = d_doc.xpath('//h3[text()="简介"]/following-sibling::div[@class="overview"]/p/text()')
        overview = overview[0].strip() if overview else "无简介"

        # 上映信息
        release_date = d_doc.xpath('//span[@class="release"]/text()')
        release_date = release_date[0].strip() if release_date else "无"

        profile_list = d_doc.xpath('//li[@class="profile"]')
        seen_name = set()
        director_list = []
        screenplay_list = []
        story_novel_list = []
        actor_list = []

        for li in profile_list:
            name_res = li.xpath('./p[1]/a/text()')
            job_res = li.xpath('./p[@class="character"]/text()')
            if not name_res or not job_res:
                continue
            name = name_res[0].strip()
            job = job_res[0].strip()

            # 同一个人只保留第一次出现
            if name in seen_name:
                continue
            seen_name.add(name)

            job_lower = job.lower()
            if "director" in job_lower:
                director_list.append(name)
            elif "screenplay" in job_lower:
                screenplay_list.append(name)
            elif any(k in job_lower for k in ["story", "novel"]):
                story_novel_list.append(name)
            else:
                actor_list.append(name)

        director = "、".join(director_list) if director_list else "无"
        screenplay = "、".join(screenplay_list) if screenplay_list else "无"
        story_novel = "、".join(story_novel_list) if story_novel_list else "无"
        actors = "、".join(actor_list) if actor_list else "无"

        res = {
            "上映信息": release_date,
            "评分": score,
            "简介": overview,
            "导演": director,
            "Screenplay": screenplay,
            "Story_Novel": story_novel,
            "角色": actors
        }
    except Exception as e:
        print(f"详情页捕获异常：{e}")
        res = {
            "上映信息": "无",
            "评分": "无",
            "简介": "无简介",
            "导演": "无",
            "Screenplay": "无",
            "Story_Novel": "无",
            "角色": "无"
        }
    return res
