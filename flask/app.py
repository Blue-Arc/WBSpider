from flask import Flask, jsonify, request, Response
from flask_cors import *
from flask import render_template #引入模板插件

import sys
sys.path.append("..")  
from main import execute
from info import Info

app = Flask(__name__,
static_folder='../vue/static',  # 设置静态文件夹目录
template_folder = "../vue")  # 设置vue编译输出目录dist文件夹，为Flask模板文件目录
CORS(app, supports_credentials=True) # 跨域解决方案




@app.route('/')
@app.route('/login')
def index():
    return render_template('index.html',name='index') #使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。

"""
login 的后端api
""" 
@app.route("/api/checklogin", methods=['POST'])
def login():
    global cookie
    if request.method == 'POST' and request.form.get('username') and request.form.get('password'):
        data = request.form.to_dict()
        uname = data.get("username")
        passwd = data.get("password")
        cookie = execute(uname, passwd)
        if cookie == -1:
            return Response("-1")
        else:
            return Response("0")
    else:
        return Response("-1")

@app.route("/api/search", methods=['POST'])
def search():
    global cookie
    info = Info(cookie)
    if request.method == 'POST' and request.form.get('uname'):
        data = request.form.to_dict()
        uname = data.get("uname")
        uid = info.get_Info(uname)
        return Response(uid)
        
if __name__ == '__main__':
    app.run(debug=True)