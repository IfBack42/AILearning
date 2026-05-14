from playwright.sync_api import sync_playwright

with sync_playwright() as p: # 启动playwright进程
    # 启动浏览器，返回browser对象      👇是否显示操作浏览器
    browser = p.firefox.launch(headless=False)
    # 创建新页面，返回page对象，后续主要操作通过page对象进行
    context = browser.new_context() # 先创建context对象独立上下文，不需要重复创建浏览器
    page = context.new_page()
    # page = browser.new_page()

    page.goto("https://www.baidu.com")
    print(page.title())
    input('='*50)


    # 打开浏览器页面后后续内容进行其他操作


    # 关闭浏览器
    browser.close()
