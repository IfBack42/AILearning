import re
import time
import requests
import random
from lxml import etree
from fake_useragent import UserAgent
import traceback


def get_html(url, params=None, max_retries=3):
    ua = UserAgent()
    headers = {
        'Cookie': 'browserid=346322557376458133; timezoneOffset=28800,0; sessionid=513da5cc5e17868745d3e620; birthtime=1149264001; lastagecheckage=3-June-2006; deep_dive_carousel_method=default; steamLoginSecure=76561199751823022%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAxMl8yNkEwN0IxRl9FQkJENyIsICJzdWIiOiAiNzY1NjExOTk3NTE4MjMwMjIiLCAiYXVkIjogWyAid2ViOnN0b3JlIiBdLCAiZXhwIjogMTc1MzgwNDI1NSwgIm5iZiI6IDE3NDUwNzcwNDAsICJpYXQiOiAxNzUzNzE3MDQwLCAianRpIjogIjAwMTRfMjZBOUIzRjhfODAwQjIiLCAib2F0IjogMTc1MzAxMDE3MSwgInJ0X2V4cCI6IDE3NzEwNjQzMjcsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxODUuMjQ0LjIwOC45MCIsICJpcF9jb25maXJtZXIiOiAiMTg1LjI0NC4yMDguOTAiIH0.0bhQMoajzltygM6XhWH4Yx7W6mhoCt4OVeyq5QNuh9DzeTQrZ97QwaRFH5ttHM_Gt3e93YS7a0W7OwU0hZtxCQ; deep_dive_carousel_focused_app=2358720; steamCountry=SG%7C4f1b041640b1a32b00ec6c9b08881df1; recentapps=%7B%22992300%22%3A1753767386%2C%221546570%22%3A1753721529%2C%222277560%22%3A1753721030%2C%222593370%22%3A1753719125%2C%22736190%22%3A1753718574%2C%222358720%22%3A1753717058%2C%22990630%22%3A1753097581%2C%221485690%22%3A1753096276%2C%22667970%22%3A1753085459%2C%221172470%22%3A1753084797%7D; app_impressions=1096030%401_5_9__405%7C1092250%401_5_9__405%7C992300%401_5_9__412%7C3056010%401_5_9__412%7C1155760%401_5_9__412%7C1092250%401_5_9__412%7C2314360%401_5_9__412%7C1329262%401_5_9__412%7C1329261%401_5_9__412%7C1295190%401_5_9__412%7C1329264%401_5_9__412%7C1329263%401_5_9__412%7C2358720%401_5_9__414%7C1111500%401_5_9__405%7C1111360%401_5_9__405%7C1096040%401_5_9__405%7C2622380%401_5_9__300%7C1245620%401_5_9__300%7C3489700%401_5_9__300%7C2384580%401_5_9__300',        "User-Agent": ua.random
    }

    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(1.0, 3.0))
            response = requests.get(
                url=url,
                headers=headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            return response.content.decode('utf-8', errors='replace')

        except (requests.exceptions.RequestException, UnicodeDecodeError) as e:
            print(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(2.0, 5.0))
            else:
                raise Exception(f"无法获取页面: {url}") from e


def extract_app_id(url):
    match = re.search(r'app/(\d+)', url)
    if match:
        return match.group(1)
    raise ValueError(f"无法从URL中提取app ID: {url}")


def extract_game_name(content):
    """
    从 Steam 页面 HTML 中提取游戏名称

    参数:
        content (str): Steam 页面的 HTML 内容

    返回:
        str: 游戏名称（已清理非法字符）
    """
    tree = etree.HTML(content)

    # 方法1：从标题标签提取
    title_elem = tree.xpath('//div[@id="appHubAppName" or @class="apphub_AppName"]/text()')
    if title_elem:
        game_name = title_elem[0].strip()
    else:
        # 方法2：从meta标签提取
        meta_title = tree.xpath('//meta[@property="og:title"]/@content')
        game_name = meta_title[0].strip() if meta_title else "Unknown Game"

    # 清理非法文件名字符
    game_name = re.sub(r'[\\/:*?"<>|]', '_', game_name)
    return game_name


def get_review_stats(content):
    """
    从 Steam 页面 HTML 中提取评价数据

    参数:
        content (str): Steam 页面的 HTML 内容

    返回:
        tuple: (好评数, 差评数, 好评率)
    """
    tree = etree.HTML(content)

    # 方法1：优先从 meta 标签提取总评价数（更可靠）
    review_count_elem = tree.xpath('//meta[@itemprop="reviewCount"]/@content')
    total_reviews = int(review_count_elem[0]) if review_count_elem else 0

    # 方法2：从好评元素提取（兼容旧版页面）
    summary_span = tree.xpath('//span[@class="game_review_summary positive" and @data0-tooltip-html]')
    if summary_span:
        tooltip = summary_span[0].get('data0-tooltip-html', '')
        match = re.search(r'(\d+)%', tooltip.replace('，', ','))
        if match:
            rate = int(match.group(1))
            positive = int(total_reviews * rate / 100) if total_reviews > 0 else 0
            negative = total_reviews - positive
            return positive, negative, rate

    # 方法3：从隐藏输入字段提取（备用方案）
    positive_input = tree.xpath('//input[@id="review_summary_num_positive_reviews"]/@value')
    if positive_input:
        positive = int(positive_input[0])
        negative = total_reviews - positive if total_reviews > 0 else 0
        rate = round((positive / total_reviews) * 100, 2) if total_reviews else 0
        return positive, negative, rate

    # 默认返回
    return 0, 0, 0


def parse_reviews(content):
    tree = etree.HTML(content)
    reviews_list = []
    unique_reviews = set()  # 用于检测重复评论

    # 检查是否有错误消息
    error_msg = tree.xpath('//div[@class="error_ctn"]/text()')
    if error_msg:
        print(f"Steam错误消息: {error_msg[0]}")
        return [], None

    # 提取所有评论卡片
    review_cards = tree.xpath('//div[contains(@class, "apphub_Card")]')
    if not review_cards:
        print("未找到评论卡片，可能是页面结构变化")
        return [], None

    for card in review_cards:
        try:
            # 用户名
            username_elem = card.xpath('.//div[contains(@class, "apphub_CardContentAuthorName")]/a')
            username = username_elem[0].text.strip() if username_elem else ""

            # 发布日期
            date_elem = card.xpath('.//div[contains(@class, "date_posted")]/text()')
            date_posted = date_elem[0].replace("Posted: ", "").strip() if date_elem else ""

            # 评论内容 - 排除日期节点
            content_elem = card.xpath('.//div[contains(@class, "apphub_CardTextContent")]')
            if content_elem:
                # 从内容元素中排除日期节点
                date_nodes = content_elem[0].xpath('.//div[contains(@class, "date_posted")]')
                for node in date_nodes:
                    node.getparent().remove(node)

                content_text = " ".join([
                    text.strip() for text in
                    content_elem[0].xpath('.//text()[not(parent::script)]')  # 排除script标签内容
                    if text.strip()  # 过滤空文本
                ])
            else:
                content_text = ""

            # 检查是否重复
            review_id = f"{username}_{hash(content_text[:50])}"
            if review_id in unique_reviews:
                continue
            unique_reviews.add(review_id)

            # 拥有游戏数
            games_owned = "0"
            games_elem = card.xpath('.//div[contains(@class, "apphub_CardContentMoreLink")]/text()')
            if games_elem and "products" in games_elem[0]:
                games_owned = re.search(r'\d+', games_elem[0]).group(0)

            # 游戏时长
            hours_elem = card.xpath('.//div[contains(@class, "hours")]/text()')
            hours = "0"
            if hours_elem:
                hours_match = re.search(r'(\d+\.?\d*)', hours_elem[0])
                hours = hours_match.group(1) if hours_match else "0"

            # 有用数和有趣数
            helpful_elem = card.xpath('.//div[contains(@class, "found_helpful")]//text()')
            helpful = "0"
            funny = "0"
            if helpful_elem:
                helpful_text = " ".join([text.strip() for text in helpful_elem if text.strip()])
                numbers = re.findall(r'(\d+)', helpful_text)
                if numbers:
                    helpful = numbers[0]
                    funny = numbers[1] if len(numbers) > 1 else "0"

            if username and content_text:
                reviews_list.append({
                    'username': username,
                    'date_posted': date_posted,
                    'content': content_text,
                    'hours_played': hours,
                    'helpful_count': helpful,
                    'funny_count': funny,
                    'games_owned': games_owned
                })
        except Exception as e:
            print(f"解析评论时出错: {str(e)}")
            continue

    # 下一页游标
    cursor = tree.xpath('//input[@name="userreviewscursor"]/@value')
    return reviews_list, cursor[0] if cursor else None


def save_to_file(filename, game_data, reviews_data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=== 游戏评价统计 ===\n")
        f.write(f"游戏名称: {game_data['game_name']}\n")
        f.write(f"App ID: {game_data['app_id']}\n")
        f.write(f"好评数: {game_data['positive_reviews']}\n")
        f.write(f"差评数: {game_data['negative_reviews']}\n")
        f.write(f"好评率: {game_data['review_score']}%\n")
        f.write(f"总评价数: {game_data['total_reviews']}\n")
        f.write(f"数据获取时间: {game_data['timestamp']}\n\n")

        f.write(f"\n=== 用户评论 (共 {len(reviews_data)} 条) ===\n\n")
        for i, review in enumerate(reviews_data, 1):
            f.write(f"评论 #{i}\n")
            f.write(f"用户名: {review['username']}\n")
            f.write(f"拥有游戏数: {review['games_owned']}\n")
            f.write(f"游戏时长: {review['hours_played']} 小时\n")
            f.write(f"发布时间: {review['date_posted']}\n")
            f.write(f"有用数: {review['helpful_count']}\n")
            f.write(f"有趣数: {review['funny_count']}\n")
            f.write(f"评论内容:\n{review['content']}\n\n")
            f.write("-" * 80 + "\n\n")


def run():
    url = input("请输入Steam游戏URL: ").strip()

    try:
        app_id = extract_app_id(url)
        print(f"提取的App ID: {app_id}")

        # 获取游戏页面
        game_page_url = f"https://store.steampowered.com/app/{app_id}"
        game_page_content = get_html(game_page_url)

        # 自动提取游戏名称
        game_name = extract_game_name(game_page_content)
        print(f"提取的游戏名称: {game_name}")

        # 获取评价数据
        positive, negative, score = get_review_stats(game_page_content)
        total = positive + negative

        game_data = {
            'game_name': game_name,
            'app_id': app_id,
            'positive_reviews': positive,
            'negative_reviews': negative,
            'review_score': score,
            'total_reviews': total,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        # 输出结果
        print("\n=== 游戏评价统计 ===")
        for k, v in game_data.items():
            print(f"{k}: {v}")

        # 评论页面URL
        reviews_url = f"https://steamcommunity.com/app/{app_id}/reviews/?browsefilter=toprated&snr=1_5_100010_&l=english"

        # 自动生成文件名（使用游戏名称）
        safe_game_name = re.sub(r'[\\/:*?"<>|]', '_', game_name)
        output_file = f"{safe_game_name}_{app_id}_reviews.txt"

        # 获取评论数据
        content = get_html(reviews_url)
        reviews_data, cursor = parse_reviews(content)

        # 用户选择页数
        try:
            pages = int(input("\n需要爬取多少页评论? (每页约10条): ") or "1")
        except:
            pages = 1

        # 翻页处理
        for page in range(2, pages + 1):
            print(f"正在爬取第 {page} 页")
            content = get_html(reviews_url, {'p': page, 'userreviewscursor': cursor})
            new_reviews, cursor = parse_reviews(content)
            reviews_data.extend(new_reviews)
            if not cursor:
                break

        # 保存结果
        save_to_file(output_file, game_data, reviews_data)
        print(f"\n完成! 已保存到 {output_file}")
        print(f"总评论数: {len(reviews_data)}")

    except Exception as e:
        print(f"错误: {str(e)}")
        traceback.print_exc()


if __name__ == '__main__':
    run()