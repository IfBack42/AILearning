# 06 stash / cherry-pick / tag

这个模块解决三个进阶场景：**临时保存、挑选提交、标记版本。**

## stash：临时保存工作区

场景：你正在改一半，突然要切分支处理别的事。

保存当前修改：

```bash
git stash
```

带说明：

```bash
git stash push -m "临时保存 README 修改"
```

查看 stash 列表：

```bash
git stash list
```

恢复最近一次：

```bash
git stash pop
```

只应用不删除 stash：

```bash
git stash apply
```

删除某个 stash：

```bash
git stash drop stash@{0}
```

清空所有 stash：

```bash
git stash clear
```

谨慎使用 `clear`。

## stash 常见注意点

默认 `git stash` 主要保存已跟踪文件的改动。

如果要包含 untracked 文件：

```bash
git stash -u
```

如果恢复时冲突，和普通冲突一样手动解决。

## cherry-pick：挑一个提交过来

场景：某个分支上有一个 commit 很有用，但你不想合并整个分支。

```bash
git cherry-pick 提交ID
```

例如：

```bash
git cherry-pick 83985be
```

如果冲突：

```bash
git status
git add 冲突文件
git cherry-pick --continue
```

放弃：

```bash
git cherry-pick --abort
```

## cherry-pick 适用场景

适合：

- 把 bugfix 从一个分支搬到另一个分支
- 只拿某一次文档修改
- 临时补丁

不适合：

- 长期用它代替正常 merge/rebase
- 一次挑很多互相依赖的提交

## tag：给版本打标签

查看标签：

```bash
git tag
```

创建轻量标签：

```bash
git tag v1.0.0
```

创建带说明的标签：

```bash
git tag -a v1.0.0 -m "第一个稳定版本"
```

推送标签：

```bash
git push origin v1.0.0
```

推送所有标签：

```bash
git push origin --tags
```

删除本地标签：

```bash
git tag -d v1.0.0
```

删除远程标签：

```bash
git push origin --delete v1.0.0
```

## 推荐记忆

```text
stash       临时放一边
cherry-pick 从别处摘一个提交
tag         给某个版本贴标签
```

