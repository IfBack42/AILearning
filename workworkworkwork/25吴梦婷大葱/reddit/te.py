import requests
import base64
import json
from lxml import etree


class RedditSearchScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        self.base_url = "https://www.reddit.com"
        self.api_url = "https://www.reddit.com/svc/shreddit/search/"

    def parse_post(self, html):
        """解析帖子链接"""
        tree = etree.HTML(html)
        posts = tree.xpath('//a[@data0-testid="post-title"]/@href')
        return [self.base_url + url for url in posts]

    def extract_metadata(self, html):
        """从HTML中提取cId和iId"""
        tree = etree.HTML(html)
        try:
            # 尝试从shreddit-app元素获取元数据
            shreddit_app = tree.xpath('//shreddit-app')[0]
            correlation_id = shreddit_app.get('correlation-id')
            server_render_id = shreddit_app.get('serverRenderId')
            return correlation_id, server_render_id
        except:
            return None, None

    def decode_cursor(self, cursor):
        """解码cursor参数"""
        try:
            decoded = base64.b64decode(cursor).decode('utf-8')
            return json.loads(decoded)
        except:
            return None

    def search(self, query, pages=4):
        """执行搜索"""
        all_posts = []
        current_url = f"{self.base_url}/search/?q={query}"
        cId, iId = None, None

        for page in range(pages):
            try:
                # 获取页面内容
                response = requests.get(current_url, headers=self.headers)
                html_content = response.text

                # 解析帖子链接
                posts = self.parse_post(html_content)
                all_posts.extend(posts)
                print(f"第 {page + 1} 页获取到 {len(posts)} 个帖子")

                # 第一页后提取元数据
                if page == 0:
                    cId, iId = self.extract_metadata(html_content)
                    if not cId or not iId:
                        cId = "2186ee23-5694-46f6-a92f-9c5c5f84ddcf"
                        iId = "4e4cb8ad-39ea-49f4-9a4c-fe914a712023"

                # 构造下一页API URL
                params = {
                    'q': query,
                    'cId': cId,
                    'iId': iId
                }

                # 获取下一页cursor (简化处理)
                next_cursor = "eyJjYW5kaWRhdGVzX3JldHVybmVkIjoie1wic2VjdGlvbl8xX3BpcGVsaW5lXzBfZ2xvYmFsX21vZGlmaWVyc1wiOlwiNlwiLFwic2VjdGlvbl8xX3BpcGVsaW5lXzFfbG9jYWxfbW9kaWZpZXJzXCI6XCI2XCIsXCJzZWN0aW9uXzJfcGlwZWxpbmVfNV9hbnN3ZXJzX3ByZXZpZXdcIjpcIjBcIixcInNlY3Rpb25fMl9waXBlbGluZV82X3Bvc3Rfc2VhcmNoXCI6XCIxNFwiLFwic2VjdGlvbl8zX3BpcGVsaW5lXzBfc3VicmVkZGl0X3NlYXJjaFwiOlwiNFwiLFwic2VjdGlvbl8zX3BpcGVsaW5lXzFfYXV0aG9yX3NlYXJjaFwiOlwiNFwifSIsImV4cGVyaWVuY2Vfc2VsZWN0aW9uIjoiYW5zd2Vyc19wcmV2aWV3X2FsbF93aXRoX3NpZGViYXIiLCJleHBlcmllbmNlX3ZlcnNpb24iOiJkZWZhdWx0Iiwic2VjdGlvbl8yX3BpcGVsaW5lXzZfcG9zdF9zZWFyY2giOiIxNCJ9"
                params['cursor'] = next_cursor

                # 构造下一页URL
                current_url = f"{self.api_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

            except Exception as e:
                print(f"获取第 {page + 1} 页失败: {e}")
                break

        return all_posts


# 使用示例
if __name__ == "__main__":
    scraper = RedditSearchScraper()
    search_query = "black+myth+wukong"
    results = scraper.search(search_query, pages=4)
    print(f"总共获取到 {len(results)} 个帖子链接")
    for i, url in enumerate(results[:10]):  # 打印前10个结果
        print(f"{i + 1}. {url}")