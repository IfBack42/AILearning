"""
1. 基本常用操作
    - 点击元素：click()
    - 输入文本：fill()
    - 获取元素文本：inner_text()

2. CSS 选择器定位
    2.1 基础选择器
        - tag 选择器：直接写标签名
            page.locator('div').all()
            page.locator('span').all()

        - id 选择器：#xxx
            page.locator('#username').all()

        - class 选择器：.xxx
            page.locator('.btn-primary').all()

    2.2 层级选择器
        - 后代选择器（空格）：匹配所有子孙元素
            page.locator('#wrapper .item')

        - 子选择器（>）：仅匹配直接子元素           区别：>只匹配下一级; 匹配所有子代
            page.locator('div > p')

        - 链式 locator：逐步缩小范围
            page.locator('#wrapper').locator('.item')

    2.3 复合选择器
        - 组合 tag + class：标签名紧跟 class
            page.locator('div.item')  # div 且 class 包含 item

        - 属性选择器：[属性=值]
            page.locator('input[type="text"]')
            page.locator('[data-index="0"]')

    2.4 组选择器（并集）
        - 语法：用逗号分隔多个选择器，匹配任一条件
            page.locator('h1, h2, h3')  # 匹配 h1 或 h2 或 h3
            page.locator('.btn, .link')  # 匹配 class 为 btn 或 link
            page.locator('#header, #footer')  # 匹配 id 为 header 或 footer
            page.locator('#t1 > span , #t1 > p')  # 包含子集需要写全

        - 应用场景：批量操作同类型元素
            buttons = page.locator('button, input[type="button"]').all()


3. 多元素匹配
    3.1 获取所有元素
        - all()：返回 Locator 列表
        - all_inner_texts()：直接获取所有元素的文本列表

    3.2 元素计数
        - count()：返回匹配元素的数量

    3.3 定位特定元素
        - .first：第一个元素
        - .last：最后一个元素
        - .nth(n)：第 n 个元素（从 0 开始计数）
"""


from playwright.sync_api import sync_playwright

with sync_playwright() as p: # 启动playwright进程
    # 启动浏览器，返回browser对象      👇是否显示操作浏览器
    browser = p.firefox.launch(headless=False)
    # 创建新页面，返回page对象，后续主要操作通过page对象进行
    context = browser.new_context() # 先创建context会话对象独立上下文，不需要重复创建浏览器
    page = context.new_page()
    # page = browser.new_page()

    context.tracing.start(
        name="my-trace",  # 跟踪名称
        screenshots=True,  # 包含截图
        snapshots=True,  # 包含 DOM 快照
        sources=True,  # 包含源代码
    )

    page.goto("https://www.baidu.com")

    input('')


    # ========== 方式 1: 链式调用 locator (推荐) ==========

    # 先定位到父容器，再在内部查找子元素
    hot_search = page.locator('#s-hotsearch-wrapper')
    content1 = hot_search.locator('.title-content-title').all()
    for single_content in content1:
        print(single_content.inner_text())
    print('=' * 50)

    # ========== 方式 2: CSS 后代选择器 (空格) ==========
    # 语法：'父标签 子标签' 或 '.父 class .子 class'
    content_descendant = page.locator('#s-hotsearch-wrapper .title-content-title').all()
    print(f"后代选择器找到 {len(content_descendant)} 个元素")
    for item in content_descendant:
        print(item.inner_text())
    print('=' * 50)

    # ========== 方式 3: CSS 子选择器 (>) ==========
    # 只匹配直接子元素，不包括孙子元素
    # 语法：'父标签 > 子标签'
    content_child = page.locator('div > .title-content-title').all()
    print(f"子选择器找到 {len(content_child)} 个元素")
    print('=' * 50)

    # ========== 方式 4: 多层嵌套查找 ==========
    # 可以连续嵌套多层
    wrapper = page.locator('#s-hotsearch-wrapper')
    items = wrapper.locator('div').locator('.title-content-title').all()
    print(f"嵌套查找找到 {len(items)} 个元素")
    print('=' * 50)

    # ========== 方式 5: 使用 nth() 定位特定次序的元素 ==========
    content3 = hot_search.locator('.title-content-title').nth(0).inner_text()
    print(f"第 1 个热搜：{content3}")

    # 获取第一个和最后一个
    first_item = hot_search.locator('.title-content-title').first.inner_text()
    last_item = hot_search.locator('.title-content-title').last.inner_text()
    print(f"第一个热搜：{first_item}")
    print(f"最后一个热搜：{last_item}")
    print('=' * 50)

    # ========== 方式 6: 复杂 CSS 选择器组合 ==========
    # 组合使用 tag、class、属性等
    # 例如：查找 div 标签且 class 包含 'title-content-title' 的元素
    complex_locator = page.locator('div.title-content-title').all()
    print(f"复合选择器找到 {len(complex_locator)} 个元素")

    # 或者根据属性匹配
    attr_locator = page.locator('[data-index="0"]').all()  # 假设有 data-index 属性
    print(f"属性选择器找到 {len(attr_locator)} 个元素")


# 关闭浏览器
    context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()
