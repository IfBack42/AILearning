"""
================================================================================
PLAYWRIGHT ROLE 定位器 - 快速记忆手册
================================================================================

## 核心理解
page.get_by_role(角色名, name=文本内容)
- 第一个参数 = ARIA 角色（不是 HTML 标签名）
- name = 元素内的文本内容（或 aria-label）

## 常用角色 ↔ HTML标签 对应关系（默认情况下）
角色名          | 对应的HTML标签（或场景）
---------------|-----------------------------------
"link"         | <a> (有href属性)
"button"       | <button>, 或任意 role="button" 的元素
"heading"      | <h1> ~ <h6>
"textbox"      | <input type="text">, <textarea>
"checkbox"     | <input type="checkbox">
"radio"        | <input type="radio">
"combobox"     | <select> 或带下拉的输入框
"list"         | <ul>, <ol> (role="list")
"listitem"     | <li>
"img"          | <img> 或 role="img"
"table"        | <table>
"row"          | <tr>
"cell"         | <td>

## 三个最快上手例子
# 1. 找写着“登录”的按钮
page.get_by_role("button", name="登录")

# 2. 找写着“下一页”的链接（注意是link不是a）
page.get_by_role("link", name="下一页")

# 3. 找文字是“用户名”的输入框
page.get_by_role("textbox", name="用户名")

## 什么时候用 role 定位？（记住原则）
- 优先用 get_by_role() → 更接近真实用户行为，且当class/id不稳定时尤其好用
- 如果元素没有合适的角色（比如某个<div>只是容器），再用CSS选择器

## 注意陷阱
- 不要写 page.get_by_role("a", ...) → 没有"a"这个角色，要用"link"
- name匹配的是**可访问名称**：通常 = 元素内部文本，如果文本为空则找 aria-label
- 如果页面有多个相同角色且相同name，会匹配第一个（可以再加filter）

================================================================================
"""