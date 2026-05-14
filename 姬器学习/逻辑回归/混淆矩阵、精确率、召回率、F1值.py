"""
逻辑回归评估指标：
    精确率（预测正确）、召回率（不漏检）、F1值
混淆矩阵：用来描述真实值和预测值关系
                            预测标签（正例）                预测标签（反例）
            真实标签（正例）    真正例（TP）                     伪反例（FN）
            真实标签（反例）    伪正例（FP）                     真反例（TN）

        1.👉⭐根据业务需求选择正例⭐👈，正反例的选择会影响评估指标
        2.精确率 = 真正例在预测正例的占比 -> tp / （tp + fp）
        3.召回率 = 真正例在真正例中的占比 -> tp / （tp + fn）
        4.F1值 = 2 * (精确率*召回率) / （精确率+召回率）

"""
# 导包
import pandas as pd
from sklearn.metrics import confusion_matrix,precision_score,recall_score,f1_score

# 需求： 已知有10个样本，6个恶性肿瘤（正例），4个良性肿瘤（反例）
# 模型A预测结果： 预测对了3个恶性肿瘤，4个良性肿瘤
# 模型B预测结果： 预测对了6个恶性肿瘤，1个良性肿瘤
# 搭建混淆矩阵并计算精确率召回率F1值

#1. 定义变量，记录样本数据
y_train = ['恶性','恶性','恶性','恶性','恶性','恶性',   '良性','良性','良性','良性']

#2. 定义变量，记录模型A预测结果
A_y_pre = ['恶性','恶性','恶性','良性','良性','良性',   '良性','良性','良性','良性']

#3. B预测结果
B_y_pre = ['恶性','恶性','恶性','恶性','恶性','恶性',   '恶性','恶性','恶性','良性']

#4.标签没有默认，需手动标记正反例
label = ['恶性','良性']
df_label = ['恶性（正例）','良性（反例）']

#5. 针对真实结果和预测结果搭建混淆矩阵
confusion_matrix_A = confusion_matrix(y_train,A_y_pre) #先真实再预测
# print(confusion_matrix_A)
confusion_matrix_B = confusion_matrix(y_train,B_y_pre)

#6. 混淆矩阵转为DF
df_a = pd.DataFrame(confusion_matrix_A,index=df_label,columns=df_label)
df_b = pd.DataFrame(confusion_matrix_B,columns=df_label,index=df_label)
print(df_a)
print(df_b)

#7. 计算精确率，召回率，F1值
A_precison = precision_score(y_train,A_y_pre,pos_label='恶性')
B_precison = precision_score(y_train,B_y_pre,pos_label='恶性')

A_recall = recall_score(y_train,A_y_pre,pos_label='恶性')
B_recall = recall_score(y_train,B_y_pre,pos_label='恶性')

A_F1 = f1_score(y_train,A_y_pre,pos_label='恶性')
B_F1 = f1_score(y_train,B_y_pre,pos_label='恶性')

print(f'A精确率：{A_precison}')
print(f'B精确率：{B_precison}')
print(f'A召回率：{A_recall}')
print(f'B召回率：{B_recall}')
print(f'AF1：{A_F1}')
print(f'BF1：{B_F1}')










