import time
import requests
from lxml import etree
from datetime import datetime


class RedditScraper:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 QuarkPC/4.2.7.457',
            'cookie': 'edgebucket=MorlFjv30aicmZiUSC; loid=000000001n02kcp3br.2.1744262261004.Z0FBQUFBQm45MVIxTWp4T2FLaWxCMDJBeThBUEhSYVBDd2JuV2ZVVzJ0UWpfX181M05scFVxNENjUDFuOWRFYkZZUzI3ZDNBaWQ0eVhEOW56bmZxOXM5blRiZkxYX2xkN0hTZmpCR2NNS1NtR2pSelc1WF9fbWtHc0pJN1o1cEpwdGlLSk11X2Z1eEY; csv=2; eu_cookie={%22opted%22:true%2C%22nonessential%22:true}; _ga=GA1.1.2110104356.1744991689; mutiny.user.token=4d135a68-2e78-4c07-b979-ac3c61ad2a94; _uetvid=76c54a601c6d11f08234dbb2a2796533; __hstc=72739340.6c83f05ad7df958fd71f103f067793d3.1744991691831.1744991691831.1744991691831.1; hubspotutk=6c83f05ad7df958fd71f103f067793d3; _ga_5TD64ET6CX=GS1.1.1744991689.1.0.1744991692.57.0.0; _ga_G5L4KNC814=GS1.1.1744991689.1.0.1744991692.0.0.0; subreddit_sort=ARSf6gK+ALcT; __stripe_mid=738b6155-d68d-43f7-9002-f7b0afa889ad167b86; theme=1; reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml8xbjAya2NwM2JyIiwiZXhwIjoxNzY4NDkwMjY1LjE1NjcxNSwiaWF0IjoxNzUyODUxODY1LjE1NjcxNSwianRpIjoiU1VZYm44X1VuN1Bnc3dQUkpsamp4dTVmZE1NQTh3IiwiY2lkIjoiY29va2llIiwibGNhIjoxNzQ0MjYyMzY1NTM4LCJzY3AiOiJlSnlLamdVRUFBRF9fd0VWQUxrIiwidjEiOiIxNjY0NTEwNjg3NTQxOTksMjAyNS0wNC0xMFQwNToxOToyNSxlMDgxZDYyZGRkYWQ5OWQ1MTBhNjdkMTdmMjUzZjVlY2Y0NTJjZjI3IiwiZmxvIjoxMX0.abVh_3AZQIEpXUrG0BwGmmevM326HoeY5lspgiJPyjIK4c3fRFAtOnxc3ZdX1Kv6ahlKHt2xgLKzgRCDQu2OeVrXfSwYaYpCKNAcZY9AA5qfT3jYs4nOgd65uzNi28wTuA_pAvKrGWTBUbDBLSGHHS8wWcu0I1DluhO3qvs6Ws-8kybT1-d7Jwq9dNbNZhYYgC3ZwlfgY3YIuzjQ4GvZRT7OYHFJkJIUV3qXhAjK2hNd33ctc0h4WdNEsXC1tzN-ECD_A8UmoOCSUi03XJr85-VajxLvjftd3MIdpKPEB1hw7CO52XI25QZIT5S2_yNZLet0PkvNv5eAw3IAH6pNqg; csrf_token=72d6647b784c5755894c541eb2613682; reddit_chat_view=closed; __itrace_wid=84fe1790-1a93-4c75-8ebb-423c012fa36c; t2_1n02kcp3br_recentclicks3=t3_1hdmxnk%2Ct3_18dit78%2Ct3_1m4q9gq%2Ct3_1m2ltae%2Ct3_1k8yhlo%2Ct3_1k8rqdu%2Ct3_1bqh5l2%2Ct3_1fhcmol%2Ct3_163ssmk%2Ct3_1f2gut5; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzUzNzkxNDk5LjQwNDIxMywiaWF0IjoxNzUzNzA1MDk5LjQwNDIxMywianRpIjoiQXZwQm9ER0pCenJZWDhaaE1YZUVQVmRwa0tQcFdRIiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml8xbjAya2NwM2JyIiwiYWlkIjoidDJfMW4wMmtjcDNiciIsImxjYSI6MTc0NDI2MjM2NTUzOCwic2NwIjoiZUp4a2tkR090REFJaGQtRmE1X2dmNVVfbTAxdGNZYXNMUWFvazNuN0RWb2NrNzA3Y0Q0cEhQOURLb3FGRENaWGdxbkFCRmdUclREQlJ1VDluTG0zZzJpTmU4dFlzWm5DQkZtd0ZEcmttTEdzaVFRbWVKSWF5eHNtb0lMTnlGeXV0R05OTFQwUUpxaGNNcmVGSHBjMm9ia2JpNTZkR0ZXNXJEeW9zVmZsMHRqR0ZMWW54amNicXcycHVDNm5Na25MUXZrc1h2VGpOOVczOXZtel9TYTBKOE9LcXVtQjNobEpDRzRzZnBpbTNkOVRrNTZ0Q3hhMTkzcVEydWQ2M0s1OTFpdzBPN2VmNl9sckl4bVhZMmgtSnZ0MzF5LWhBNDg4THpQcUFFYXM0VWNaZG1RZF9sVUhVTG1nSkdNSjR0TUk1TXJsMjM4SnRtdlR2OGJ0RXo5OE0tS21OX3pXRE5SekNlTFFwX0gxR3dBQV9fOFExZVRSIiwicmNpZCI6IlU3T25LeWJkRjZubUpQUHFhY0haRDRuSmVTMTd0QVhJNUFQTE1vZ05GajQiLCJmbG8iOjJ9.CrJ-h6G1WOAfJJgVfJvWubVo3diPn54xdTh8A0LefOAhYoJF1JO1XsNwjepBZELD0hFVKN-b5hoj6Y8-rta-LSPETIG44h-kVH2SV_25pe5Z97k3UpKvX6BQ1sG3LgqCC-Ng9klEkYetIY4Cbc8_SU8tGSZBznmfBFUjJsC6a4PS7lzK4DVZ3NR3Odxs6bEP_MxWxK_nqXTPkKLDmQUr1nAa6jzl1fo1lO_YySVdpxBD3HqvFRvjzT4GXgHAu_5PijcsY1TEfrNuPCjYUB8PHACtvAaEElVsgLfnfHh2LA6TIVuD--jZVdM9wgCqlFXe8FWmMst_9DhLKHbH8WhudA; session_tracker=ciajoebhkpfobkopqa.0.1753708504889.Z0FBQUFBQm9oM2ZZVUx4UjBGY05oN1VBdURkN1Z5NHhOTURJY21OSlZUM25Eei1EV3pfVFpCa3JWQk0xeFBiS3J6NXdrbTRCYWEtXzUwZlpKMUdIemNwRXdhQnBua3AyMVhWTElmSHh5bFJMQ25YT3gwb3BIbU9nNWQyZHI1YU1Nc1RNREZzNjJVU1U'  # 替换为你的实际cookie
        }
        self.base_url = "https://www.reddit.com"

        # 确保所有头部值都是ASCII字符
        self._sanitize_headers()

    def _sanitize_headers(self):
        """确保所有头部值都是ASCII字符"""
        for key, value in self.headers.items():
            if isinstance(value, str):
                # 移除非ASCII字符
                self.headers[key] = value.encode('ascii', 'ignore').decode('ascii')

    def html_get(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            response.raise_for_status()
            return response.content.decode('utf-8')
        except Exception as e:
            print(f"获取页面失败: {e}")
            return None

    def parse_post(self, html):
        tree = etree.HTML(html)
        post_data = {
            'title': self._get_text(tree, '//h1[contains(@aria-label, "Post Title: ")]/text()'),
            'score': self._get_text(tree, '//shreddit-post/@score'),
            'comment_count': self._get_text(tree, '//shreddit-post/@comment-count'),
            'subscribers': self._get_text(tree, '//shreddit-subreddit-header/@subscribers'),
            'content': self._get_text(tree, '//div[@data0-post-click-location="text-body"]//p/text()'),
            'post_time': self._get_text(tree, '//faceplate-timeago/@ts'),
            'author': self._get_text(tree, '//shreddit-post/@author')
        }
        return tree, post_data

    def _get_text(self, tree, xpath):
        try:
            result = tree.xpath(xpath)
            if result:
                if isinstance(result, list):
                    return result[0].strip()
                return result.strip()
            return ""
        except:
            return ""

    def get_first_url(self, et):
        try:
            result = et.xpath('//link[@rel="preload"]/@href')[0]
            return self.base_url + result
        except:
            return None

    def first_page_comment_get(self, url, headers, et):
        result = requests.get(url=url, headers=headers).content.decode('utf-8')
        et2 = etree.HTML(result)
        try:
            cursor = et2.xpath('//input[@name="cursor"]/@value')[-1]
        except:
            cursor = None

        comments = []
        comment_elements = et2.xpath('//shreddit-comment')

        for element in comment_elements:
            try:
                comment = {
                    'author': element.xpath('@author')[0] if element.xpath('@author') else "[已删除]",
                    'score': element.xpath('@score')[0] if element.xpath('@score') else "0",
                    'content': self._get_comment_content(element),
                    'avatar': self._get_comment_avatar(element),
                    'time': self._get_comment_time(element)
                }
                comments.append(comment)
            except Exception as e:
                print(f"解析评论失败: {e}")
                continue

        return comments, cursor

    def _get_comment_content(self, element):
        try:
            content = element.xpath('.//div[contains(@class, "md")]//text()')
            return " ".join([text.strip() for text in content if text.strip()])
        except:
            return ""

    def _get_comment_avatar(self, element):
        try:
            avatar = element.xpath('.//img[contains(@class, "avatar")]/@src')
            return avatar[0] if avatar else ""
        except:
            return ""

    def _get_comment_time(self, element):
        try:
            time = element.xpath('.//faceplate-timeago/@ts')
            return time[0] if time else ""
        except:
            return ""

    def second_page_comment_get(self, url, headers, cursor):
        comment_list = []
        params = {
            "render-mode": "partial",
            "top-level": "1",
            "comments-remaining": "1"
        }
        data = {
            "cursor": cursor
        }

        response = requests.post(url, headers=headers, params=params, data=data).content.decode('utf-8')
        with open('./second_html.html','w',encoding='utf-8') as f:
            f.write(response)
        et = etree.HTML(response)
        try:
            cursor = et.xpath('//input[@name="cursor"]/@value')[-1]
        except:
            cursor = None

        comments = []
        comment_elements = et.xpath('//shreddit-comment')

        for element in comment_elements:
            try:
                comment = {
                    'author': element.xpath('@author')[0] if element.xpath('@author') else "[已删除]",
                    'score': element.xpath('@score')[0] if element.xpath('@score') else "0",
                    'content': self._get_comment_content(element),
                    'avatar': self._get_comment_avatar(element),
                    'time': self._get_comment_time(element)
                }
                comments.append(comment)
            except Exception as e:
                print(f"解析评论失败: {e}")
                continue

        return comments, cursor

    def other_page_comment_get(self, url, cursor, headers):
        comment_list = []
        params = {
            "sort": "TOP",
            "top-level": "1"
        }
        data = {
            "cursor": cursor
        }

        if cursor:
            response = requests.post(url, headers=headers, params=params, data=data).content.decode('utf-8')
        else:
            response = requests.post(url, headers=headers, params=params).content.decode('utf-8')

        et = etree.HTML(response)
        try:
            cursor = et.xpath('//input[@name="cursor"]/@value')[-1]
        except:
            cursor = None

        comments = []
        comment_elements = et.xpath('//shreddit-comment')

        for element in comment_elements:
            try:
                comment = {
                    'author': element.xpath('@author')[0] if element.xpath('@author') else "[已删除]",
                    'score': element.xpath('@score')[0] if element.xpath('@score') else "0",
                    'content': self._get_comment_content(element),
                    'avatar': self._get_comment_avatar(element),
                    'time': self._get_comment_time(element)
                }
                comments.append(comment)
            except Exception as e:
                print(f"解析评论失败: {e}")
                continue

        return comments, cursor

    def format_timestamp(self, ts):
        try:
            dt = datetime.fromtimestamp(float(ts))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ts

    def write_to_txt(self, post_data, comments, filename, n):
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                # 写入帖子信息
                f.write("=" * 80 + "\n")
                f.write(f"帖子 {n}\n")
                f.write(f"标题: {post_data['title']}\n")
                f.write(f"作者: {post_data['author']}\n")
                f.write(f"发布时间: {self.format_timestamp(post_data['post_time'])}\n")
                f.write(f"点赞数: {post_data['score']}\n")
                f.write(f"评论数: {post_data['comment_count']}\n")
                f.write(f"订阅数: {post_data['subscribers']}\n")
                f.write("-" * 80 + "\n")
                f.write(f"内容:\n{post_data['content']}\n")
                f.write("=" * 80 + "\n\n")

                # 写入评论
                f.write("评论列表:\n")
                for comment in comments:
                    f.write("-" * 60 + "\n")
                    f.write(f"用户: {comment['author']}\n")
                    f.write(f"点赞: {comment['score']}\n")
                    f.write(f"时间: {self.format_timestamp(comment['time'])}\n")
                    f.write(f"内容:\n{comment['content']}\n")

                print(f"成功写入reddit_content_{str(n)}    耶！~~")
        except Exception as e:
            print(f"保存文件失败: {e}")

    def big_topic_get(self, headers):
        big_topic_url = input("论坛url：")
        each_url = []
        html_result = requests.get(url=big_topic_url, headers=headers).content.decode('utf-8')
        et = etree.HTML(html_result)
        # 拿到论坛第一页显示的推文
        first_page_visual_url = et.xpath(
            "//a[@class='block no-underline hover:no-underline active:no-underline']/@href")
        for i in first_page_visual_url:
            each_url.append(i)
        # 拿到触发异步加载的url，还需要循环拿其他异步加载的url
        other_page_url = "https://www.reddit.com" + et.xpath(
            "//faceplate-partial[@slot='load-after' and @loading='programmatic' and @method='GET']/@src")[0]
        for j in range(0, 6):
            # 拿异步加载的剩余推文，现在要来一个循环
            remaining_result = requests.get(url=other_page_url, headers=headers).content.decode('utf-8')
            et = etree.HTML(remaining_result)
            remaining_page_visual_url = et.xpath("//a[@target=\"_self\"]/@href")
            for i in remaining_page_visual_url:
                each_url.append(i)
            # 继续拿下一个异步加载
            other_page_url = "https://www.reddit.com" + et.xpath(
                "//faceplate-partial[@slot='load-after' and @loading='programmatic' and @method='GET']/@src")[0]
            print(other_page_url)
            time.sleep(0.1)
        print(len(each_url))
        return each_url

    def search_html(self):
        search_url = input("搜索url：")
        url_list = []

        for i in range(0, 4):
            try:
                response = requests.get(url=search_url, headers=self.headers)
                response.raise_for_status()
                search_result = response.content.decode('utf-8')
            except Exception as e:
                print(f"获取搜索页面失败: {e}")
                break

            et = etree.HTML(search_result)

            # 获取当前页面的帖子链接
            each_url = et.xpath('//a[@data0-testid="post-title"]/@href')
            for j in each_url:
                url_list.append(j)

            # 获取下一页的URL
            next_urls = et.xpath("//faceplate-partial[@loading='lazy']/@src")
            if not next_urls:
                print("没有找到更多页面，停止爬取")
                break

            # 过滤长度大于100的URL
            valid_urls = [url for url in next_urls if len(url) > 100]
            if not valid_urls:
                print("没有有效的下一页URL，停止爬取")
                break

            search_url = "https://www.reddit.com" + valid_urls[0]
            print(f"下一页URL: {search_url}")
            time.sleep(0.2)  # 添加延迟避免请求过快

        print(f"共获取到 {len(url_list)} 个帖子链接")
        return url_list

    def run(self):
        flag = int(input("论坛=>1  搜索=>2: "))
        if flag == 1:
            each_url = self.big_topic_get(self.headers)
        elif flag == 2:
            each_url = self.search_html()
        else:
            print("输入错误，程序退出")
            exit(1)

        n = int(input("从第几篇开始？: "))

        for url in each_url:
            # 先拿一下主html，从里面拿到主推文内容
            url = "https://www.reddit.com" + url
            html_content = self.html_get(url)
            if not html_content:
                print(f"无法获取页面: {url}")
                continue

            et, post_data = self.parse_post(html_content)
            # 再拿一下第一页评论url和评论内容
            first_page_comment_url = self.get_first_url(et)
            if not first_page_comment_url:
                print(f"无法获取评论URL: {url}")
                continue

            first_page_comment, cursor = self.first_page_comment_get(first_page_comment_url, self.headers, et)
            # 拿剩余所有评论
            other_page_comment_url = first_page_comment_url.replace('comments', 'more-comments').replace('r/', '')
            other_page_comment, cursor = self.second_page_comment_get(other_page_comment_url, self.headers, cursor)

            # 合并所有评论
            all_comments = first_page_comment + other_page_comment

            # 写入文件
            self.write_to_txt(post_data, all_comments, f'content/reddit_content_{str(n)}.txt', n)

            # 第二页有cursor的话继续拿其他页的评论
            if cursor and len(cursor) > 1000:
                flag = 1
                # 拿到下一页评论和cursor，cursor合法就继续拿
                while flag:
                    time.sleep(0.1)
                    other_page_comment, cursor = self.other_page_comment_get(other_page_comment_url, cursor,
                                                                             self.headers)
                    if other_page_comment:
                        self.write_to_txt({}, other_page_comment, f'massive_content/reddit_content_{str(n)}.txt', n)
                    if not cursor or len(cursor) < 1000:
                        flag = 0
            n += 1


if __name__ == '__main__':
    scraper = RedditScraper()
    scraper.run()