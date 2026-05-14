# 导入必要的库
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
import matplotlib.pyplot as plt
import warnings

# 忽略警告信息
warnings.filterwarnings('ignore')

# 确保使用的是 TensorFlow 2.x
assert tf.__version__.startswith('2'), "请确保使用 TensorFlow 2.x 版本。"

# 1. 数据生成：构建一个自定义图结构
num_nodes = 10  # 节点数量
feature_dim = 5  # 每个节点的特征维度

# 随机生成节点特征矩阵，形状为 (num_nodes, feature_dim)
X = np.random.rand(num_nodes, feature_dim)  # 每个节点有5个特征

# 随机生成邻接矩阵A，形状为 (num_nodes, num_nodes)
A = np.random.randint(0, 2, size=(num_nodes, num_nodes))  # 生成0和1的随机矩阵，表示是否有边
A = np.triu(A)  # 保证上三角矩阵对称
A += A.T - np.diag(A.diagonal())  # 生成对称邻接矩阵，表示无向图

# 打印节点特征和邻接矩阵
print(f"节点特征矩阵:\n{X}\n")
print(f"邻接矩阵:\n{A}\n")

# 扩展邻接矩阵为适合批次输入的形状
A = np.expand_dims(A, axis=0)  # 现在A的形状为 (1, num_nodes, num_nodes)


# 2. 图神经网络（GNN）的改进实现

# 定义图卷积层
class GraphConvolution(layers.Layer):
    def __init__(self, output_dim, use_bias=True, l2_reg=0.01):
        super(GraphConvolution, self).__init__()
        self.output_dim = output_dim  # 图卷积输出的维度
        self.use_bias = use_bias  # 是否使用偏置
        self.l2_reg = l2_reg  # L2正则化系数

    def build(self, input_shape):
        # 定义权重矩阵，形状为 (输入维度, 输出维度)
        self.kernel = self.add_weight(
            shape=(input_shape[-1], self.output_dim),
            initializer='glorot_uniform',
            regularizer=tf.keras.regularizers.L2(self.l2_reg),
            trainable=True
        )
        if self.use_bias:
            # 如果使用偏置，定义偏置向量
            self.bias = self.add_weight(
                shape=(self.output_dim,),
                initializer='zeros',
                trainable=True
            )

    def call(self, inputs, adj):
        # 计算图卷积的前向传播
        support = tf.matmul(inputs, self.kernel)  # 计算支持矩阵，表示X * W
        output = tf.matmul(adj, support)  # 将支持矩阵与邻接矩阵A相乘，进行邻接矩阵传播
        if self.use_bias:
            output += self.bias  # 如果使用偏置，加上偏置
        return output  # 返回图卷积的输出


# 定义改进的图神经网络模型
def build_gnn(input_dim, output_dim, num_hidden, num_nodes, dropout_rate=0.5):
    # 输入层：输入节点特征和邻接矩阵
    node_features = layers.Input(shape=(num_nodes, input_dim), name="Node_Features")  # 节点特征输入
    adj_matrix = layers.Input(shape=(num_nodes, num_nodes), name="Adjacency_Matrix")  # 邻接矩阵输入

    # 第一层图卷积层
    x = GraphConvolution(num_hidden)(node_features, adj_matrix)  # 第一层图卷积，输出隐藏层
    x = layers.ReLU()(x)  # 激活函数ReLU
    x = layers.Dropout(dropout_rate)(x)  # 添加Dropout层防止过拟合

    # 第二层图卷积层
    x = GraphConvolution(output_dim)(x, adj_matrix)  # 第二层图卷积，输出层

    # 定义模型
    model = Model(inputs=[node_features, adj_matrix], outputs=x)  # 构建图神经网络模型
    return model


# 3. 定义模型
input_dim = X.shape[1]  # 输入维度为节点特征的维度
output_dim = 2  # 输出维度，假设要进行二分类任务
num_hidden = 32  # 增加隐藏层维度
dropout_rate = 0.5  # 设置Dropout率为50%

# 扩展节点特征矩阵以适应batch_size为1的情况
X = np.expand_dims(X, axis=0)  # 现在X的形状为 (1, num_nodes, feature_dim)

gnn_model = build_gnn(input_dim, output_dim, num_hidden, num_nodes, dropout_rate)  # 创建改进后的GNN模型
gnn_model.summary()  # 打印模型结构

# 4. 编译模型
gnn_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='categorical_crossentropy',
                  metrics=['accuracy'])  # 调低学习率，编译模型

# 5. 训练模型
# 假设Y是一个one-hot编码的标签矩阵
Y = np.random.randint(2, size=(1, num_nodes, 2))  # 生成随机的二分类标签，模拟数据
history_gnn = gnn_model.fit([X, A], Y, epochs=2000, batch_size=1, verbose=1)  # 使用图数据（节点特征X和邻接矩阵A）训练模型

# 6. 模型评估与预测
Y_pred = gnn_model.predict([X, A])  # 使用模型进行预测
print("预测结果:", Y_pred)  # 打印预测结果


# 定义模型评价函数
def evaluate_model(Y_true, Y_pred, dataset_type="数据集"):  # 输入真实值和预测值，计算模型性能
    mse = mean_squared_error(Y_true.flatten(), Y_pred.flatten())  # 计算均方误差
    mae = mean_absolute_error(Y_true.flatten(), Y_pred.flatten())  # 计算平均绝对误差
    r2 = r2_score(Y_true.flatten(), Y_pred.flatten())  # 计算R²得分
    evs = explained_variance_score(Y_true.flatten(), Y_pred.flatten())  # 计算解释方差得分
    print(f"{dataset_type} - MSE: {mse:.4f}")  # 打印MSE
    print(f"{dataset_type} - MAE: {mae:.4f}")  # 打印MAE
    print(f"{dataset_type} - R²: {r2:.4f}")  # 打印R²得分
    print(f"{dataset_type} - EVS: {evs:.4f}\n")  # 打印EVS


# 评估模型性能
evaluate_model(Y, Y_pred, "图神经网络")

# 7. 结果可视化
plt.figure(figsize=(14, 6))  # 创建画布，设置大小
plt.subplot(1, 2, 1)  # 创建子图
plt.scatter(Y.flatten(), Y_pred.flatten(), color='blue', alpha=0.5, label='预测值')  # 绘制真实值与预测值的散点图
plt.plot([Y.flatten().min(), Y.flatten().max()], [Y.flatten().min(), Y.flatten().max()], 'k--', lw=2,
         label='理想情况')  # 绘制理想的参考线
plt.xlabel('真实值')  # 设置x轴标签
plt.ylabel('预测值')  # 设置y轴标签
plt.title('图神经网络预测值 vs 真实值')  # 设置标题
plt.legend()  # 显示图例

plt.tight_layout()  # 自动调整子图间的布局，避免重叠
plt.show()  # 显示图像
