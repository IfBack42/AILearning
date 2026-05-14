import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# 显式下载资源并提示
nltk_resources = ['punkt', 'stopwords', 'wordnet']
for res in nltk_resources:
    try:
        nltk.data.find(f'tokenizers/{res}' if res == 'punkt' else f'corpora/{res}')
    except LookupError:
        print(f"正在下载 NLTK 资源：{res}...")
        nltk.download(res)
        print(f"{res} 下载完成！")

lemmatizer = WordNetLemmatizer()
# preprocess.py 修改建议
custom_stop_words = {
    # 移除可能包含文化元素的游戏术语
    # 'boss', 'dodge', 'combo' ← 原设置可能过滤关键文化载体
    'lol', '😂', 'share', 'flair', 'infraction',  # 保留纯操作类词汇
    'rock','controller','quest','code','dlc','link', 'message', 'summons', 'bonk', 'pull', 'rail', 'cosplay',
    'frog', 'rat', 'goty', 'review', '10/10', 'steam', 'studio', 'anniversary', 'hsr', 'rail', '50/50', 'pity', 'sell', 'steam',
    'burst', 'dp', 'kratos', 'goku', 'ign', 'bot', 'bonk', 'quest',
    '/10', 'exploration', 'tamer', 'fucker', 'tornado',    'billion', 'box', 'million', 'dub', 'ccp', 'party', 'government',
    # 新增游戏术语
    'genshin', 'mihoyo', 'va', 'netflix',
    # 新增口语化噪音
    'bruh', 'monke', 'dog', 'mile',
    # 新增中文停用词
    '内容', '点赞', '用户', '时间', '浏览量', '简介', '标题'
}

custom_stop_words.update({
    # 新增游戏机制词汇
    'hsr', 'gacha', 'grind', 'nerf', 'buff',
    # 新增社区互动词汇
    'upvote', 'spoiler', 'mods', 'subreddit',
    # 新增通用噪音词
    'lmao', 'btw', 'imo', 'tbh'
})
cultural_whitelist = {
    'nezha', 'tang', 'bodhisattva', 'pilgrim', 'kingdom', 'jade',
    'yellowbrow', 'lingji', 'whiteclad', 'temple', 'soulslike'
}
stop_words = set(stopwords.words('english')).union(custom_stop_words)
# 扩展停用词表
custom_stop_words.update({
    'anniversary', 'hsr', 'rail', '50/50', 'pity', 'sell', 'steam',
    'burst', 'dp', 'kratos', 'goku', 'ign', 'bot', 'bonk', 'quest',
    'exploration', 'tamer', 'fucker', 'tornado', 'banner', 'pulling'
})

# 正则表达式优化（修改preprocess_text函数）
def preprocess_text(text):
    # 过滤掉URL、数字和非英文字符
    text = re.sub(r'http\S+|www\S+|\d+|[^\x00-\x7F]+', ' ', text, flags=re.I)
    # 过滤特殊符号
    text = re.sub(r'[^\w\s\-]', ' ', text)
    # 保护连字符（如Zhongyuan-Jie）
    text = re.sub(r'(?<!\w)-(?!\w)', '', text)
    tokens = word_tokenize(text)
    return [
        lemmatizer.lemmatize(word.lower())
        for word in tokens
        if len(word) > 1 and word.lower() not in stop_words and word.isalpha()
    ]
#
# def preprocess_text(text):
#     text = re.sub(r'http\S+|www\S+', '', text, flags=re.I)  # 保留数字和符号
#     text = re.sub(r'(?<!\w)[^a-zA-Z\-\s](?!\w)', '', text)  # 弱化标点过滤
#     tokens = word_tokenize(text)
#     return [lemmatizer.lemmatize(word.lower())
#             for word in tokens if len(word) > 2 and word not in stop_words]  # 保留短词
