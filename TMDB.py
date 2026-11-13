from playwright.sync_api import sync_playwright
from lxml import html
from TMDB_detail import get_movie_detail
from data_save import save_movie_data  # 新增导入


def main():
    # ========== 在这里指定你要抓取多少页 ==========
    page_total = 5   # 改成5就是抓前5页
    # ===========================================

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for current_page in range(1, page_total + 1):
            print(f"\n========== 正在抓取第 {current_page} 页 / 共 {page_total} 页 ==========")
            url = f"https://www.themoviedb.org/movie/top-rated?page={current_page}"
            page.goto(url)

            # 处理Cookie弹窗（只在第一页大概率出现，多页加容错）
            if current_page == 1:
                try:
                    page.get_by_role("button", name="接受所有 Cookie").click(timeout=6000)
                except:
                    try:
                        page.get_by_role("button", name="Accept All Cookies").click(timeout=6000)
                    except:
                        print("Cookie弹窗未出现，跳过")

            page.wait_for_selector('div[class*="card"]', timeout=20000)
            html_content = page.content()
            doc = html.fromstring(html_content)

            items = doc.xpath('//div[@class="media-list-results contents"]/div[contains(@class,"bg-surface-card")]')
            print(f"本页抓到电影数量：{len(items)}")

            for item in items:
                title = item.xpath('.//div[@class="options w-[26px] h-[26px] absolute top-2 right-2"]/@data-name')
                title = title[0].strip() if title else "无标题"

                href_res = item.xpath('.//a[@class="flex w-full"]/@href')
                if href_res:
                    detail_url = "https://www.themoviedb.org" + href_res[0].strip()
                else:
                    detail_url = ""

                poster_url = item.xpath('.//img/@src')
                poster_url = poster_url[0].strip() if poster_url else ""

                if detail_url:
                    print(f"\n正在访问详情页：{title} → {detail_url}")
                    detail_info = get_movie_detail(page, detail_url)
                    # ========== 新增：调用保存函数 ==========
                    save_movie_data(title, poster_url, detail_info)
                    # ======================================
                    print(f"  海报链接：{poster_url}")
                    print(f"  上映信息：{detail_info['上映信息']}")
                    print(f"  评分：{detail_info['评分']}")
                    print(f"  简介：{detail_info['简介']}")
                    print(f"  导演：{detail_info['导演']}")
                    print(f"  剧本编剧(Screenplay)：{detail_info['Screenplay']}")
                    print(f"  故事/原著(Story/Novel)：{detail_info['Story_Novel']}")
                    print(f"  演员：{detail_info['角色']}")
                else:
                    print(f"\n⚠️ {title} 没有详情链接")
                print("-" * 60)

        browser.close()
        print("\n✅ 全部页面抓取完成！csv已生成 tmdb_top_movie.csv")


if __name__ == '__main__':
    main()
