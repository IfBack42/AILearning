# 04 远程仓库和 GitHub

这一节学习如何把本地仓库和 GitHub 连接起来。

## 本地仓库和远程仓库

本地仓库：保存在你电脑里的 Git 仓库。

远程仓库：保存在 GitHub 上的 Git 仓库。

它们的关系可以理解为：

```text
你的电脑 <-> GitHub
```

本地写代码，提交后推送到 GitHub；别人或者另一台电脑也可以从 GitHub 拉取代码。

## 查看远程仓库

```bash
git remote -v
```

如果还没有绑定 GitHub，通常不会输出内容。

## 添加远程仓库

在 GitHub 创建一个新仓库后，会得到一个地址，比如：

```text
https://github.com/用户名/仓库名.git
```

绑定远程仓库：

```bash
git remote add origin https://github.com/用户名/仓库名.git
```

这里的 `origin` 是远程仓库的默认名字。

## 第一次推送

```bash
git push -u origin main
```

含义：

- `push`：把本地提交推送到远程
- `origin`：远程仓库名字
- `main`：要推送的分支
- `-u`：建立本地分支和远程分支的默认关联

第一次推送后，以后通常只需要：

```bash
git push
```

## 从 GitHub 拉取更新

```bash
git pull
```

意思是：把远程仓库的新提交拉到本地，并尝试合并。

## 克隆别人的仓库

```bash
git clone 仓库地址
```

例如：

```bash
git clone https://github.com/用户名/仓库名.git
```

`clone` 会把整个远程仓库下载到本地，包括历史记录。

## 常见流程

本地已有项目，第一次上传 GitHub：

```bash
git init
git add .
git commit -m "初始化项目"
git remote add origin https://github.com/用户名/仓库名.git
git push -u origin main
```

已经绑定远程仓库后，日常提交：

```bash
git status
git add .
git commit -m "说明这次修改"
git push
```

## 初学者要记住

`commit` 是提交到本地仓库。

`push` 是把本地提交上传到 GitHub。

所以只 commit 不 push，GitHub 上是看不到新代码的。

