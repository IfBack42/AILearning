# 04 branch / remote / PR / cleanup

这个模块解决一个问题：**分支和远程仓库怎么管理，PR 合并后怎么收尾。**

## 分支查看

查看本地分支：

```bash
git branch
```

查看远程分支：

```bash
git branch -r
```

查看全部分支：

```bash
git branch -a
```

更详细：

```bash
git branch -vv
```

能看到本地分支跟踪哪个远程分支，以及领先/落后情况。

## 创建和切换分支

推荐新命令：

```bash
git switch main
git switch -c feature/readme
```

老命令也能用：

```bash
git checkout main
git checkout -b feature/readme
```

## 远程仓库

查看远程：

```bash
git remote -v
```

添加远程：

```bash
git remote add origin 仓库地址
```

修改远程地址：

```bash
git remote set-url origin 新地址
```

## push 分支

第一次 push 新分支：

```bash
git push -u origin feature/readme
```

后续：

```bash
git push
```

`-u` 的作用是建立本地分支和远程分支的默认关联。

## fetch 与 pull

只下载远程信息，不自动合并：

```bash
git fetch origin
```

下载并合并：

```bash
git pull
```

更稳的习惯：

```bash
git fetch origin
git status -sb
```

先看清楚本地和远程差异，再决定 merge 或 rebase。

## PR 合并后的标准收尾

假设 `feature/readme` 已经在 GitHub 上合并进 `main`。

本地切回 main：

```bash
git switch main
```

同步远程 main：

```bash
git pull origin main
```

删除本地 feature 分支：

```bash
git branch -d feature/readme
```

删除远程 feature 分支：

```bash
git push origin --delete feature/readme
```

清理本地记录里已经不存在的远程分支：

```bash
git fetch --prune
```

## 删除分支的区别

安全删除：

```bash
git branch -d 分支名
```

强制删除：

```bash
git branch -D 分支名
```

`-D` 会删除未合并分支，谨慎使用。

## 常见场景

### 我想知道当前分支有没有推到远程

```bash
git branch -vv
```

### 远程分支 GitHub 上删了，本地还看得到

```bash
git fetch --prune
```

### push 提示没有 upstream

```bash
git push -u origin 当前分支名
```

