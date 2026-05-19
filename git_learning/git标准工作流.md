# GitHub 协作开发 README（当前阶段）

适合：

* 初学 Git 的开发者
* 团队协作开发
* 从“压缩包传代码”转向 GitHub 工作流
* 日常 feature 分支开发

---

# 一、Git 与 GitHub 的关系

## Git

本地版本管理工具。

负责：

* commit
* branch
* diff
* 历史管理

即使没有网络也能使用。

---

## GitHub

远程代码仓库平台。

负责：

* 存储代码
* 团队协作
* Pull Request（PR）
* 权限管理

---

# 二、第一次配置 Git

## 1. 配置用户名

```bash id="1jlwmr"
git config --global user.name "你的名字"
```

---

## 2. 配置邮箱

```bash id="2jlwmr"
git config --global user.email "你的邮箱"
```

---

## 3. 查看配置

```bash id="3jlwmr"
git config --list
```

---

# 三、克隆远程仓库

## clone 项目

```bash id="4jlwmr"
git clone https://github.com/用户名/仓库名.git
```

例如：

```bash id="5jlwmr"
git clone https://github.com/1nancy23/YiLiao.git
```

---

## 进入项目目录

```bash id="6jlwmr"
cd YiLiao
```

---

# 四、远程仓库 remote

## 查看当前连接的远程仓库

```bash id="7jlwmr"
git remote -v
```

输出类似：

```text id="8jlwmr"
origin  https://github.com/1nancy23/YiLiao.git (fetch)
origin  https://github.com/1nancy23/YiLiao.git (push)
```

---

## 含义

### origin

远程仓库默认名字。

---

### fetch

用于拉取代码。

---

### push

用于上传代码。

---

# 五、查看当前状态

## 查看仓库状态

```bash id="9jlwmr"
git status
```

重点看：

---

## 当前所在分支

```text id="10jlwmr"
On branch main
```

---

## 是否和远程同步

```text id="11jlwmr"
Your branch is up to date with 'origin/main'
```

---

## 是否有修改

```text id="12jlwmr"
modified:
untracked:
```

---

# 六、查看当前分支

```bash id="13jlwmr"
git branch
```

例如：

```text id="14jlwmr"
* main
```

星号：

表示当前所在分支。

---

# 七、同步最新 main（开发前必须）

## 切换到 main

```bash id="15jlwmr"
git checkout main
```

---

## 拉取最新 main

```bash id="16jlwmr"
git fetch -p
git pull origin main
```

作用：

```text id="17jlwmr"
让本地 main 与远程 main 保持一致
```

---

# 八、创建自己的开发分支

## 创建并切换分支

```bash id="18jlwmr"
git checkout -b feature/xxx
```

例如：

```bash id="19jlwmr"
git checkout -b feature/readme
```

---

## 再次确认分支

```bash id="20jlwmr"
git branch
```

例如：

```text id="21jlwmr"
main
* feature/readme
```

说明：

当前已经进入自己的开发分支。

---

# 九、开始修改代码

此时：

可以安全开发。

因为：

```text id="22jlwmr"
不会影响 main
```

---

# 十、提交代码

## 查看修改状态

```bash id="23jlwmr"
git status
```

---

## 添加文件到暂存区

添加指定文件：

```bash id="24jlwmr"
git add README.md
```

添加全部：

```bash id="25jlwmr"
git add .
```

---

## commit 提交

```bash id="26jlwmr"
git commit -m "写了readme"
```

---

# 十一、push 到 GitHub

## 第一次 push

```bash id="27jlwmr"
git push -u origin feature/readme
```

---

## 含义

### push

上传代码。

---

### origin

远程仓库。

---

### feature/readme

上传的分支。

---

### -u

建立：

```text id="28jlwmr"
本地分支 ↔ 远程分支
```

跟踪关系。

---

## 后续 push

```bash id="29jlwmr"
git push
```

即可。

---

# 十二、Pull Request（PR）

push 后：

GitHub 会提示：

```text id="30jlwmr"
Compare & pull request
```

---

## 创建 PR

填写：

### Title

```text id="31jlwmr"
完善 README
```

---

### Description

```text id="32jlwmr"
添加项目说明与开发流程
```

---

点击：

```text id="33jlwmr"
Create pull request
```

---

# 十三、PR 与 Merge

## PR 是什么？

PR：

```text id="34jlwmr"
Pull Request
```

意思：

```text id="35jlwmr"
请求把我的代码合并到 main
```

---

## 谁创建 PR？

通常：

```text id="36jlwmr"
开发者自己
```

---

## 谁 merge？

通常：

```text id="37jlwmr"
管理员 / 项目负责人
```

例如：

师兄。

---

# 十四、merge 后正确流程

## 回到 main

```bash id="38jlwmr"
git checkout main
```

---

## 同步最新 main

```bash id="39jlwmr"
git pull origin main
```

因为：

```text id="40jlwmr"
远程 main 已更新，
本地 main 还未同步
```

---

# 十五、开始新任务

## 创建新的 feature 分支

```bash id="41jlwmr"
git checkout -b feature/new-task
```

原则：

```text id="42jlwmr"
一个功能，一个分支
```

---

# 十六、删除 feature 分支（推荐）

merge 后：

feature 分支通常可以删除。

---

## 删除本地分支

注意：

不能删除当前分支。

先切回：

```bash id="43jlwmr"
git checkout main
```

再删除：

```bash id="44jlwmr"
git branch -d feature/readme
```

---

## 删除远程分支

```bash id="45jlwmr"
git push origin --delete feature/readme
```

---

# 十七、为什么删除分支不会丢代码？

因为：

merge 后：

代码已经进入：

```text id="46jlwmr"
main
```

分支只是：

```text id="47jlwmr"
一个指针名字
```

删除分支：

不会删除已经 merge 的代码。

---

# 十八、当前阶段最重要的 Git 命令

## 查看状态

```bash id="48jlwmr"
git status
```

---

## 查看分支

```bash id="49jlwmr"
git branch
```

---

## 查看远程仓库

```bash id="50jlwmr"
git remote -v
```

---

## 切换分支

```bash id="51jlwmr"
git checkout 分支名
```

---

## 创建并切换分支

```bash id="52jlwmr"
git checkout -b feature/xxx
```

---

## 同步 main

```bash id="53jlwmr"
git checkout main
git pull origin main
```

---

## 添加修改

```bash id="54jlwmr"
git add .
```

---

## 提交

```bash id="55jlwmr"
git commit -m "message"
```

---

## push

```bash id="56jlwmr"
git push
```

---

# 十九、当前阶段最重要的工程思想

---

## 1. main 永远稳定

不要直接在 main 开发。

---

## 2. feature 分支开发

每个功能单独分支。

---

## 3. 开发前同步 main

```bash id="57jlwmr"
git checkout main
git pull origin main
```

---

## 4. push 不等于 merge

push：

只是上传分支。

---

## 5. PR 才是正式合并

---

# 二十、当前阶段暂时不用深入的内容

后续再学习：

* rebase
* merge conflict
* stash
* cherry-pick
* reflog
* interactive rebase
* CI/CD

当前：

先把：

```text id="58jlwmr"
clone
branch
commit
push
PR
merge
```

完整走熟。
