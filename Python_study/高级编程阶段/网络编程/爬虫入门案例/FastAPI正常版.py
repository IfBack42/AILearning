#1.导入模块
from fastapi import FastAPI
from fastapi import Response
import uvicorn

#2.创建FastAPI对象
app = FastAPI()

#3.使用路由装饰器进行收发
@app.get("/")
def get_():
    with open("source/html/index.html", "rb") as f:
        data = f.read()
    return Response(content=data,media_type="text/html")
@app.get("/{path}")
def get_html(path:str):
    with open(f"source/html/{path}","rb") as f:
        data = f.read()
    return Response(content=data,media_type="text/html")

@app.get("/images/{path}")
def get_images(path:str):
    with open(f"source/images/{path}","rb") as f:
        data = f.read()
    return Response(content=data,media_type="jpg")
"""
@app.get("/{path:path}")    #单个path代表捕获/ /中的一小段路径，如/images/{path}/0.jpg
def index(path: str):        #path：path代表捕获所有路径，如/images/{path：path}，可以是很长的一段
    if path == "/" or path == "/images/index.html":  #用{path：path}开头会捕获所有路径，导致其他路由失效
        with open("source/html/index.html","rb") as f: #所以放在最后，且加上没找到的处理
            data0 = f.read()
        return Response(content=data0,media_type="text/html")
    else:
        return Response(content="404 Not Found", media_type="text/plain", status_code=404)
"""
#4.使用uvicorn启动服务
uvicorn.run(app,host="192.168.0.11",port=8999)