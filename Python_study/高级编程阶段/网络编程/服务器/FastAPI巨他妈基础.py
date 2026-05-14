#1.导入模块
#导入FastAPI类
from fastapi import FastAPI
#导入Response类，用于返回数据给浏览器端
from fastapi import Response
#导入uvicorn模块用于保持程序一直运行
import uvicorn
#2.创建FastAPI对象
app = FastAPI()
#3.通过@app路由装饰器收发消息
@app.get("/favicon.ico")
def main():
    with open("source/html/favicon.ico", "rb") as f:
        data = f.read()

    return Response(content=data,media_type="image/png")

#4.运行服务器
#FastAPI对象
#绑定IP
#绑定端口
uvicorn.run(app,host="192.168.0.10",port=8999)
"""
从代码逻辑来看，这段代码主要是通过 FastAPI 提供静态 HTML 页面的访问功能。
然而，它目前的实现方式存在一些问题，导致无法正常支持 HTML 页面中其他链接的访问以及 CSS 文件的请求。以下是具体分析：
1. HTML 页面中其他链接的访问
在你的代码中，index.html 和 gdp.html 是通过 FastAPI 的路由装饰器分别绑定到 /index.html 和 /gdp.html 路径上。如果在 index.html 页面中存在指向其他页面的链接（例如 <a href="/about.html">About</a>），那么当用户点击该链接时，FastAPI 会尝试访问 /about.html 路径。然而，你的代码中并没有定义 /about.html 的路由处理函数，因此 FastAPI 会返回 404 错误。
2. CSS 文件的请求
HTML 页面通常会通过 <link> 标签引入 CSS 文件，例如：
HTML
复制
<link rel="stylesheet" href="styles.css">
在这种情况下，浏览器会向服务器请求 /styles.css 路径。然而，你的代码中并没有定义处理静态文件（如 CSS 文件）的路由。
因此，当浏览器请求 CSS 文件时，FastAPI 会返回 404 错误。
解决方案
为了支持 HTML 页面中其他链接的访问以及 CSS 文件的请求，可以采用以下方法：
方法 1：使用 FastAPI 的 StaticFiles 模块
FastAPI 提供了 StaticFiles 模块，可以方便地托管静态文件（如 HTML、CSS、JavaScript 等）。以下是改进后的代码：
Python
复制


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

# 创建 FastAPI 对象
app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="source/html"), name="static")

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(app, host="192.168.27.93", port=8000)
    
    
目录结构：
复制
project/
├── source/
│   └── html/
│       ├── index.html
│       ├── gdp.html
│       └── styles.css
└── text_stitcher.py
HTML 示例：
在 index.html 中，可以这样引用 CSS 文件：
HTML
复制
<link rel="stylesheet" href="/static/styles.css">
通过这种方式，FastAPI 会自动处理 /static 路径下的所有静态文件请求，
包括 HTML 页面、CSS 文件、JavaScript 文件等。"""