import json
import csv
import matplotlib.pyplot as plt
from gensim import corpora, models
from LDA_preprocess import preprocess_text

# 设置中文字体（根据你的系统调整）
plt.rcParams['font.sans-serif'] = ['SimHei']      # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False        # 解决负号显示问题

def model_init(dictionary, corpus, num_topics=9):
    """
    训练LDA模型
    """
    lda_model = models.LdaModel(
        corpus,
        num_topics=num_topics,
        id2word=dictionary,
        passes=30,
        alpha='asymmetric',
        eta='auto',
        iterations=500,
        random_state=42,
        eval_every=10
    )
    return lda_model

def preprocess_from_file(input_file):
    """
    从单个文件读取数据，每行是一个文档的原始文本。
    返回预处理后的文档列表，每个文档是分词后的词列表。
    """
    all_content = []
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line:                     # 跳过空行
            all_content.append(line)

    # 预处理：分词、去停用词等（preprocess_text需返回列表）
    processed_comments = [preprocess_text(comment) for comment in all_content]
    return processed_comments


def doc_cor(processed_comments):
    """
    构建词典和语料库
    """
    dictionary = corpora.Dictionary(processed_comments)
    # 根据数据量调整过滤参数
    dictionary.filter_extremes(
        no_below=1,       # 至少在2个文档中出现
        no_above=0.6,     # 出现在70%以上文档中的词被过滤
        keep_n=5000       # 保留最多5000个词
    )
    # 构建词袋模型
    corpus = [dictionary.doc2bow(text) for text in processed_comments]
    return corpus, dictionary




def topic_probability(lda_model, corpus):
    """
    获取每个文档的主题概率分布
    """
    doc_topics = []
    for doc_bow in corpus:
        topic_dist = lda_model.get_document_topics(
            doc_bow,
            minimum_probability=0,
            per_word_topics=False
        )
        doc_topics.append(topic_dist)
    return doc_topics


def format_topic_weights(model, dictionary, num_words=15):
    """
    格式化每个主题的关键词及权重
    """
    topics = []
    for topic_id in range(model.num_topics):
        word_weights = [
            (dictionary[int(word_id)], weight)
            for word_id, weight in model.get_topic_terms(topic_id, num_words)
        ]
        total = sum(weight for _, weight in word_weights)
        sorted_weights = sorted(
            [(word, round(weight / total, 4)) for word, weight in word_weights],
            key=lambda x: -x[1]
        )
        topics.append((topic_id, sorted_weights))
    return topics


def topic_print(lda_model, dictionary):
    """
    打印主题关键词
    """
    optimized_topics = format_topic_weights(lda_model, dictionary)
    for topic_id, word_weights in optimized_topics:
        print(f"\n主题 {topic_id+1} 权重分布（Top 15）：")
        for word, weight in word_weights:
            print(f"{word}: {weight:.2%}", end=' | ')
        print()


def visualize_topics(optimized_topics):
    """
    可视化主题关键词权重
    """
    num_topics = len(optimized_topics)
    # 动态计算子图行列数
    rows = (num_topics + 1) // 2
    cols = 2 if num_topics > 1 else 1
    plt.figure(figsize=(14, rows * 4))
    for idx, (topic_id, word_weights) in enumerate(optimized_topics):
        words, weights = zip(*word_weights[:10])  # 取前10个词
        plt.subplot(rows, cols, idx+1)
        plt.barh(words, weights)
        plt.gca().invert_yaxis()
        plt.title(f'主题 {topic_id+1} 关键词权重')
        plt.xlabel('概率')
    plt.tight_layout()
    plt.show()


def save_topic_probabilities(doc_topics, num_topics):
    """
    保存主题概率分布到CSV和JSON文件
    """
    # CSV原始格式（每个文档一行，每行是元组列表）
    with open("./topic_probability.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for doc_topic_dist in doc_topics:
            row = [f"({topic_id},{prob})" for topic_id, prob in doc_topic_dist]
            writer.writerow(row)

    # 简化CSV格式（每行是每个主题的概率）
    with open("./topic_probability_simple.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = [f"Topic_{i+1}" for i in range(num_topics)]
        writer.writerow(header)
        for doc_topic_dist in doc_topics:
            topic_probs = [0.0] * num_topics
            for topic_id, prob in doc_topic_dist:
                topic_probs[topic_id] = prob
            writer.writerow(topic_probs)

    print("已保存主题概率分布到以下文件:")
    print("  - topic_probability.csv")
    print("  - topic_probability_simple.csv")


def run(input_file, num_topics=9):
    """
    主流程
    """
    # 1. 数据预处理
    print("正在读取和预处理数据...")
    processed_comments = preprocess_from_file(input_file)
    print(f"共读取 {len(processed_comments)} 个文档。")

    # 2. 构建词典和语料库
    corpus, dictionary = doc_cor(processed_comments)
    print(f"词典大小: {len(dictionary)}")

    # 3. 训练LDA模型
    print("正在训练LDA模型...")
    lda_model = model_init(dictionary, corpus, num_topics)

    # 4. 输出主题
    topic_print(lda_model, dictionary)

    # 5. 获取文档主题分布并保存
    doc_topics = topic_probability(lda_model, corpus)
    save_topic_probabilities(doc_topics, num_topics)

    # 6. 可视化（可选）
    optimized_topics = format_topic_weights(lda_model, dictionary)
    visualize_topics(optimized_topics)

    return lda_model, dictionary, corpus


if __name__ == '__main__':
    input_file = "./data.txt"

    # 设置主题数（可根据需要调整）
    num_topics = int(input("请输入主题数量（默认9）：") or "9")

    model, dic, cur = run(input_file, num_topics)
    print("处理完成！")