import json
import time
import requests
from jsonpath import jsonpath

def synthesis(cursor):
    params = {
        'variables': json.dumps({
            'focalTweetId': focalTweetId,
            'with_rux_injections': False,
            'rankingMode': 'Relevance',
            'includePromotedContent': True,
            'withCommunity': True,
            'withQuickPromoteEligibilityTweetFields': True,
            'withBirdwatchNotes': True,
            'withVoice': True,
            'cursor': cursor, # 如果需要分页，可以设置 cursor 参数
            'referrer': "tweet",  # 如果需要设置 referrer 参数
            'controller_data': None  # 如果需要设置 controller_data 参数
        }),
        'features': json.dumps({
            'rweb_video_screen_enabled': False,
            'profile_label_improvements_pcf_label_in_post_enabled': True,
            'rweb_tipjar_consumption_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'creator_subscriptions_tweet_preview_api_enabled': True,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'premium_content_api_read_enabled': False,
            'communities_web_enable_tweet_community_results_fetch': True,
            'c9s_tweet_anatomy_moderator_badge_enabled': True,
            'responsive_web_grok_analyze_button_fetch_trends_enabled': False,
            'responsive_web_grok_analyze_post_followups_enabled': True,
            'responsive_web_jetfuel_frame': False,
            'responsive_web_grok_share_attachment_enabled': True,
            'articles_preview_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': False,
            'responsive_web_grok_show_grok_translated_post': False,
            'responsive_web_grok_analysis_button_from_backend': False,
            'creator_subscriptions_quote_tweet_preview_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_grok_image_annotation_enabled': True,
            'responsive_web_enhance_cards_enabled': False
        }),
        'fieldToggles': json.dumps({
            'withArticleRichContentState': True,
            'withArticlePlainText': False,
            'withGrokAnalyze': False,
            'withDisallowedReplyControls': False
        })
    }
    return params

def get_response(params):
    response = requests.get(url=url, headers=headers, params=params)
    js_data = response.json()
    # print(js_data)
    with open('content.json', 'w', encoding='utf-8') as f:
        json.dump(js_data,f,ensure_ascii=False,indent=2)
    return js_data


def content_extract(js_data,filename):
    with open(f"{filename}.txt", "w", encoding='utf-8') as f:
        # 提取主推文数据
        main_tweet = js_data.get('data0', {}).get('threaded_conversation_with_injections_v2', {}).get('instructions', [])
        for instruction in main_tweet:
            if instruction.get('type') == 'TimelineAddEntries':
                entries = instruction.get('entries', [])
                for entry in entries:
                    if entry.get('entryId', '').startswith('tweet-'):
                        content = entry.get('content', {})
                        item_content = content.get('itemContent', {})
                        tweet_results = item_content.get('tweet_results', {})
                        result = tweet_results.get('result', {})
                        legacy = result.get('legacy', {})
                        if legacy:
                            f.write("=== 主推文 ===\n")
                            f.write(f"内容: {legacy.get('full_text', '')}\n")
                            f.write(f"点赞数: {legacy.get('favorite_count', 0)}\n")
                            f.write(f"评论数: {legacy.get('reply_count', 0)}\n")
                            f.write(f"转发数: {legacy.get('retweet_count', 0)}\n")
                            f.write(f"发布时间: {legacy.get('created_at', '')}\n\n")
                        break
                break

        # 提取评论数据
        for instruction in main_tweet:
            if instruction.get('type') == 'TimelineAddEntries':
                entries = instruction.get('entries', [])
                for entry in entries:
                    if entry.get('entryId', '').startswith('conversationthread-'):
                        content = entry.get('content', {})
                        items = content.get('items', [])
                        for item in items:
                            item_content = item.get('item', {}).get('itemContent', {})
                            tweet_results = item_content.get('tweet_results', {})
                            result = tweet_results.get('result', {})
                            legacy = result.get('legacy', {})
                            if legacy:
                                f.write("=== 评论 ===\n")
                                f.write(f"内容: {legacy.get('full_text', '')}\n")
                                f.write(f"点赞数: {legacy.get('favorite_count', 0)}\n")
                                f.write(f"发布时间: {legacy.get('created_at', '')}\n\n")

def get_cursor(js_data):
    # 提取 next_cursor
    next_cursor = jsonpath(js_data, '$.data0.threaded_conversation_with_injections_v2.instructions[*].entries[*].content.itemContent.value')
    return next_cursor[0] if next_cursor else None

if __name__ == '__main__':
    url = "https://x.com/i/api/graphql/b9Yw90FMr_zUb8DvA8r2ug/TweetDetail"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 QuarkPC/2.4.0.281',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'x-csrf-token': '18b471a80782813ac200a7552d6a19cfb44e551a962f4b35dc2882fbb10efca4190b0d842c9f002a20245daf6724d6b8cd54497afa7fe395fc857713e04707f884cc0f02df0c40af5af7324af3c66435',
        'cookie': 'guest_id=v1%3A174382166662437395; kdt=X1LL9ojJ5ZMAyS65LT851pLjc2sttidauDeFeGHK; auth_token=187ffa1ff2ae52ed8550984148b3d3ae1fba6eb3; ct0=18b471a80782813ac200a7552d6a19cfb44e551a962f4b35dc2882fbb10efca4190b0d842c9f002a20245daf6724d6b8cd54497afa7fe395fc857713e04707f884cc0f02df0c40af5af7324af3c66435; twid=u%3D1908191320901890048; personalization_id="v1_OmaLUkUDCOaM+M9+luWEyQ=="; guest_id_marketing=v1%3A174382166662437395; guest_id_ads=v1%3A174382166662437395; dnt=1; __cf_bm=rSEBCXOf.zQm374KzvQDzFCEKoGPCxYYFtR7W5lp4.8-1753189899-1.0.1.1-3FCJrTey2Z3DbXUCw0py_s1meGgAdhhp98Z31BPFngNhTuSt4tM2PgOgxw32e1b1NR8ml55ivfY5T7GUTSJI1wMI9noMFpnekzImcd7dcdA',
        'Cache-Control': 'no-cache, no-store, must-revalidate, pre-check=0, post-check=0'
    }
    print("如 https://x.com/GenshinImpact/status/1907251640023019683\n复制最后一串数字填入ID~")
    while True:
        focalTweetId = input("推文ID：")
        filename = focalTweetId
        # 初始化 cursor 为 None
        cursor = None
        while True:
            time.sleep(0.5)
            params = synthesis(cursor)
            js_data = get_response(params)
            content_extract(js_data,filename)
            # 获取下一个 cursor
            next_cursor = get_cursor(js_data)
            if not next_cursor:
                print("榨干哩~")
                break
            cursor = next_cursor