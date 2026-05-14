# Flask 服务端演示
"""
Flask - 核心应用类:
    创建Flask应用实例: app = Flask(__name__)
    注册路由、启动服务器
request - 请求对象
    获取客户端请求数据
    常用属性:
    request.args - GET参数
    request.form - POST表单数据
    request.json - JSON请求体
    request.method - HTTP方法
    request.files - 上传文件
jsonify - JSON响应函数
    将Python对象转为JSON响应
    自动设置 Content-Type: application/json
    用法: return jsonify({"key": "value"})
Response - 响应对象基类
    自定义HTTP响应
    可设置状态码、响应头、MIME类型
    用法: Response(data, status=200, mimetype='text/html')
"""

from flask import Flask, request, jsonify, Response

# 1.初始化flask应用
app = Flask(__name__)
app.json.ensure_ascii = False # 解决中文乱码

# 2.创建路由和响应函数
@app.route('/bilibli',method=['POST'])
def bilibili():
    pass

