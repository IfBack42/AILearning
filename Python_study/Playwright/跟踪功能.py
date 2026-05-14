# 使用跟踪功能记录代码运行结果
# 运行 playwright show-trace trace.zip 查看跟踪记录

import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()

    # 详细跟踪配置
    context.tracing.start(
        name="my-trace",  # 跟踪名称
        screenshots=True,  # 包含截图
        snapshots=True,  # 包含 DOM 快照
        sources=True,  # 包含源代码
    )

    page = context.new_page()
    page.goto("https://www.bilibili.com/")
    page.locator(".nav-search-content").click()
    page.get_by_role("textbox").fill("明日方舟")
    with page.expect_popup() as page1_info:
        page.get_by_role("textbox").press("Enter")
    page1 = page1_info.value
    page1.goto("https://search.bilibili.com/all?keyword=%E6%98%8E%E6%97%A5%E6%96%B9%E8%88%9F&from_source=webtop_search&spm_id_from=333.1007&search_source=5")
    page1.get_by_role("link", name="《明日方舟》EP - Oath 104.7万 03:").click()

    input('='*50)

    # ---------------------
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
