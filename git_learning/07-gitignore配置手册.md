# 07 gitignore 配置手册

这一节专门学习 `.gitignore`。

`.gitignore` 的作用是告诉 Git：哪些文件不需要纳入版本管理。

它不是用来删除文件的，也不是用来隐藏文件的。它只影响 Git 是否把这些文件加入版本控制。

## 为什么需要 .gitignore

一个项目里通常有两类文件：

第一类是应该提交的文件：

- 源代码：`.py`、`.sql`、`.ipynb`
- 文档：`README.md`、学习笔记
- 配置模板：`.env.example`
- 小样例数据：`sample_data/`

第二类是不适合提交的文件：

- 虚拟环境：`.venv/`
- 编辑器配置：`.idea/`、`.vscode/`
- 缓存：`__pycache__/`
- 大数据集：`data/`、`dataset/`
- 模型权重：`.pkl`、`.pt`、`.pth`
- 密钥和密码：`.env`、`.pem`
- 临时输出：`output.csv`、`result.txt`

`.gitignore` 就是用来过滤第二类文件的。

## 基本写法

忽略某个文件：

```gitignore
test.txt
```

忽略某类后缀：

```gitignore
*.log
*.tmp
```

忽略某个文件夹：

```gitignore
.venv/
__pycache__/
```

忽略任意层级下的某个文件夹：

```gitignore
**/data/
**/dataset/
**/outputs/
```

## 常见符号含义

### `#`：注释

```gitignore
# Python cache
__pycache__/
```

`#` 后面的内容是说明文字，不会被 Git 当成规则。

### `*`：匹配任意字符

```gitignore
*.log
```

表示忽略所有 `.log` 文件，例如：

```text
debug.log
run.log
error.log
```

### `/`：表示目录

```gitignore
data/
```

表示忽略名为 `data` 的目录。

如果不加 `/`：

```gitignore
data
```

它可能同时匹配文件和目录。初学时建议目录都加 `/`，更清楚。

### `**`：匹配任意层级目录

```gitignore
**/data/
```

表示不管 `data` 在哪里，都忽略。

例如：

```text
机器学习/KNN/data/
deep_learning/day06/data/
workworkworkwork/数模/data/
```

都会被忽略。

### `!`：反向保留

```gitignore
*.env
!.env.example
```

意思是：

- 忽略所有 `.env` 相关文件
- 但是保留 `.env.example`

这很常见，因为真实 `.env` 可能有密码，但 `.env.example` 可以告诉别人需要哪些配置项。

## 路径匹配规则

### 只写文件名

```gitignore
output.csv
```

表示忽略任意位置叫 `output.csv` 的文件。

### 写具体路径

```gitignore
workworkworkwork/数模/output.csv
```

表示只忽略这个具体位置的文件。

### 忽略所有同名目录

```gitignore
data/
```

通常会忽略任意位置的 `data` 目录。

为了表达得更明确，也可以写：

```gitignore
**/data/
```

### 忽略某目录下所有内容

```gitignore
models/
```

表示忽略 `models` 整个目录。

也可以写：

```gitignore
models/*
```

区别是：`models/` 更常用，意思更直接。

## 命名规则建议

`.gitignore` 不是随便堆规则，最好按类别分组。

推荐结构：

```gitignore
# Python cache
__pycache__/
*.py[cod]

# Virtual environments
.venv/
venv/

# IDE files
.idea/
.vscode/

# Data and model files
**/data/
*.pkl
*.pt

# Outputs
output/
result.*
```

这样以后你回来维护时，能快速知道每一组规则是干什么的。

## 什么文件应该忽略

可以用下面这个判断表。

| 文件类型 | 是否提交 | 原因 |
| --- | --- | --- |
| `.py` 源代码 | 提交 | 项目核心内容 |
| `.md` 文档 | 提交 | 方便别人理解项目 |
| `.ipynb` 笔记 | 通常提交 | 学习项目里有价值 |
| `.venv/` | 忽略 | 本地虚拟环境，体积大且别人不能直接复用 |
| `.idea/` | 忽略 | 编辑器个人配置 |
| `__pycache__/` | 忽略 | Python 自动生成缓存 |
| `.env` | 忽略 | 可能有密钥、密码 |
| `.env.example` | 提交 | 给别人看配置模板 |
| 大型 CSV / XLSX | 看情况 | 小样例可提交，大数据集建议忽略 |
| `.pkl` / `.pt` / `.pth` | 通常忽略 | 模型文件通常很大 |
| `output.csv` / `result.txt` | 通常忽略 | 程序运行结果，可重新生成 |

## 学习项目的推荐策略

你的项目是 AI 学习仓库，所以建议：

提交：

- 学习代码
- README
- Git 学习笔记
- SQL 练习
- 小型 Notebook
- 小样例数据

忽略：

- 完整数据集
- 模型文件
- 爬虫下载结果
- 视频、压缩包
- 数模附件大文件
- 运行输出结果
- 本地环境和缓存

## 如何检查规则是否生效

使用：

```bash
git status --ignored
```

它会显示哪些文件被忽略了。

也可以检查某一个文件为什么被忽略：

```bash
git check-ignore -v 文件路径
```

例如：

```bash
git check-ignore -v deep_learning/day06/data/train.csv
```

输出里会告诉你：是哪一行 `.gitignore` 规则忽略了它。

## 常见误区

### 误区 1：写了 .gitignore，已提交的大文件就会消失

不会。

`.gitignore` 只对“还没有被 Git 跟踪的文件”生效。

如果一个大文件已经被提交过，需要另外处理：

```bash
git rm --cached 文件名
```

这表示从 Git 跟踪中移除，但保留本地文件。

### 误区 2：什么数据都不能传

不是。

小样例数据可以传，尤其是能帮助别人运行你的代码时。

推荐做法：

```text
sample_data/
```

把很小的一份示例数据放进去，完整数据集放网盘或不上传。

### 误区 3：直接忽略所有 csv

不一定合适。

比如：

```gitignore
*.csv
```

会忽略所有 CSV。这样虽然安全，但可能把你想展示的小样例数据也忽略掉。

更好的写法：

```gitignore
**/data/
output.csv
*_result.csv
!**/sample_data/*.csv
```

这样能忽略大数据和结果文件，同时保留样例数据。

## 一个适合 AI 学习仓库的模板

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual environment
.venv/
venv/

# IDE
.idea/
.vscode/

# Secrets
.env
.env.*
!.env.example

# Data
**/data/
**/dataset/
**/datasets/
!**/sample_data/
!**/sample_data/**

# Models
*.pkl
*.joblib
*.pt
*.pth
*.ckpt
*.onnx
*.safetensors

# Outputs
output/
outputs/
result/
results/
output.*
result.*
*_result.*
*_summary.*

# Archives and media
*.zip
*.rar
*.7z
*.mp4
*.avi
```

## 我自己的配置原则

每次写 `.gitignore` 前，先问 4 个问题：

1. 这个文件是不是我亲手写的源码或文档？
2. 这个文件是不是别人运行项目必须要的？
3. 这个文件是不是很大，或者可以重新生成？
4. 这个文件里有没有隐私、密码、密钥？

如果是源码和文档，通常提交。

如果是大文件、缓存、环境、模型、运行结果，通常忽略。

如果是别人运行项目需要的数据，尽量只提交一小份 `sample_data/`。

