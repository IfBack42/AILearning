# 01 status / diff / add / commit

这个模块解决一个问题：**如何看清当前改动，并组织成一次干净的提交。**

## 核心心法

不要上来就 `git add .`。

进阶一点的流程是：

```bash
git status
git diff
git add 指定文件
git diff --cached
git commit -m "清楚说明这次改了什么"
```

## status：看当前状态

```bash
git status
```

重点看三类：

- `modified`：已跟踪文件被修改
- `untracked`：新文件，Git 还没跟踪
- `Changes to be committed`：已经进入暂存区，下一次 commit 会提交

简洁版：

```bash
git status -sb
```

常用于快速看当前分支和改动状态。

## diff：看具体改了什么

看工作区还没暂存的改动：

```bash
git diff
```

看某个文件：

```bash
git diff README.md
```

看已经暂存、准备提交的改动：

```bash
git diff --cached
```

或者：

```bash
git diff --staged
```

## add：只添加该提交需要的内容

添加指定文件：

```bash
git add README.md
```

添加某个目录：

```bash
git add git_learning/
```

谨慎使用：

```bash
git add .
```

它会把当前目录下所有没有被 `.gitignore` 忽略的改动加入暂存区。学习项目里有数据集、模型文件、爬虫结果时尤其要小心。

## 交互式 add

只想提交一个文件里的部分改动：

```bash
git add -p
```

Git 会把改动拆成小块问你：

- `y`：暂存这块
- `n`：不暂存这块
- `s`：继续拆小
- `q`：退出

这个命令很适合把“顺手改的东西”和“本次真正任务”分开提交。

## commit：保存一个版本

```bash
git commit -m "更新 Git 进阶笔记"
```

好 commit 的标准：

- 只做一类事情
- message 能说明目的
- 不混入临时文件、大数据、无关改动

不推荐：

```text
update
fix
111
继续调整
```

更推荐：

```text
整理 Git 进阶查阅笔记
移除 Reddit 评论数据跟踪
补充 gitignore 大文件处理说明
```

## 修改最近一次 commit

提交后发现漏了一个文件：

```bash
git add 漏掉的文件
git commit --amend
```

只改最近一次提交说明：

```bash
git commit --amend -m "新的提交说明"
```

注意：如果这个 commit 已经 push 并且别人可能基于它开发了，不要随便 amend。

## 推荐提交前检查清单

```bash
git status -sb
git diff --cached
```

确认：

- 暂存区里只有本次要提交的文件
- 没有大数据、模型、临时输出
- commit message 能看懂

