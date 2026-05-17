# 02 log / show / blame

这个模块解决一个问题：**如何查看历史，并定位一次改动从哪里来。**

## log：看提交历史

简洁历史：

```bash
git log --oneline
```

带分支图：

```bash
git log --oneline --graph --decorate --all
```

只看最近 10 条：

```bash
git log --oneline -10
```

查看某个文件的历史：

```bash
git log --oneline -- README.md
```

## log 常用筛选

按作者：

```bash
git log --author="name"
```

按时间：

```bash
git log --since="2026-05-01"
git log --until="2026-05-18"
```

按提交信息搜索：

```bash
git log --grep="gitignore"
```

查某个字符串在哪次提交中被加入或删除：

```bash
git log -S "massive_content" --oneline
```

## show：看某一次提交详情

```bash
git show 提交ID
```

例如：

```bash
git show 83985be
```

只看某次提交改了哪些文件：

```bash
git show --name-only 83985be
```

只看统计：

```bash
git show --stat 83985be
```

## blame：查某一行是谁改的

```bash
git blame README.md
```

只查某个范围：

```bash
git blame -L 10,30 README.md
```

`blame` 不是为了甩锅，而是为了找到上下文：这个改动是什么时候、为什么出现的。

## 查看两个提交之间的差异

```bash
git diff 旧提交ID 新提交ID
```

例如：

```bash
git diff HEAD~1 HEAD
```

意思是查看上一次提交和当前提交之间的差异。

## 常见场景

### 我想知道最近一次提交改了什么

```bash
git show --stat HEAD
git show HEAD
```

### 我想知道某个文件最近谁改过

```bash
git log --oneline -- 文件名
git blame 文件名
```

### 我想找某个大文件什么时候进来的

```bash
git log --all -- 文件路径
git log -S "文件名关键字" --all --oneline
```

如果大文件已经进过历史，即使当前删除了，GitHub push 仍可能失败。这时要考虑历史清理。

