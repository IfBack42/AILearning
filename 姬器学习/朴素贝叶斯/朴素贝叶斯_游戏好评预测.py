"""
STEAM游戏哦评 分析案例——朴素贝叶斯分类问题

####  步骤分析
- 1）获取数据
- 2）数据基本处理
  - 2.1） 取出内容列，对数据进行分析
  - 2.2） 判定评判标准
  - 2.3） 选择停用词
  - 2.4） 把内容处理，转化成标准格式
  - 2.5） 统计词的个数
  - 2.6）准备训练集和测试集
- 3）模型训练
- 4）模型评估
"""

import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# ----------------------------- 1. 读取数据 -----------------------------
data = pd.read_csv('./data/steam_comments_dataset.csv', encoding='utf-8')

print("原始数据前5行：")
print(data.head())
print(f"数据集形状：{data.shape}\n")

# 过滤x列长度小于5的行
data = data[data['x'].str.len() >= 10].reset_index(drop=True)
print(f"过滤后数据集形状：{data.shape}\n")

# ----------------------------- 2. 数据预处理 -----------------------------
# 2.1 增加标签列：1 -> 好评，0 -> 差评
data['labels'] = np.where(data['y'] == '不推荐', 0, 1)

# 2.2 提取特征列和标签列
X = data['x']      # 评论内容
y = data['labels'] # 标签

# ----------------------------- 3. 停用词表加载与检查 -----------------------------
stopword_path = './data/stopwords.txt'
try:
    with open(stopword_path, encoding='utf-8') as f:
        stopword_list = [line.strip() for line in f.readlines()]
    # 去重
    stopword_list = list(set(stopword_list))
    print(f"成功加载停用词表，共 {len(stopword_list)} 个停用词（去重后）")
    if len(stopword_list) == 0:
        print("警告：停用词表为空，请检查文件内容！")
except FileNotFoundError:
    print(f"错误：停用词文件不存在于 {stopword_path}，请确认路径。")
    stopword_list = []  # 若文件缺失，使用空列表

# ----------------------------- 4. 定义中文分词器 -----------------------------
import re

def chinese_tokenizer(text):
    words = jieba.lcut(text)
    # 过滤规则：
    # 1. 去除长度小于2的词（去掉标点、单字）
    # 2. 去除纯数字
    # 3. 可选：只保留中文、英文、数字（但建议保留英文单词）
    filtered_words = []
    for w in words:
        w = w.strip()
        if len(w) < 2:
            continue
        if w.isdigit():  # 纯数字
            continue
        # 如果想保留英文单词，去掉下面这行的注释
        # if re.match(r'^[a-zA-Z]+$', w):
        #     filtered_words.append(w.lower())
        #     continue
        # 保留包含中文的词，或者您也可以保留英文词
        if re.search(r'[\u4e00-\u9fff]', w):  # 包含中文字符
            filtered_words.append(w)
        # 如果也要保留英文词，可以加上 else 分支
        # else:
        #     # 保留长度>=2的英文词
        #     if len(w) >= 2 and w.isalpha():
        #         filtered_words.append(w.lower())
    return filtered_words

# ----------------------------- 5. TF-IDF 特征提取 -----------------------------
# 使用 TfidfVectorizer 替代 CountVectorizer
tfidf = TfidfVectorizer(
    tokenizer=chinese_tokenizer,
    stop_words=stopword_list,
    max_features=5000,      # 可选：限制特征数量，防止维度过高
    min_df=5,               # 忽略出现次数少于5的词
    max_df=0.8              # 忽略出现在80%以上文档中的词
)

# 打印前5条分词结果
print("\n分词结果示例（前5条）：")
for i in range(min(5, len(X))):
    tokens = chinese_tokenizer(X.iloc[i])
    print(f"原文：{X.iloc[i][:50]}...")
    print(f"分词：{' / '.join(tokens)}\n")

X_tfidf = tfidf.fit_transform(X)
print(f"TF-IDF 特征矩阵形状：{X_tfidf.shape}\n")

# 查看部分提取的特征词（可选）
feature_names = tfidf.get_feature_names_out()
print(f"示例特征词（前20个）：{feature_names[:20]}\n")

# ----------------------------- 6. 划分训练集和测试集 -----------------------------
# 使用随机划分，保证训练和测试的分布一致性，设置 random_state 使得结果可复现
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.15, random_state=42, stratify=y
)
print(f"训练集大小：{X_train.shape[0]}，测试集大小：{X_test.shape[0]}\n")

# 若您希望保留原始代码的前10条训练、后3条测试（不推荐小样本），可改用以下注释代码：
# X_train, X_test = X_tfidf[:10], X_tfidf[10:]
# y_train, y_test = y[:10], y[10:]

# ----------------------------- 7. 模型训练 -----------------------------

from sklearn.naive_bayes import ComplementNB

# estimator = ComplementNB()
estimator = MultinomialNB()
estimator.fit(X_train, y_train)

# ----------------------------- 8. 模型预测 -----------------------------
y_pred = estimator.predict(X_test)
print("预测结果（前10个）：", y_pred[:10])
print("真实标签（前10个）：", y_test.values[:10])

# ----------------------------- 9. 模型评估（完善版） -----------------------------
# 9.1 准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"\n模型整体准确率：{accuracy:.4f}")

# 9.2 分类报告（精确率、召回率、F1分）
print("\n分类报告：")
print(classification_report(y_test, y_pred, target_names=['差评', '好评']))

# 9.3 混淆矩阵（可视化）
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['差评', '好评'],
            yticklabels=['差评', '好评'])
plt.xlabel('预测标签')
plt.ylabel('真实标签')
plt.title('混淆矩阵')
plt.tight_layout()
plt.show()

# 额外输出各类别数量分布
print(f"测试集中实际差评数：{sum(y_test == 0)}，好评数：{sum(y_test == 1)}")

# ----------------------------- 10. 展示前5条分类结果 -----------------------------
# ----------------------------- 10. 展示前5条分类结果 -----------------------------
print("\n" + "=" * 60)
print("           📊 模型预测结果详情（前5条样本）")
print("=" * 60)
print(f"{'序号':<4} {'情感判定':<12} {'预测结果':<12} {'原文摘要'}")
print("-" * 60)

# 定义映射字典，将数字转换为人类可读的标签
label_map = {0: '❌ 差评', 1: '✅ 好评'}

# 获取测试集的前5个样本索引（注意：X_test是稀疏矩阵，y_test是Series，需要对齐索引）
for i in range(min(5, X_test.shape[0])):
    # 获取原始文本（需要从原始数据中根据测试集索引获取，这里简化处理取前5个测试样本对应的原始数据）
    # 注意：由于我们使用了 train_test_split，X_test 的索引是乱序的。
    # 为了简单展示，我们直接展示测试集的前5条。

    # 获取真实标签和预测标签
    true_label = y_test.iloc[i] if hasattr(y_test, 'iloc') else y_test[i]
    pred_label = y_pred[i]


    raw_text_sample = X.iloc[y_test.index[i] if hasattr(y_test, 'index') else i].strip('\n')

    # 判断预测是否正确
    result_status = "✔️ 正确" if true_label == pred_label else "❌ 错误"

    print(
        f"{i + 1:<4} {label_map[true_label]:<12} {label_map[pred_label]:<12} {result_status:<12} {raw_text_sample[:30]}...")
print("=" * 60)


