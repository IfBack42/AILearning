import re
import csv
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # 跳转到页面
    page.goto("https://store.steampowered.com/app/55100/Homefront/")
    # 滚动到页面底部
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    # 定位到评论区并点击
    page.locator("a[href*='https://steamcommunity.com/app/55100/reviews/?browsefilter=toprated']").first.click()
    page.wait_for_load_state("networkidle")
    # 更改页面语言
    page.locator("span#language_pulldown").click()
    page.get_by_text("简体中文").click()

    # 进行循环滑动
    for _ in range(5):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(200)
        page.wait_for_load_state("load")


    # 定位到评论，获取标签（推荐or不推荐）
    content_page_locator = page.locator("div#AppHubContent.apphub_Content")
    content_locator = content_page_locator.locator("div.apphub_Card.modalContentLink.interactable[role='button']")
    labels = content_locator.locator("div.title").all_inner_texts()
    content = content_locator.locator("div.apphub_CardTextContent").all_inner_texts()
    #
    # # 保存为CSV文件
    # with open('steam_comments_dataset.csv', 'w', newline='', encoding='utf-8-sig') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['x', 'y'])  # 写入表头
    #
    #     for label, text in zip(labels, content):
    #         comment = '\n'.join(text.split('\n')[1:])
    #         writer.writerow([comment, label])
    #
    # print(f"已保存 {len(labels)} 条评论到 steam_comments_dataset.csv")

    for label, text in zip(labels, content):
        comment = '\n'.join(text.split('\n')[1:])
        print(label)
        print(comment,end='\n'*5)


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
