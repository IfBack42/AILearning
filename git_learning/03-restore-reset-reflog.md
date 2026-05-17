# 03 restore / reset / reflog

这个模块解决一个问题：**改错了、提交错了、撤错了，如何救回来。**

## 先分清三个区域

```text
工作区：你当前看到的文件
暂存区：下一次 commit 准备提交的内容
提交历史：已经 commit 的版本
```

不同区域用不同命令，不要混用。

## restore：撤销工作区或暂存区

取消暂存，但保留文件修改：

```bash
git restore --staged 文件名
```

放弃某个文件的工作区修改：

```bash
git restore 文件名
```

危险点：`git restore 文件名` 会丢掉该文件未提交的修改。

## reset：移动分支指针

`reset` 主要影响提交历史和暂存区。

### soft：撤回 commit，保留暂存

```bash
git reset --soft HEAD~1
```

效果：

- 最近一次 commit 被撤回
- 改动还在暂存区
- 适合“刚 commit，发现 message 错或想重新组织提交”

### mixed：撤回 commit，取消暂存，保留文件修改

```bash
git reset HEAD~1
```

或者：

```bash
git reset --mixed HEAD~1
```

效果：

- commit 被撤回
- 改动回到工作区
- 默认就是 mixed

### hard：撤回 commit，并丢弃文件修改

```bash
git reset --hard HEAD~1
```

危险。它会让工作区也回到目标提交，未保存的修改会消失。

除非你非常确定，否则不要用。

## revert：用新提交反向撤销

如果某个 commit 已经 push 到远程，推荐用：

```bash
git revert 提交ID
```

它不会改写历史，而是新增一个“反向提交”。

适合团队协作中撤销线上错误。

## reflog：救命记录

`reflog` 会记录 HEAD 移动历史。

```bash
git reflog
```

如果你 reset 错了，可以先看：

```bash
git reflog
```

找到想回去的位置：

```bash
git reset --hard HEAD@{编号}
```

注意：这也是危险操作。先确认 `git status`，必要时先备份或建临时分支。

## 建临时救援分支

不确定要不要回退时，可以先在当前位置打个分支：

```bash
git branch backup/before-reset
```

这样即使 reset 错了，也能回来。

## 常见场景

### add 错了，但还没 commit

```bash
git restore --staged .
```

### commit 错了，但没 push

```bash
git reset --soft HEAD~1
```

重新整理后再提交。

### 已经 push 了，想撤销某次提交

```bash
git revert 提交ID
git push
```

### reset 后后悔了

```bash
git reflog
git reset --hard HEAD@{你要回去的位置}
```

