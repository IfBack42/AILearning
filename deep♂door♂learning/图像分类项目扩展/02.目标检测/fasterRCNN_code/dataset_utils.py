# 1.导入依赖包
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# 2.图像展示
def show_images(imgs, num_rows, num_cols, titles=None, scale=8):
    figsize = (num_cols * scale, num_rows * scale)
    _, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    axes = axes.flatten()
    for i, (ax, img) in enumerate(zip(axes, imgs)):
        ax.imshow(img)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        if titles and len(titles) > i:
            ax.set_title(titles[i])
    return axes


# 3.框的展示
def show_bboxes(axes, bboxes, labels=None, colors=None):
    def _make_list(obj, default_values=None):
        if obj is None:
            obj = default_values
        elif not isinstance(obj, (list, tuple)):
            obj = [obj]
        return obj

    labels = _make_list(labels)
    colors = _make_list(colors, ['b', 'g', 'r', 'm', 'c'])
    for i, bbox in enumerate(bboxes):
        color = colors[i % len(colors)]
        rect = plt.Rectangle(
            xy=(bbox[0], bbox[1]),
            width=bbox[2] - bbox[0],
            height=bbox[3] - bbox[1],
            fill=False,
            edgecolor=color,
            linewidth=2)
        axes.add_patch(rect)
        if labels and len(labels) > i:
            text_color = 'k' if color == 'w' else 'w'
            axes.text(rect.xy[0], rect.xy[1], labels[i], va='center',
                      ha='center', fontsize=9, color=text_color,
                      bbox=dict(facecolor=color, lw=0))


if __name__ == "__main__":
    train_data_dir = 'wheatData/train'
    test_data_dir = 'wheatData/test'
    # 1 读取CSV文件
    train_data_label = pd.read_csv('wheatData/train_data.csv')
    print(train_data_label.head())
    print("框的个数：{}".format(train_data_label.shape))
    print("标注图片的个数：{}".format(train_data_label['image_id'].nunique()))
    print("图片的个数：{}".format(len(os.listdir(train_data_dir))))

    # 2 统计每张图片中目标个数
    counts = train_data_label['image_id'].value_counts()
    sns.displot(counts, kde=True, color='r')
    plt.xlabel('boxes')
    plt.ylabel('images')
    plt.show()
    print(min(counts))
    print(max(counts))

    # 3 左上角坐标
    sns.histplot(data=train_data_label, x='x', y='y', bins=50)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    # 4 中心点坐标
    train_data_label['cx'] = train_data_label['x'] + train_data_label['w'] / 2
    train_data_label['cy'] = train_data_label['y'] + train_data_label['h'] / 2
    sns.histplot(data=train_data_label, x='cx', y='cy', bins=50)
    plt.xlabel('cx')
    plt.ylabel('cy')
    plt.show()
    # 5 宽高
    sns.histplot(data=train_data_label, x='w', y='h', bins=50)
    plt.xlabel('w')
    plt.ylabel('h')
    plt.show()
    # 6 面积
    aeras = train_data_label['w'] * train_data_label['h']
    sns.histplot(aeras, bins=50)
    plt.show()

    # 图片及标注框预览
    # 设置坐标轴的够长
    num_rows, num_cols = 1, 2
    # 获取标注信息
    ids = train_data_label['image_id'].unique()[120:120 + num_rows * num_cols]
    # 读取图片
    imgs = [plt.imread(f'{train_data_dir}/{n}.jpg') for n in ids]
    # 图片显示
    axes = show_images(imgs, num_rows, num_cols)
    # 显示标注框
    for ax, id in zip(axes, ids):
        datas = train_data_label[train_data_label['image_id'] == id]
        bboxes = [(d['x'], d['y'], d['x'] + d['w'], d['y'] + d['h']) for _, d in datas.iterrows()]
        show_bboxes(ax, bboxes, colors=['r'])
    plt.show()
