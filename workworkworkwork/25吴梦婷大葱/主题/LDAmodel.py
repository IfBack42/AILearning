import json

from preprocess import preprocess_text
from gensim import corpora, models
import pandas as pd
import csv
import matplotlib.pyplot as plt


"""
get_topic_terms()	       获取主题关键词及权重	        [(词ID, 权重)]
print_topics()	           打印主题关键词（字符串格式）	    ["0.024*'游戏' + ..."]
get_document_topics()      获取文档的主题分布	            [(主题ID, 概率)]
get_term_topics()	       获取词项的主题分布	            [(主题ID, 权重)]
log_perplexity()	       计算对数困惑度	                -5.23
alpha 和 eta	           获取自动调整后的超参数	        alpha=[0.1, 0.2, ...], eta=0.01
show_topics()	           返回格式化主题信息	            字符串或词权重列表
"""

# plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
# plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
def preprocess(n):
    # 数据预处理
    all_content = []
    for i in range(1,n+1):
        with open(f'../reddit/massive_content/reddit_content_{i}.txt', 'r', encoding='utf-8') as f:
            data = f.read()
        raw_comments = [line.strip() for line in data.split('\n') if line.strip()]
        each_text = ' '.join(raw_comments[4:])
        all_content.append(each_text)
    print('-'*50)
    processed_comments = [preprocess_text(comment) for comment in all_content]   #这里处理后会变成二维数组
    # print(processed_comments)
    return processed_comments

def doc_cor(processed_comments):
    # 构建词典时的优化
    # 词典类似词汇表，给每个词一个下标，如  {'I': 0, 'amazing': 1, 'builds': 2, 'Deep': 3, 'is': 4, 'learning': 5, 'love': 6, 'Machine': 7, 'machine': 8, 'on': 9}
    # 这是一个全局过程，把所有子列表出现的词构建为一个字典
    dictionary = corpora.Dictionary(processed_comments)
    dictionary.filter_extremes(
        no_below=10,  # 提升低频词过滤阈值
        no_above=0.65,  # 降低高频词保留比例
        keep_n=3000,  # 扩大保留词汇量
    )
    print(len(dictionary))
    # 转换为向量时过滤空文档
    # corpus = [dictionary.doc2bow(text) for text in processed_comments if len(text) > 0]
    corpus = [dictionary.doc2bow(text) for text in processed_comments]
    # print(corpus)
    return corpus,dictionary

def model_init(dictionary,corpus):
    # 优化LDA模型参数
    lda_model = models.LdaModel(
        corpus,
        num_topics=9,
        id2word=dictionary,
        passes=30,  # 增加迭代轮次至50
        alpha='asymmetric',  # 强制主题稀疏性，优先生成少数强文化主题
        eta='auto',  # 经验值，提升文化相关词分布权重
        iterations=500,  # 增加单次迭代至800
        random_state=42,
        eval_every=10  # 每10次评估模型收敛性
    )
    return lda_model

#获取主题概率分布
def topic_probability(lda_model,corpus):
    doc_topics = []
    for doc_bow in corpus:
        topic_dist = lda_model.get_document_topics(
            doc_bow,
            minimum_probability=0,
            per_word_topics=False
        )
        doc_topics.append(topic_dist)
    return doc_topics
# print(doc_topics)
# print(len(doc_topics))


# 获取自动学习后的alpha参数（主题先验分布）
# alpha = lda_model.alpha  # 返回长度为num_topics的numpy数组
# 获取自动学习后的eta参数（词项先验分布）
# eta = lda_model.eta      # 返回形状为(num_topics, vocab_size)的numpy数组
# print(f"alpha:{alpha}")
# print(f"eta:{eta}")

# 权重计算与格式化输出
def format_topic_weights(model,dictionary, num_words=15):
    topics = []
                            #    ↓这里就是自己设置的模型主题数
    for topic_id in range(model.num_topics):
                        #    ↓这里拿到字典里面对应id的单词,权重为get_term_topics()计算得到
        word_weights = [(dictionary[int(word_id)], weight) for word_id, weight in model.get_topic_terms(topic_id, num_words)]
        # 转换为实际概率并排序
        total = sum(weight for _, weight in word_weights)
        sorted_weights = sorted([(word, round(weight/total, 4)) for word, weight in word_weights],key=lambda x: -x[1])
        topics.append((topic_id, sorted_weights))
    return topics

def topic_print(lda_model,dictionary):
    # 获取优化后的主题权重
    optimized_topics = format_topic_weights(lda_model,dictionary)

    # 打印带权重的主题
    for topic_id, word_weights in optimized_topics:
        print(f"\n主题 {topic_id +1} 权重分布（Top 15）：")
        for word, weight in word_weights:
            print(f"{word}: {weight:.2%}", end=' | ')

def run(n):
    processed_comments = preprocess(n)
    cur,dic = doc_cor(processed_comments)
    model = model_init(dic,cur)
    return model,dic,cur


if __name__ == '__main__':
    n = int(input("总文档数："))
    model, dic, cur = run(n)
    topic_print(model, dic)
    doc_topics = topic_probability(model, cur)
    print(f"处理了 {len(doc_topics)} 个文档的主题分布")

    # 保存为CSV格式，每行代表一个文档的主题分布
    with open("./topic_probability.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for doc_topic_dist in doc_topics:
            # 将每个文档的主题分布写成一行，格式为 (主题ID,概率)
            row = [f"({topic_id},{prob})" for topic_id, prob in doc_topic_dist]
            writer.writerow(row)

    # 同时保存为JSON格式，更便于程序读取
    with open("./topic_probability.json", 'w', encoding='utf-8') as f:
        json.dump(doc_topics, f, ensure_ascii=False, indent=2)

    # 保存为简化格式的CSV，便于查看
    with open("./topic_probability_simple.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入表头
        header = [f"Topic_{i}" for i in range(9)]  # 假设有16个主题
        writer.writerow(header)
        # 写入每个文档的数据
        for doc_topic_dist in doc_topics:
            # 创建一个包含所有主题概率的列表
            topic_probs = [0.0] * 9  # 初始化为0
            for topic_id, prob in doc_topic_dist:
                topic_probs[topic_id] = prob
            writer.writerow(topic_probs)

    print(f"已保存主题概率分布到以下文件:")
    print(f"  - topic_probability.csv: 原始格式")
    print(f"  - topic_probability.json: JSON格式")
    print(f"  - topic_probability_simple.csv: 简化CSV格式")






# # 可视化优化
# plt.figure(figsize=(14, 8))
# for topic_id, word_weights in optimized_topics:  # 展示前4个主题
#     words, weights = zip(*word_weights[:10])  # 取前10个词
#     plt.subplot(2, 2, topic_id+1)
#     plt.barh(words, weights)
#     plt.gca().invert_yaxis()
#     plt.title(f'主题 {topic_id} 关键词权重')
#     plt.xlabel('概率分布')
# plt.tight_layout()
# plt.show()
#
# # 保存结果到CSV（可选）
# df = pd.DataFrame(
#     [(topic_id, word, weight) for topic_id, words in optimized_topics for word, weight in words],
#     columns=['主题ID', '关键词', '权重']
# )
# df.to_csv('topic_weights.csv', index=False, encoding='utf-8-sig')