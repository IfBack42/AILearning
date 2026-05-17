# 05 merge / rebase / conflict

这个模块解决一个问题：**如何同步 main、整理提交历史、处理冲突。**

## merge 和 rebase 的区别

假设你在 `feature/a` 开发，同时 `main` 也更新了。

### merge

```bash
git merge main
```

特点：

- 保留真实分叉历史
- 可能产生 merge commit
- 安全直观

### rebase

```bash
git rebase main
```

特点：

- 把你的提交“挪到”最新 main 后面
- 历史更直
- 会改写当前分支提交历史

简单理解：

```text
merge：把别人的变化合进来
rebase：把我的变化重新放到最新基础上
```

## 什么时候用 merge

适合：

- 团队不要求线性历史
- 你不想改写提交历史
- 分支已经被多人使用

命令：

```bash
git switch feature/a
git fetch origin
git merge origin/main
```

## 什么时候用 rebase

适合：

- 自己的 feature 分支
- 还没被别人基于它开发
- 想让 PR 历史更干净

命令：

```bash
git switch feature/a
git fetch origin
git rebase origin/main
```

如果已经 push 过 feature 分支，rebase 后需要：

```bash
git push --force-with-lease
```

不要用普通 `--force`，`--force-with-lease` 会更安全。

## 冲突是什么

冲突不是错误。

冲突的意思是：Git 不知道该保留哪一边，需要你人工判断。

冲突文件里会出现：

```text
<<<<<<< HEAD
当前分支内容
=======
被合并或被 rebase 的内容
>>>>>>> branch-name
```

你要手动改成最终想要的样子，然后保存。

## merge 冲突处理

```bash
git status
```

打开冲突文件，手动解决后：

```bash
git add 冲突文件
git commit
```

如果不想继续 merge：

```bash
git merge --abort
```

## rebase 冲突处理

解决文件后：

```bash
git add 冲突文件
git rebase --continue
```

如果还有冲突，继续解决。

放弃这次 rebase：

```bash
git rebase --abort
```

跳过当前提交：

```bash
git rebase --skip
```

`skip` 要谨慎，因为它会丢掉当前这个提交的修改。

## interactive rebase：整理提交历史

整理最近 3 次提交：

```bash
git rebase -i HEAD~3
```

常见操作：

- `pick`：保留
- `reword`：修改提交说明
- `squash`：合并到前一个提交
- `fixup`：合并到前一个提交，并丢掉当前提交说明
- `drop`：删除提交

适合在 PR 前整理自己的 feature 分支。

不要随便整理已经共享给别人使用的公共分支。

## 推荐策略

个人 feature 分支：

```bash
git fetch origin
git rebase origin/main
```

公共分支或不确定情况：

```bash
git fetch origin
git merge origin/main
```

不确定时，先别 rebase。

