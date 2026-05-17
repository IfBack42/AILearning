# 07 gitignore / large files

这个模块解决一个问题：**哪些文件不该进 Git，以及大文件误提交后怎么办。**

## .gitignore 作用

`.gitignore` 只阻止“未被 Git 跟踪的文件”被 `git add` 加入。

它不会自动移除已经被跟踪或已经提交过的文件。

所以正确顺序是：

```bash
git init
先写 .gitignore
git status
git add 需要提交的文件
git commit
```

## 常见应该忽略的内容

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual env
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
**/sample_data/
!**/sample_data/
!**/sample_data/**

# Models
*.pkl
*.pt
*.pth
*.onnx
*.safetensors

# Outputs
output/
outputs/
result/
results/
*.log

# Archives and media
*.zip
*.rar
*.7z
*.mp4
*.avi
```

注意：如果你想保留小样例数据，不要全局忽略所有 `*.csv`。更推荐忽略 `data/`，保留 `sample_data/`。

## 检查某个文件是否被忽略

```bash
git check-ignore -v 文件路径
```

查看所有忽略文件：

```bash
git status --ignored
```

## 文件已经被跟踪怎么办

只从 Git 跟踪中移除，保留本地文件：

```bash
git rm --cached 文件名
```

目录：

```bash
git rm -r --cached 目录名
```

然后提交：

```bash
git commit -m "移除大文件跟踪"
```

你之前处理 Reddit 评论数据时，就是这种情况：

```bash
git rm -r --cached workworkworkwork/25吴梦婷大葱/reddit/content
git rm -r --cached workworkworkwork/25吴梦婷大葱/reddit/extracted_comments
git commit -m "移除 Reddit 评论数据跟踪"
```

本地文件还在，只是 Git 不再跟踪。

## 文件已经进历史怎么办

如果大文件已经 commit 进历史，即使当前删除了，Git 仓库体积仍可能很大。

这时普通 `.gitignore` 和 `git rm --cached` 不够，需要清理历史。

常用工具：

```text
git filter-repo
BFG Repo-Cleaner
```

这类操作会改写历史，风险比普通命令高。做之前要确认：

- 是否已经 push 到远程
- 是否有别人基于这个仓库开发
- 是否需要备份

## GitHub 大文件限制

GitHub 单文件超过约 100MB 会拒绝普通 push。

更适合的方式：

- 小样例数据放 `sample_data/`
- 完整数据集放网盘、对象存储或 Kaggle
- 模型权重放 Release、网盘或 Git LFS

## Git LFS

Git LFS 用来管理大文件。

常见流程：

```bash
git lfs install
git lfs track "*.pt"
git lfs track "*.pkl"
git add .gitattributes
git add 模型文件.pt
git commit -m "使用 Git LFS 管理模型文件"
```

但是学习仓库一般先别急着用 LFS。先把大数据和模型忽略掉，仓库保持轻量。

## 判断文件该不该进 Git

问自己四个问题：

1. 这是源码或文档吗？
2. 别人理解项目必须要它吗？
3. 它能不能重新生成？
4. 它是不是很大或包含隐私？

通常：

- 源码、README、学习笔记：提交
- 数据集、模型、运行输出、缓存、环境：忽略
- 小样例数据：可以提交

